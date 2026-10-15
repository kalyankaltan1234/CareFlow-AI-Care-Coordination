"""
RAG Clinical Knowledge Retrieval Module

Retrieves evidence-based clinical protocols, safe OTC medication limits,
and dietary guidelines for grounding agent responses.
Features:
1. Singleton cached ChromaDB vector collection to avoid 200ms cold-start latency.
2. Graceful offline fallback: if vector embeddings are unavailable or offline,
   we fall back to keyword and token overlap scoring without crashing.
"""

import os
import re
from typing import List, Dict, Any
from src.state import CareFlowState

# Curated outpatient clinical protocols for acute & chronic conditions
KNOWLEDGE_DOCUMENTS = [
    {
        "id": "doc_headache",
        "topic": "Neurology & Headache / Migraine Protocol",
        "keywords": ["headache", "migraine", "head", "throbbing", "tension", "neurology", "sharma"],
        "content": "For tension headaches or migraines: rest in a quiet, dark room; apply cold or warm compresses to the forehead or neck; ensure adequate hydration. Maintain a 7-day headache diary noting onset time, severity, and triggers. If headaches are accompanied by sudden visual disturbance, neck stiffness, high fever, or severe sudden onset ('thunderclap'), immediate emergency care is required.",
        "instructions": [
            "Rest in a dimly lit, quiet environment to reduce sensory overload.",
            "Stay well hydrated — drink at least 500ml of water or electrolyte fluid.",
            "Apply a cold gel pack or cool cloth across the forehead or base of the neck for 15-20 minutes.",
            "Keep a symptom log: record duration, intensity (1-10), and potential triggers (caffeine, screen time, lack of sleep)."
        ],
        "specialist": "Dr. Sharma (Neurology)",
        "urgent_warning": "Seek immediate ER care if headache is sudden and explosive, or accompanied by neck stiffness, fever, or confusion."
    },
    {
        "id": "doc_fever",
        "topic": "General Medicine & Fever / Infection Protocol",
        "keywords": ["fever", "temperature", "chills", "flu", "cough", "cold", "body ache", "infection"],
        "content": "For mild to moderate fever: rest, drink plenty of clear fluids (water, broth, herbal tea), and wear light clothing. Monitor body temperature every 4-6 hours. Avoid strenuous activity. Seek medical attention if fever exceeds 103°F (39.4°C), lasts more than 3 consecutive days, or is accompanied by rash or breathing difficulty.",
        "instructions": [
            "Measure and record temperature every 4 hours using a digital thermometer.",
            "Increase fluid intake (minimum 2.5 to 3 liters daily) to prevent dehydration.",
            "Get adequate bed rest; avoid physical exertion.",
            "Take lukewarm sponge baths if feeling uncomfortable. Do not use cold water or ice."
        ],
        "specialist": "Dr. Sneha Reddy (General Medicine)",
        "urgent_warning": "Consult a doctor immediately if fever exceeds 103°F, persists past 72 hours, or causes shortness of breath."
    },
    {
        "id": "doc_stomach",
        "topic": "Gastroenterology & Abdominal Discomfort",
        "keywords": ["stomach", "abdomen", "nausea", "vomiting", "cramps", "digestion", "acid"],
        "content": "For non-acute stomach discomfort: sip clear fluids slowly; follow the BRAT diet (bananas, rice, applesauce, toast); avoid dairy, caffeine, and spicy or greasy foods. Avoid taking NSAIDs (like ibuprofen or aspirin) on an empty stomach.",
        "instructions": [
            "Sip clear broths, oral rehydration solutions, or water in small sips.",
            "Avoid spicy, oily, fatty foods, dairy, and alcohol for 24-48 hours.",
            "Do not take aspirin or ibuprofen without food, as they can irritate the stomach lining.",
            "Rest in an elevated position if experiencing acid reflux or heartburn."
        ],
        "specialist": "Dr. Sandeep Singhania (Gastroenterology)",
        "urgent_warning": "Go to the ER if you experience severe localized abdominal pain, persistent vomiting, or black/bloody stools."
    },
    {
        "id": "doc_cardio",
        "topic": "Cardiology Consultation & Heart Health Policy",
        "keywords": ["heart", "cardio", "palpitation", "blood pressure", "hypertension", "mehta"],
        "content": "Patients visiting Cardiology should bring recent blood pressure logs (taken morning and evening for 7 days) and a complete list of current medications and dosages. Routine resting ECGs are conducted 15 minutes before doctor evaluation.",
        "instructions": [
            "Log your blood pressure twice daily (morning and evening) in a calm seated position.",
            "Bring your physical prescription bottles or medication list to the clinic.",
            "Arrive 15 minutes early for scheduled pre-consultation vitals and ECG."
        ],
        "specialist": "Dr. Mehta (Cardiology)",
        "urgent_warning": "Chest pain, radiating pain to the jaw/left arm, or sudden breathlessness are medical emergencies — dial 911 / 112 immediately."
    },
    {
        "id": "doc_ortho",
        "topic": "Orthopedics & Spine / Musculoskeletal Protocol",
        "keywords": ["back", "backpain", "spine", "joint", "orthopedics", "sciatica", "neck", "knee", "bone", "muscle", "pain", "lumbago", "strain", "disc", "kapoor"],
        "content": "For acute lower back pain, spinal stiffness, and musculoskeletal strain: avoid prolonged complete bed rest beyond 48 hours; apply alternating ice (acute phase) and heat therapy; engage in gentle walking and lumbar stabilization. Maintain spinal ergonomics and avoid heavy lifting. If accompanied by bowel/bladder numbness or progressive leg weakness (cauda equina syndrome), emergency surgical evaluation is required.",
        "instructions": [
            "Apply cold ice packs for 15-20 minutes every 4 hours for the first 48 hours; switch to moist heat thereafter.",
            "Avoid prolonged bed rest; gentle walking prevents spinal muscle deconditioning.",
            "Use ergonomic lumbar support while seated and sleep on a firm supportive mattress with a knee pillow.",
            "Consult an orthopedic specialist if pain radiates past the knee or is accompanied by numbness or weakness."
        ],
        "specialist": "Dr. Sanjay Kapoor (Orthopedics & Spine Care)",
        "urgent_warning": "Seek immediate ER care if back pain is accompanied by loss of bowel/bladder control or sudden groin numbness."
    },
    {
        "id": "doc_pulmo",
        "topic": "Pulmonology & Respiratory Care Protocol",
        "keywords": ["cough", "lung", "chest", "breath", "respiratory", "asthma", "bronchitis", "pneumonia", "wheezing", "covid", "akhtar"],
        "content": "For respiratory symptoms, persistent cough, or bronchospasm: practice warm steam inhalations twice daily, stay hydrated with warm fluids, and sleep with head elevated. Avoid smoke, cold dry drafts, and environmental allergens. Monitor pulse oximetry (SpO2) at rest.",
        "instructions": [
            "Inhale steam for 10 minutes twice daily to loosen pulmonary secretions.",
            "Monitor oxygen saturation (SpO2); maintain above 94% on room air.",
            "Take prescribed bronchodilators or expectorants as directed; do not stop maintenance inhalers."
        ],
        "specialist": "Dr. Farhan Akhtar (Pulmonology & Chest Medicine)",
        "urgent_warning": "Shortness of breath at rest, chest pain, or SpO2 dropping below 93% requires urgent emergency room care."
    },
    {
        "id": "doc_infectious",
        "topic": "Infectious Disease & Viral Care Protocol",
        "keywords": ["virus", "viral", "infection", "zika", "dengue", "malaria", "typhoid", "chikungunya", "chickenpox", "flu", "norovirus", "swamy"],
        "content": "For communicable viral or bacterial illnesses: prioritize intensive hydration with oral rehydration solutions (ORS) and bed rest in a well-ventilated space. Monitor body temperature logs every 4 hours. Do not initiate unprescribed antibiotics for viral illnesses.",
        "instructions": [
            "Drink at least 2.5 to 3 liters of fluids (ORS, coconut water, clear broths) daily.",
            "Isolate in a private room to break the transmission chain to household members.",
            "Use paracetamol for fever control; avoid aspirin or ibuprofen if Dengue or chickenpox cannot be excluded."
        ],
        "specialist": "Dr. Arvind Swamy (Infectious Diseases)",
        "urgent_warning": "High fever unresponsive to antipyretics, bleeding from gums/skin, or sudden confusion requires immediate hospitalization."
    },
    {
        "id": "doc_reschedule",
        "topic": "Clinic Appointments & Rescheduling Policy",
        "keywords": ["reschedule", "cancel", "timing", "hours", "change appointment", "fee"],
        "content": "CareFlow allows appointment modifications or cancellations up to 24 hours prior to the slot without charge. Urgent changes within 24 hours are coordinated directly with our on-duty triage nurse.",
        "instructions": [
            "Provide your Booking ID (e.g. BK-1001) to reschedule or cancel.",
            "Select an alternative open slot from our Doctor Directory tab.",
            "Same-day modifications require confirmation by the Care Coordinator."
        ],
        "specialist": "Hospital Care Coordination Desk",
        "urgent_warning": None
    },
    {
        "id": "doc_emergency",
        "topic": "Emergency Red Flags & Immediate Escalation",
        "keywords": ["chest pain", "heart attack", "breathe", "stroke", "bleeding", "unconscious"],
        "content": "Life-threatening emergencies cannot be managed via online coordination. Emergency medical services (911 / 112) must be contacted immediately.",
        "instructions": [
            "Stop all physical activity immediately and sit or lie down in a safe position.",
            "Call emergency services (911 in US / 112 in India/Europe) or have someone drive you to the nearest ER.",
            "Do not attempt to drive yourself."
        ],
        "specialist": "Emergency Medical Services (EMS)",
        "urgent_warning": "ACTIVE MEDICAL EMERGENCY: Seek immediate hospital care."
    }
]

# Singleton collection cache: avoids re-initializing ChromaDB on every request
_CHROMA_COLLECTION = None

def get_chroma_collection():
    """
    Returns cached ChromaDB collection if local ONNX weights exist.
    Avoids slow network calls on startup.
    """
    global _CHROMA_COLLECTION
    if _CHROMA_COLLECTION is not None:
        return _CHROMA_COLLECTION

    try:
        onnx_file = os.path.expanduser("~/.cache/chroma/onnx_models/all-MiniLM-L6-v2/onnx/model.onnx")
        if os.path.exists(onnx_file):
            import chromadb
            client = chromadb.EphemeralClient()
            col = client.get_or_create_collection("hospital_guidelines")
            if col.count() == 0:
                col.add(
                    documents=[f"[{doc['topic']}] {doc['content']}" for doc in KNOWLEDGE_DOCUMENTS],
                    ids=[doc["id"] for doc in KNOWLEDGE_DOCUMENTS],
                    metadatas=[{"topic": doc["topic"], "specialist": doc.get("specialist", "")} for doc in KNOWLEDGE_DOCUMENTS]
                )
            _CHROMA_COLLECTION = col
            return _CHROMA_COLLECTION
    except Exception:
        pass
    return None

def run_rag_agent(state: CareFlowState) -> dict:
    """
    Retrieves matching clinical guideline passages using vector search
    with a keyword scoring fallback.
    """
    messages = state.get("messages", [])
    intake = state.get("intake")
    
    last_text = ""
    if messages:
        last_text = str(messages[-1].content).lower()
        
    symptoms_text = " ".join(intake.symptoms).lower() if intake and intake.symptoms else ""
    intent_str = intake.intent if intake and intake.intent else ""
    specialty_str = intake.requested_specialty if intake and intake.requested_specialty else ""
    query_text = f"{last_text} {symptoms_text} {intent_str} {specialty_str}".strip().lower()

    retrieved: List[str] = []

    # Vector retrieval
    col = get_chroma_collection()
    if col is not None:
        try:
            results = col.query(query_texts=[query_text], n_results=2)
            if results and results.get("documents") and results["documents"][0]:
                retrieved = results["documents"][0]
        except Exception:
            pass

    # Keyword and token matching fallback
    if not retrieved:
        scored_docs = []
        for doc in KNOWLEDGE_DOCUMENTS:
            score = 0
            for kw in doc["keywords"]:
                if kw in query_text:
                    score += 2
            for word in re.findall(r'\b\w{4,}\b', query_text):
                if word in doc["content"].lower():
                    score += 1
                    
            if score > 0:
                scored_docs.append((score, doc))
                
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        
        if scored_docs:
            for _, doc in scored_docs[:2]:
                retrieved.append(f"[{doc['topic']}] {doc['content']}")
        else:
            retrieved.append(f"[{KNOWLEDGE_DOCUMENTS[0]['topic']}] {KNOWLEDGE_DOCUMENTS[0]['content']}")
            retrieved.append(f"[{KNOWLEDGE_DOCUMENTS[4]['topic']}] {KNOWLEDGE_DOCUMENTS[4]['content']}")
            
    return {"retrieved_knowledge": retrieved}
