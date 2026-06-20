"""Pydantic models for the MSL Intelligence module."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class MSLDebriefRequest(BaseModel):
    msl_name: str = "Anonymous MSL"
    msl_region: Optional[str] = None
    transcript: Optional[str] = None


class InsightCreate(BaseModel):
    msl_name: str
    msl_region: Optional[str] = None
    kol_name: Optional[str] = None
    kol_institution: Optional[str] = None
    kol_specialty: Optional[str] = None
    drug_name: Optional[str] = None
    indication: Optional[str] = None
    insight_type: str
    description: str
    confidence: str
    urgency: str
    routing_target: Optional[str] = None
    kol_sentiment: Optional[str] = None
    full_transcript: Optional[str] = None
    debrief_summary: Optional[str] = None


class InsightResponse(BaseModel):
    id: str
    created_at: datetime
    msl_name: str
    drug_name: Optional[str] = None
    insight_type: str
    description: str
    confidence: str
    urgency: str
    routing_target: Optional[str] = None
    status: str


class MSLDebriefResponse(BaseModel):
    success: bool
    transcript: str
    insights_extracted: int
    insights: List[dict]
    debrief_summary: str
    message: str
