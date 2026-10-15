"""
LangGraph Multi-Agent Orchestrator

Coordinates the dataflow across our 5 agents:
1. Intake Agent: extracts symptoms and detects user intent.
2. RAG Knowledge Retriever & Hospital Tool Agent: executed concurrently.
3. Safety Guardrails Agent: inspects for life-threatening emergency signs.
4. Response Synthesizer: formats actionable patient instructions and appointment tokens.
"""

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AIMessage
from src.state import CareFlowState
from src.llm_manager import get_active_llm
from src.agents.intake_agent import run_intake_agent
from src.agents.rag_agent import run_rag_agent
from src.agents.tool_agent import run_tool_agent
from src.agents.safety_agent import run_safety_guardrails
from src.knowledge.disease_db import match_disease, format_disease_response

def aggregate_and_respond(state: CareFlowState) -> dict:
    """
    Combines outputs from intake, RAG guidelines, and scheduling tools
    into a structured patient guidance summary.
    """
    intake = state.get("intake")
    knowledge = state.get("retrieved_knowledge", [])
    tool_result = state.get("tool_result")
    safety_passed = state.get("safety_passed", True)
    violations = state.get("safety_violations", [])
    patient_name = state.get("patient_name") or "Patient"
    patient_age = state.get("patient_age")
    patient_place = state.get("patient_place")
    reported_disease = state.get("reported_disease")
    
    messages = state.get("messages", [])
    last_user_query = str(messages[-1].content) if messages else ""
    
    # Urgent emergency override
    if not safety_passed:
        emergency_msg = (
            "🚨 **URGENT MEDICAL NOTICE: Active Emergency Symptoms Detected**\n\n"
            "CareFlow cannot safely triage acute medical emergencies through online chat. "
            "Please **immediately call 911 / 112** or proceed to your nearest hospital Emergency Room.\n\n"
            "🛡️ **Immediate Safety Instructions**:\n"
            "• Stop all physical activity and sit or lie down in a safe, comfortable position.\n"
            "• Have someone nearby stay with you.\n"
            "• Do NOT drive yourself to the hospital.\n\n"
            f"**Triage Alerts**: {', '.join(violations)}"
        )
        return {"final_response": emergency_msg, "messages": [AIMessage(content=emergency_msg)]}

    # If user provided API keys, synthesize using live LLM (OpenAI or Gemini)
    llm = get_active_llm()
    if llm:
        try:
            demo_str = f"Patient: {patient_name}"
            if patient_age: 
                demo_str += f", Age: {patient_age}"
            if patient_place: 
                demo_str += f", Location: {patient_place}"
            if reported_disease: 
                demo_str += f", Reported Condition: {reported_disease}"

            prompt = (
                f"You are CareFlow, an empathetic, highly structured AI Care Coordination Assistant for Project ID: 11.\n"
                f"{demo_str}\n"
                f"User Question/Message: \"{last_user_query}\"\n\n"
                f"Intake Assessment:\n"
                f"- Primary Intent: {intake.intent if intake else 'General'}\n"
                f"- Urgency: {intake.urgency_level if intake else 'Medium'}\n"
                f"- Extracted Symptoms: {', '.join(intake.symptoms) if intake and intake.symptoms else 'None'}\n"
                f"- Specialty: {intake.requested_specialty or 'General Medicine'}\n\n"
                f"Retrieved Clinical Guidance:\n" + "\n".join(knowledge) + "\n\n"
                f"Hospital Tool Booking Result: {tool_result}\n\n"
                "CRITICAL INSTRUCTIONS FOR YOUR RESPONSE:\n"
                "You MUST structure your response with these exact markdown sections:\n"
                "1. Brief empathetic opening addressing the disease/symptom for this patient\n"
                "2. 🔍 **Common Symptoms & Clinical Signs** (bulleted list)\n"
                "3. 🛡️ **Key Precautions & Immediate At-Home Care** (actionable step-by-step guidance, including age-appropriate precautions)\n"
                "4. 💊 **Medications You Can Use (Supportive & First-Line Guidance)** (list common safe OTC/supportive medicines, generic names, dosage instructions, and critical medication safety warnings)\n"
                "5. 🚫 **What to Avoid (Diet, Habits & Contraindicated Medicines)** (clear list of foods or drugs to avoid)\n"
                "6. 🚨 **Red-Flag Warnings (Seek Emergency Hospital Care If)** (critical threshold signs)\n"
                "7. 📅 **Recommended Specialist & Next Steps** (Recommend the appropriate medical department and consulting doctor dynamically based on the patient's condition)\n"
                "If an appointment was booked, include the booking ID and time. Keep it clean and highly structured."
            )
            response = llm.invoke(prompt)
            return {"final_response": response.content, "messages": [AIMessage(content=response.content)]}
        except Exception as e:
            print(f"[Graph Synthesizer] Online LLM call failed: {e}. Using deterministic clinical engine instead.")

    # Offline clinical response engine
    if tool_result and "booking" in tool_result:
        b = tool_result["booking"]
        doc_name = tool_result.get("doctor_name", "Specialist")
        spec = tool_result.get("specialty", "General Medicine")
        lines = [
            f"Hello {patient_name}, I have coordinated your appointment request:\n",
            f"✅ **Appointment Provisionally Reserved**:",
            f"• **Doctor**: {doc_name} ({spec})",
            f"• **Reserved Slot**: {b.get('slot_time')}",
            f"• **Booking ID**: `{b.get('booking_id')}`",
            f"• **Status**: {b.get('status')}\n",
            "📋 **Pre-Appointment Instructions**:"
        ]
        if "neurolog" in spec.lower():
            lines.append("• Maintain a 7-day headache diary noting frequency, pain triggers, and sleep patterns.")
            lines.append("• Bring any previous brain scans, MRIs, or neurological reports.")
        elif "cardio" in spec.lower():
            lines.append("• Log your resting blood pressure twice daily for the next 7 days.")
            lines.append("• Arrive 15 minutes early for your baseline resting ECG.")
        else:
            lines.append("• Bring a list of current daily medications and past health records.")
            lines.append("• Note when your symptoms first began and any medication taken.")
        lines.append("\n⚠️ *Note: Your care coordinator has been alerted to review and confirm this slot on the Clinician Desk.*")
        final_text = "\n".join(lines)
        return {"final_response": final_text, "messages": [AIMessage(content=final_text)]}

    # Disease condition matching
    search_term = last_user_query
    matched_disease = match_disease(search_term, reported_disease=reported_disease)
    if not matched_disease and reported_disease:
        matched_disease = match_disease(reported_disease)
        
    if matched_disease:
        final_text = format_disease_response(matched_disease, patient_name, patient_age, patient_place)
        return {"final_response": final_text, "messages": [AIMessage(content=final_text)]}

    # General clinic inquiry fallback
    lines = [
        f"Hello {patient_name}, thank you for contacting CareFlow.\n",
        "📋 **Care Coordination Assistance**:",
        "Please describe the symptoms or condition you need help with (for example: fever, migraine, dengue, back pain, cough, or diabetes).",
        "I can help provide:",
        "• 🔍 Common symptoms & expected progression",
        "• 🛡️ Precautions & supportive home care",
        "• 🚫 Contraindications (medicines or foods to avoid)",
        "• 🚨 Red-flag signs needing urgent ER attention",
        "• 📅 Scheduling with the right hospital department\n"
    ]
    if knowledge:
        lines.append("📚 **Relevant Clinical Guidelines**:")
        for doc in knowledge[:2]:
            lines.append(f"• {doc}")
            
    final_text = "\n".join(lines)
    return {"final_response": final_text, "messages": [AIMessage(content=final_text)]}

def build_careflow_graph():
    """Builds and compiles the state graph."""
    builder = StateGraph(CareFlowState)
    
    # Register our agents as graph nodes
    builder.add_node("intake_agent", run_intake_agent)
    builder.add_node("rag_agent", run_rag_agent)
    builder.add_node("tool_agent", run_tool_agent)
    builder.add_node("safety_guardrails", run_safety_guardrails)
    builder.add_node("response_synthesizer", aggregate_and_respond)
    
    # Define directed edges
    builder.add_edge(START, "intake_agent")
    builder.add_edge("intake_agent", "rag_agent")
    builder.add_edge("intake_agent", "tool_agent")
    builder.add_edge("rag_agent", "safety_guardrails")
    builder.add_edge("tool_agent", "safety_guardrails")
    builder.add_edge("safety_guardrails", "response_synthesizer")
    builder.add_edge("response_synthesizer", END)
    
    return builder.compile()

# Module-level compiled instance for direct import
careflow_graph = build_careflow_graph()
