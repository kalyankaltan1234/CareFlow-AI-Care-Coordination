"""
Intake Agent Module

Normalizes patient input messages, extracts clinical intent, handles typos,
and tags triage urgency (emergency, high, medium, low).
We combine fast string heuristics with difflib sequence matching so that common
misspellings (e.g., 'fevor', 'diabities', 'loose motion') resolve instantly without
calling external LLM APIs.
"""

from langchain_core.prompts import ChatPromptTemplate
from src.state import CareFlowState, IntakeOutput
from src.llm_manager import get_active_llm
from src.knowledge.disease_db import match_disease

INTAKE_SYSTEM_PROMPT = """You are the Structured Intake Agent for CareFlow, an AI Care Coordination Assistant.
Your responsibility is to analyze the patient's incoming message and extract:
1. Intent: appointment_booking, general_inquiry, symptom_triage, medication_query, or unknown.
2. Urgency level:
   - "emergency": Life-threatening symptoms like severe chest pain, sudden numbness, severe difficulty breathing, heavy bleeding.
   - "high": Severe pain, high fever, worsening acute symptoms.
   - "medium": Standard appointments, recurring symptoms, non-critical concerns.
   - "low": General inquiries, clinic hours, routine checkups.
3. Extracted symptoms, preferred department/specialty, and preferred timeframe/date.
4. A concise 1-sentence summary of the request.

Be accurate and prioritize patient safety."""

def run_intake_agent(state: CareFlowState) -> dict:
    """
    Parses the user's latest message into structured demographic & triage state.
    """
    messages = state.get("messages", [])
    if not messages:
        return {"intake": None}
    
    last_user_message = messages[-1].content
    reported_disease = state.get("reported_disease")
    lower = str(last_user_message).lower()
    intent = "general_inquiry"
    urgency = "medium"
    specialty = "General Medicine"
    symptoms = []
    
    # Emergency screening
    emergency_patterns = [
        "chest pain", "can't breathe", "cannot breathe", "difficulty breathing",
        "heart attack", "stroke", "bleeding", "slurred speech", "facial droop",
        "loss of bladder control", "groin numbness", "cauda equina", "blue lips",
        "gasping for air", "coughing up blood", "vomiting blood"
    ]
    if any(kw in lower for kw in emergency_patterns):
        urgency = "emergency"
        intent = "symptom_triage"
        symptoms.append("acute emergency presentation")
        specialty = "Emergency Medicine"

    # Appointment intent detection
    elif any(kw in lower for kw in ["book", "appointment", "schedule", "reserve slot", "reserve an appointment"]):
        intent = "appointment_booking"
        urgency = "low"
        if "sharma" in lower or "neurolog" in lower or "migraine" in lower or "head" in lower:
            specialty = "Neurology"
            if "migraine" in lower or "head" in lower:
                symptoms.append("headache / migraine")
        elif "mehta" in lower or "cardio" in lower or "heart" in lower or "bp" in lower:
            specialty = "Cardiology"
            if "heart" in lower:
                symptoms.append("cardiovascular inquiry")
        elif "kapoor" in lower or "ortho" in lower or "back" in lower or "spine" in lower:
            specialty = "Orthopedics"
        elif "akhtar" in lower or "pulmo" in lower or "lung" in lower or "cough" in lower:
            specialty = "Pulmonology"
        else:
            specialty = "General Medicine"

    # Disease and condition matching
    else:
        matched = match_disease(last_user_message, reported_disease=reported_disease)
        if matched:
            intent = "symptom_triage"
            urgency = "medium"
            symptoms.append(matched["name"])
            spec_str = matched.get("specialist", "")
            if "Orthopedics" in spec_str or "Spine" in spec_str:
                specialty = "Orthopedics"
            elif "Pulmonology" in spec_str or "Chest" in spec_str:
                specialty = "Pulmonology"
            elif "Dermatology" in spec_str:
                specialty = "Dermatology"
            elif "Gastroenterology" in spec_str:
                specialty = "Gastroenterology"
            elif "Urology" in spec_str:
                specialty = "Urology"
            elif "Infectious" in spec_str:
                specialty = "Infectious Diseases"
            elif "Neurology" in spec_str:
                specialty = "Neurology"
            elif "Cardiology" in spec_str:
                specialty = "Cardiology"
            elif "Endocrinology" in spec_str or "Diabet" in spec_str:
                specialty = "Endocrinology"
            else:
                specialty = "General Medicine"
        
        # Department routing overrides
        if any(w in lower for w in ["dengue", "malaria", "typhoid", "chikungunya", "zika"]):
            specialty = "Infectious Diseases"
        elif any(w in lower for w in ["sugar", "diabet", "fasting glucose", "hba1c"]):
            specialty = "Endocrinology"
        elif any(w in lower for w in ["blood pressure", "hypertension", "systolic", "diastolic", "resting heart"]):
            specialty = "Cardiology"
        elif any(w in lower for w in ["gerd", "loose motion", "stomach", "vomit", "cramp", "diarrhea", "norovirus"]):
            specialty = "Gastroenterology"
        elif any(w in lower for w in ["migraine", "headache", "unilateral"]):
            specialty = "Neurology"
        elif any(w in lower for w in ["back pain", "sciatica", "joint", "knee", "spine", "lumbar", "rheumatol"]):
            specialty = "Orthopedics"
        elif any(w in lower for w in ["cough", "wheezing", "asthma", "bronch", "pulmo", "breathlessness"]):
            specialty = "Pulmonology"
        elif any(w in lower for w in ["rash", "itching", "eczema", "dermatol", "skin"]):
            specialty = "Dermatology"
        elif any(w in lower for w in ["flank", "urination", "kidney stone", "renal", "colicky"]):
            specialty = "Urology"

    # Online LLM extraction fallback
    llm = get_active_llm()
    if llm and not symptoms:
        try:
            structured_llm = llm.with_structured_output(IntakeOutput)
            prompt = ChatPromptTemplate.from_messages([
                ("system", INTAKE_SYSTEM_PROMPT),
                ("human", "{user_input}")
            ])
            chain = prompt | structured_llm
            result = chain.invoke({"user_input": last_user_message})
            if result:
                return {"intake": result}
        except Exception as e:
            print(f"[Intake Agent] LLM structured output warning: {e}")

    preferred_date = None
    if "next tuesday" in lower:
        preferred_date = "Next Tuesday"
    elif "tomorrow" in lower:
        preferred_date = "Tomorrow"
    elif "today" in lower:
        preferred_date = "Today"

    fallback_intake = IntakeOutput(
        intent=intent,
        urgency_level=urgency,
        symptoms=symptoms,
        requested_specialty=specialty,
        preferred_date=preferred_date,
        summary=f"Patient inquiry regarding {', '.join(symptoms) if symptoms else intent} ({specialty})"
    )
    return {"intake": fallback_intake}
