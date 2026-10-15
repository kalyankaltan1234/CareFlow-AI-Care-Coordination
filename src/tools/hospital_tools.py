from typing import Dict, Any, List, Optional

# Hospital Doctor Roster across diverse specialties
DOCTOR_SCHEDULES: Dict[str, List[Dict[str, Any]]] = {
    "General Medicine": [
        {"doctor_id": "DOC-301", "name": "Dr. Sneha Reddy", "qualification": "MD (Internal Medicine)", "available_slots": ["2026-10-06 11:30 AM", "2026-10-06 03:00 PM"]},
        {"doctor_id": "DOC-302", "name": "Dr. Rajesh Kulkarni", "qualification": "MBBS, MD (Senior Physician)", "available_slots": ["2026-10-06 04:30 PM", "2026-10-07 10:00 AM"]},
        {"doctor_id": "DOC-303", "name": "Dr. Vikram Sen", "qualification": "MD (General Medicine)", "available_slots": ["2026-10-06 01:00 PM", "2026-10-07 02:00 PM"]},
        {"doctor_id": "DOC-304", "name": "Dr. Anita Desai", "qualification": "MBBS, DNB (Family Medicine)", "available_slots": ["2026-10-06 10:30 AM", "2026-10-06 05:00 PM"]}
    ],
    "Infectious Diseases": [
        {"doctor_id": "DOC-401", "name": "Dr. Arvind Swamy", "qualification": "MD, DM (Infectious Diseases)", "available_slots": ["2026-10-06 11:00 AM", "2026-10-06 03:30 PM"]},
        {"doctor_id": "DOC-402", "name": "Dr. Meenakshi Sundaram", "qualification": "MD (Tropical Medicine)", "available_slots": ["2026-10-06 02:00 PM", "2026-10-07 11:30 AM"]}
    ],
    "Neurology": [
        {"doctor_id": "DOC-101", "name": "Dr. Ananya Sharma", "qualification": "MD, DM (Neurology)", "available_slots": ["2026-10-06 10:00 AM", "2026-10-06 02:30 PM"]},
        {"doctor_id": "DOC-102", "name": "Dr. Rohan V. Kulkarni", "qualification": "MD (Neurology Specialist)", "available_slots": ["2026-10-06 04:00 PM", "2026-10-07 09:30 AM"]}
    ],
    "Cardiology": [
        {"doctor_id": "DOC-201", "name": "Dr. Arvind Mehta", "qualification": "MD, DM (Cardiology)", "available_slots": ["2026-10-06 09:30 AM", "2026-10-08 03:00 PM"]},
        {"doctor_id": "DOC-202", "name": "Dr. Kavita Iyer", "qualification": "DNB, FACC (Interventional Cardiology)", "available_slots": ["2026-10-06 02:00 PM", "2026-10-07 11:00 AM"]}
    ],
    "Pulmonology": [
        {"doctor_id": "DOC-501", "name": "Dr. Farhan Akhtar", "qualification": "MD, DNB (Pulmonology & Chest)", "available_slots": ["2026-10-06 11:30 AM", "2026-10-06 04:00 PM"]},
        {"doctor_id": "DOC-502", "name": "Dr. Sunita Deshmukh", "qualification": "MD (Respiratory Medicine)", "available_slots": ["2026-10-06 01:30 PM", "2026-10-07 10:30 AM"]}
    ],
    "Gastroenterology": [
        {"doctor_id": "DOC-701", "name": "Dr. Sandeep Singhania", "qualification": "MD, DM (Gastroenterology)", "available_slots": ["2026-10-06 10:30 AM", "2026-10-06 03:00 PM"]},
        {"doctor_id": "DOC-702", "name": "Dr. Radhika Joshi", "qualification": "MD (Digestive Diseases)", "available_slots": ["2026-10-06 02:30 PM", "2026-10-07 11:00 AM"]},
        {"doctor_id": "DOC-703", "name": "Dr. Suresh Nambiar", "qualification": "MD, DM (Hepatology)", "available_slots": ["2026-10-06 12:00 PM", "2026-10-07 04:00 PM"]}
    ],
    "Endocrinology": [
        {"doctor_id": "DOC-601", "name": "Dr. Harish Chandra", "qualification": "MD, DM (Endocrinology & Diabetology)", "available_slots": ["2026-10-06 11:00 AM", "2026-10-06 03:30 PM"]},
        {"doctor_id": "DOC-602", "name": "Dr. Shweta Bansal", "qualification": "MD (Diabetes Care Specialist)", "available_slots": ["2026-10-06 01:00 PM", "2026-10-07 10:00 AM"]}
    ],
    "Urology": [
        {"doctor_id": "DOC-801", "name": "Dr. Pradeep Chawla", "qualification": "MS, MCh (Urology & Renal Care)", "available_slots": ["2026-10-06 10:00 AM", "2026-10-06 02:00 PM"]},
        {"doctor_id": "DOC-802", "name": "Dr. Manoj Tiwari", "qualification": "MD, DNB (Nephrology)", "available_slots": ["2026-10-06 03:30 PM", "2026-10-07 11:30 AM"]}
    ],
    "Orthopedics": [
        {"doctor_id": "DOC-901", "name": "Dr. Sanjay Kapoor", "qualification": "MS (Orthopedics & Joint Replacement)", "available_slots": ["2026-10-06 11:30 AM", "2026-10-06 04:00 PM"]},
        {"doctor_id": "DOC-902", "name": "Dr. Deepa George", "qualification": "MD (Rheumatology & Arthritis)", "available_slots": ["2026-10-06 01:30 PM", "2026-10-07 10:00 AM"]}
    ],
    "Dermatology": [
        {"doctor_id": "DOC-1001", "name": "Dr. Tanvi Kapoor", "qualification": "MD (Dermatology, Venereology & Leprosy)", "available_slots": ["2026-10-06 10:30 AM", "2026-10-06 03:00 PM"]},
        {"doctor_id": "DOC-1002", "name": "Dr. Amit Saxena", "qualification": "MBBS, DVD (Allergy & Skin Specialist)", "available_slots": ["2026-10-06 02:00 PM", "2026-10-07 11:00 AM"]}
    ]
}

BOOKED_APPOINTMENTS: List[Dict[str, Any]] = []

def lookup_available_slots(specialty: str) -> List[Dict[str, Any]]:
    """Look up available doctor appointment slots by specialty across our network."""
    matched_specialty = None
    spec_lower = specialty.lower()
    
    # Direct specialty matching
    for s in DOCTOR_SCHEDULES:
        if s.lower() in spec_lower or spec_lower in s.lower():
            matched_specialty = s
            break
            
    if not matched_specialty:
        if any(w in spec_lower for w in ["neuro", "head", "migraine", "brain"]):
            matched_specialty = "Neurology"
        elif any(w in spec_lower for w in ["heart", "cardio", "chest", "bp", "hypertension"]):
            matched_specialty = "Cardiology"
        elif any(w in spec_lower for w in ["lung", "breath", "pulmon", "asthma", "cough"]):
            matched_specialty = "Pulmonology"
        elif any(w in spec_lower for w in ["dengue", "malaria", "typhoid", "virus", "infection", "infectious"]):
            matched_specialty = "Infectious Diseases"
        elif any(w in spec_lower for w in ["stomach", "gastric", "acidity", "liver", "jaundice", "digest"]):
            matched_specialty = "Gastroenterology"
        elif any(w in spec_lower for w in ["sugar", "diabet", "endocrin", "thyroid"]):
            matched_specialty = "Endocrinology"
        elif any(w in spec_lower for w in ["kidney", "stone", "uro", "renal", "urine"]):
            matched_specialty = "Urology"
        elif any(w in spec_lower for w in ["joint", "bone", "arthrit", "ortho", "knee"]):
            matched_specialty = "Orthopedics"
        elif any(w in spec_lower for w in ["skin", "derma", "rash", "allergy", "itch"]):
            matched_specialty = "Dermatology"
        else:
            matched_specialty = "General Medicine"
        
    return DOCTOR_SCHEDULES.get(matched_specialty, DOCTOR_SCHEDULES["General Medicine"])

def schedule_appointment(patient_id: str, doctor_id: str, slot_time: str, reason: str) -> Dict[str, Any]:
    """Reserve an appointment slot in the hospital calendar with unique single-use Patient ID validation."""
    from src.tools.patient_registry import consume_patient_id
    
    booking_id = f"BK-{len(BOOKED_APPOINTMENTS) + 1001}"
    appointment = {
        "booking_id": booking_id,
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "slot_time": slot_time,
        "reason": reason,
        "status": "Confirmed (Pending Clinician Sign-off)"
    }
    BOOKED_APPOINTMENTS.append(appointment)
    
    # Single-use ID retirement
    consume_patient_id(
        patient_id=patient_id,
        reason=f"Appointment Booked ({booking_id}) with {doctor_id}",
        booking_id=booking_id
    )
    
    return appointment
