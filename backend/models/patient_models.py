"""Pydantic models for the Patient Adherence Companion module."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ConversationTurn(BaseModel):
    role: str
    content: str


class PatientChatRequest(BaseModel):
    patient_id: str
    message: str
    conversation_history: List[ConversationTurn] = []
    include_audio: bool = True


class PatientChatResponse(BaseModel):
    success: bool
    response_text: str
    detected_barrier: Optional[str] = None
    barrier_confidence: Optional[str] = None
    alert_triggered: bool = False
    audio: Optional[dict] = None


class StartSessionRequest(BaseModel):
    patient_id: str


class PatientProfile(BaseModel):
    id: str
    patient_name: str
    patient_code: str
    condition: Optional[str] = None
    drug_name: str
    adherence_rate: float
    primary_barrier: str
    barrier_confidence: str
    last_checkin_at: Optional[datetime] = None
