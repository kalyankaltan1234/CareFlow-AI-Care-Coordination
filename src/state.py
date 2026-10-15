from typing import Annotated, List, Optional, Dict, Any, Literal
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
import operator

class IntakeOutput(BaseModel):
    """Structured extraction produced by the Intake Agent."""
    intent: Literal["appointment_booking", "general_inquiry", "symptom_triage", "medication_query", "unknown"] = Field(
        description="The primary intent of the user request"
    )
    urgency_level: Literal["low", "medium", "high", "emergency"] = Field(
        description="Assessed urgency level of the request"
    )
    symptoms: List[str] = Field(default_factory=list, description="Extracted patient symptoms, if any")
    requested_specialty: Optional[str] = Field(None, description="Medical specialty (e.g., Cardiology, Neurology, General Medicine)")
    preferred_date: Optional[str] = Field(None, description="Preferred appointment date or timeframe")
    summary: str = Field(description="A concise 1-sentence summary of what the patient needs")


class CareFlowState(TypedDict):
    """State schema for CareFlow multi-agent orchestration."""
    messages: Annotated[List[BaseMessage], operator.add]
    patient_id: Optional[str]
    patient_name: Optional[str]
    patient_age: Optional[str]
    patient_place: Optional[str]
    reported_disease: Optional[str]
    intake: Optional[IntakeOutput]
    retrieved_knowledge: Optional[List[str]]
    tool_action: Optional[str]
    tool_result: Optional[Dict[str, Any]]
    safety_passed: bool
    safety_violations: List[str]
    requires_human_review: bool
    human_feedback: Optional[str]
    final_response: Optional[str]
