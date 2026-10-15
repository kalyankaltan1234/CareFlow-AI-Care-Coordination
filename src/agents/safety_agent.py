"""
Safety Guardrails Module
Deterministic pre-inference emergency screening.
"""

from src.state import CareFlowState

EMERGENCY_KEYWORDS = [
    "chest pain", "heart attack", "can't breathe", "cannot breathe", "difficulty breathing",
    "stroke", "suicidal", "severe bleeding", "unconscious", "anaphylaxis",
    "slurred speech", "facial droop", "facial drooping", "sudden numbness", "weakness on one side",
    "loss of bladder control", "loss of bowel control", "groin numbness", "saddle anesthesia",
    "cauda equina", "blue lips", "gasping for air", "throat closing", "coughing up blood",
    "vomiting blood", "crushing chest pain"
]

def run_safety_guardrails(state: CareFlowState) -> dict:
    """
    Scans the patient's message against pre-compiled emergency symptoms.
    If matched, it halts regular booking and triggers emergency routing (911 / 112).
    """
    intake = state.get("intake")
    messages = state.get("messages", [])
    last_text = str(messages[-1].content).lower() if messages else ""
    
    violations = []
    requires_human_review = False
    safety_passed = True
    
    # Emergency keyword screening
    for kw in EMERGENCY_KEYWORDS:
        if kw in last_text:
            violations.append(f"Emergency symptom detected: '{kw}'")
            safety_passed = False
            requires_human_review = True
            break
            
    # Intake emergency status
    if intake and intake.urgency_level == "emergency":
        safety_passed = False
        requires_human_review = True
        violations.append("Intake classified request as Emergency level.")

    # Require clinician review for scheduled bookings
    if state.get("tool_action") == "schedule_appointment":
        requires_human_review = True

    return {
        "safety_passed": safety_passed,
        "safety_violations": violations,
        "requires_human_review": requires_human_review
    }
