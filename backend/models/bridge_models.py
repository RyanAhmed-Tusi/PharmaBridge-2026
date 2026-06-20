"""Pydantic models for the Bridge Layer module."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ConvergentSignalDetection(BaseModel):
    convergent_signal_detected: bool
    drug_name: Optional[str] = None
    signal_type: Optional[str] = None
    confidence: Optional[str] = None
    velocity: Optional[str] = None
    signal_summary: Optional[str] = None
    recommended_actions: List[str] = []
    reasoning: Optional[str] = None


class ConvergentSignal(BaseModel):
    id: str
    created_at: datetime
    drug_name: str
    signal_type: str
    confidence: str
    velocity: Optional[str] = None
    msl_evidence: str
    patient_evidence: str
    msl_insight_count: int = 0
    patient_count: int = 0
    signal_summary: str
    recommended_actions: List[str] = []
    status: str = "Active"


class BridgeScanResponse(BaseModel):
    success: bool
    drugs_analyzed: int
    new_signals_detected: int
    signals: List[dict]
    message: str
