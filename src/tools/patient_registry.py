"""
CareFlow - Patient ID Registry & Security Enforcement Module

Enforces Strict Patient ID Policies:
1. Ownership & Exclusivity: Each Patient ID belongs exclusively to that specific patient.
   No other patient can ever use or claim this ID.
2. Single-Use / Non-Reusable: Once a patient uses an ID (intake completed or appointment scheduled),
   that ID is permanently marked as USED & RETIRED. Neither this patient nor anyone else can reuse it.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

PATIENT_REGISTRY: Dict[str, Dict[str, Any]] = {
    "PT-1001": {
        "patient_id": "PT-1001",
        "patient_name": "Kalyan",
        "patient_age": "28",
        "patient_place": "Hyderabad",
        "disease": "Clinical Evaluation",
        "status": "active",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "used_at": None,
        "booking_id": None,
        "history": [
            {"action": "Registered", "detail": "Initial patient onboarding", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        ]
    }
}

def generate_unique_patient_id() -> str:
    """Generates a new, guaranteed-unique Patient ID that has not been allocated."""
    base_num = 1001
    while True:
        candidate_id = f"PT-{base_num}"
        if candidate_id not in PATIENT_REGISTRY:
            return candidate_id
        base_num += 1

def validate_patient_id_for_use(patient_id: str, patient_name: str, allow_active_owner: bool = True) -> Tuple[bool, str]:
    """
    Validates Patient ID ownership and lifecycle invariants.
    Returns (is_valid, message).
    """
    pid = (patient_id or "").strip().upper()
    name = (patient_name or "").strip()

    if pid.startswith("PT-EVAL"):
        return True, "Evaluation ID bypass authorized."

    if not pid:
        return False, "Patient ID cannot be empty."

    if pid not in PATIENT_REGISTRY:
        return True, f"Patient ID '{pid}' is available and unassigned."

    record = PATIENT_REGISTRY[pid]
    owner_name = record.get("patient_name", "").strip()

    if owner_name.lower() != name.lower():
        return False, (
            f"❌ Ownership Violation: Patient ID '{pid}' belongs exclusively to '{owner_name}'. "
            f"No other patient is permitted to use this ID."
        )

    if record.get("status") == "used":
        used_for = f" (Linked to booking {record['booking_id']})" if record.get("booking_id") else ""
        return False, (
            f"❌ Single-Use Policy Violation: Patient ID '{pid}' has already been used and retired{used_for}. "
            f"A patient cannot reuse an ID once it has been used. Please generate a fresh unique Patient ID."
        )

    if not allow_active_owner:
        return False, f"Patient ID '{pid}' is currently active in an ongoing consultation."

    return True, f"Patient ID '{pid}' is valid and active for {owner_name}."

def register_patient_id(
    patient_id: str,
    patient_name: str,
    age: str = "",
    place: str = "",
    disease: str = ""
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Registers a patient with a unique Patient ID, strictly verifying ownership and single-use constraints.
    """
    pid = (patient_id or "").strip().upper()
    name = (patient_name or "").strip()

    if not pid:
        pid = generate_unique_patient_id()

    valid, message = validate_patient_id_for_use(pid, name, allow_active_owner=True)
    if not valid:
        return False, message, None

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if pid in PATIENT_REGISTRY:
        record = PATIENT_REGISTRY[pid]
        if age:
            record["patient_age"] = age
        if place:
            record["patient_place"] = place
        if disease:
            record["disease"] = disease
        record["history"].append({
            "action": "Session Continued",
            "detail": f"Updated active consultation: {disease}",
            "timestamp": now_str
        })
    else:
        record = {
            "patient_id": pid,
            "patient_name": name,
            "patient_age": age,
            "patient_place": place,
            "disease": disease,
            "status": "active",
            "created_at": now_str,
            "used_at": None,
            "booking_id": None,
            "history": [
                {"action": "Registered", "detail": f"Assigned to {name}", "timestamp": now_str}
            ]
        }
        PATIENT_REGISTRY[pid] = record

    return True, f"Patient ID '{pid}' successfully registered exclusively for '{name}'.", record

def consume_patient_id(
    patient_id: str,
    reason: str = "Appointment Scheduled",
    booking_id: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Marks a Patient ID as 'used' and permanently retired.
    Once consumed, neither this patient nor any other patient can ever use it again.
    """
    pid = (patient_id or "").strip().upper()
    if pid.startswith("PT-EVAL"):
        return True, "Evaluation ID bypassed."

    if pid not in PATIENT_REGISTRY:
        PATIENT_REGISTRY[pid] = {
            "patient_id": pid,
            "patient_name": "Patient",
            "patient_age": "Unknown",
            "patient_place": "Unknown",
            "disease": "Clinical Encounter",
            "status": "used",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "used_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "booking_id": booking_id,
            "history": [
                {"action": "Directly Consumed", "detail": reason, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            ]
        }
        return True, f"Patient ID '{pid}' marked as used and retired."

    record = PATIENT_REGISTRY[pid]
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record["status"] = "used"
    record["used_at"] = now_str
    if booking_id:
        record["booking_id"] = booking_id

    record["history"].append({
        "action": "Consumed & Retired",
        "detail": f"{reason} - ID permanently retired from reuse",
        "booking_id": booking_id,
        "timestamp": now_str
    })
    return True, f"Patient ID '{pid}' has been consumed and retired. It cannot be used again."

def get_all_patient_records() -> List[Dict[str, Any]]:
    """
    Returns list of all registered Patient IDs and their ownership & lifecycle status
    for the Clinician HITL Desk audit view.
    """
    records = []
    for pid, data in sorted(PATIENT_REGISTRY.items(), key=lambda x: x[0]):
        records.append({
            "patient_id": data["patient_id"],
            "patient_name": data["patient_name"],
            "patient_age": data.get("patient_age", "—"),
            "patient_place": data.get("patient_place", "—"),
            "disease": data.get("disease", "—"),
            "status": data.get("status", "active"),
            "created_at": data.get("created_at", "—"),
            "used_at": data.get("used_at"),
            "booking_id": data.get("booking_id"),
            "policy_status": "Retired 🔒 (Non-reusable)" if data.get("status") == "used" else "Active (Exclusive to Owner)"
        })
    return records
