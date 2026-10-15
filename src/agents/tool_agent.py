"""
Hospital Tool Agent Module

Checks hospital doctor rosters for open slots and creates provisional bookings.
All appointments are created with 'Pending Clinician Sign-off' status so that
medical coordinators can review and approve them before releasing the final referral slip.
"""

from src.state import CareFlowState
from src.tools.hospital_tools import lookup_available_slots, schedule_appointment

def run_tool_agent(state: CareFlowState) -> dict:
    """
    Executes hospital roster queries or schedules provisional slots
    based on the structured intake intent.
    """
    intake = state.get("intake")
    patient_id = state.get("patient_id") or "PT-90210"
    
    if not intake or intake.intent != "appointment_booking":
        return {"tool_action": "none", "tool_result": None}

    specialty = intake.requested_specialty or "General Medicine"
    slots_data = lookup_available_slots(specialty)
    
    # If open slots are found for this department, reserve the earliest one
    if slots_data and len(slots_data) > 0:
        first_doc = slots_data[0]
        selected_slot = first_doc["available_slots"][0] if first_doc.get("available_slots") else "Next open slot"
        
        booking = schedule_appointment(
            patient_id=patient_id,
            doctor_id=first_doc["doctor_id"],
            slot_time=selected_slot,
            reason=intake.summary
        )
        return {
            "tool_action": "schedule_appointment",
            "tool_result": {
                "booking": booking,
                "doctor_name": first_doc["name"],
                "specialty": specialty,
                "all_options": slots_data
            }
        }
    
    return {
        "tool_action": "lookup_available_slots",
        "tool_result": {"status": "no_direct_slots_found", "specialty": specialty}
    }
