"""PharmaBridge FastAPI application entry point.

Wires together:
  - Core voice pipeline: /api/transcribe, /api/speak
  - MSL Intelligence:    /api/msl/*
  - Patient Companion:   /api/patient/*
  - Bridge Layer:        /api/bridge/*
"""

# Use the Windows / OS native certificate store for TLS verification.
# This must run BEFORE any module that creates an SSL context (httpx,
# anthropic, supabase, elevenlabs, …) — required on corporate networks
# where outbound HTTPS is SSL-inspected with an internal root CA that
# is not in the public `certifi` bundle.
import truststore

truststore.inject_into_ssl()

import os

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from routes import bridge_routes, msl_routes, patient_routes
from services.transcription import get_stt_provider_info, transcribe_audio
from services.tts import text_to_speech

load_dotenv()

app = FastAPI(
    title="PharmaBridge API",
    description="Autonomous Pharma Intelligence Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv(
        "CORS_ORIGINS", "http://localhost:5173"
    ).split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(msl_routes.router, prefix="/api/msl", tags=["MSL Intelligence"])
app.include_router(
    patient_routes.router, prefix="/api/patient", tags=["Patient Companion"]
)
app.include_router(
    bridge_routes.router, prefix="/api/bridge", tags=["Bridge Layer"]
)


@app.get("/")
async def root():
    return {
        "message": "PharmaBridge API is running",
        "version": "1.0.0",
        "modules": [
            "MSL Field Intelligence",
            "Patient Adherence Companion",
            "Bridge Layer",
        ],
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "stt": get_stt_provider_info()}


@app.post("/api/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    """Receives an audio file and returns its transcript.

    Used by both MSL debrief and patient companion.
    """
    audio_bytes = await audio.read()

    if len(audio_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty audio file received")

    result = await transcribe_audio(audio_bytes, audio.filename or "audio.webm")

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {result.get('error', 'Unknown error')}",
        )

    return {
        "transcript": result["transcript"],
        "character_count": len(result["transcript"]),
        "provider": result.get("provider"),
    }


@app.post("/api/speak")
async def speak(request: dict):
    """Converts text to speech and returns base64 audio.

    Used by the patient companion.
    """
    text = (request or {}).get("text", "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    result = await text_to_speech(text)
    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Text-to-speech failed"),
        )

    return result
