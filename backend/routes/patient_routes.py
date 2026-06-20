"""Patient Adherence Companion API routes.

POST /api/patient/chat                       -> one turn of conversation
POST /api/patient/start-session              -> opening message for today's check-in
GET  /api/patient/patients                   -> all patient profiles
GET  /api/patient/patients/{id}/history      -> full conversation history for a patient
"""

from datetime import date, datetime, timezone

from fastapi import APIRouter, HTTPException

from services.claude_patient import generate_opening_message, patient_chat
from services.supabase_client import supabase
from services.tts import text_to_speech

router = APIRouter()


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_recommended_action(barrier_type: str) -> str:
    """Returns the recommended clinical action for each barrier type."""
    actions = {
        "Cost": "Review patient assistance programs, generic alternatives, and co-pay card eligibility.",
        "Side Effect": "Schedule clinical review of dose timing or alternative formulation. Consider pharmacovigilance report if severe.",
        "Forgetfulness": "Consider medication management app, pill organizer, or simplified dosing schedule.",
        "Belief": "Schedule motivational interview with physician to discuss disease progression risks.",
        "Complexity": "Request medication reconciliation review. Explore regimen simplification.",
        "Access": "Explore mail-order pharmacy, medication delivery services, or 90-day supply options.",
    }
    return actions.get(
        barrier_type, "Review patient's full medication history and barriers."
    )


@router.post("/chat")
async def patient_chat_endpoint(request: dict):
    """Main patient companion chat endpoint.

    Receives a patient message, generates AI response, persists conversation,
    updates barrier profile, and triggers care-team alert when warranted.
    """
    request = request or {}
    patient_id = request.get("patient_id")
    patient_message = (request.get("message") or "").strip()
    conversation_history = request.get("conversation_history") or []
    include_audio = request.get("include_audio", True)

    if not patient_id or not patient_message:
        raise HTTPException(
            status_code=400, detail="patient_id and message are required"
        )

    patient_result = (
        supabase.table("patient_profiles")
        .select("*")
        .eq("id", patient_id)
        .single()
        .execute()
    )
    if not patient_result.data:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient_profile = patient_result.data

    ai_result = await patient_chat(patient_message, conversation_history, patient_profile)

    if not ai_result.get("success", True) and ai_result.get("error"):
        raise HTTPException(status_code=500, detail=ai_result.get("error"))

    response_text = ai_result.get("response_text", "")

    supabase.table("patient_conversations").insert(
        {
            "patient_id": patient_id,
            "role": "patient",
            "message": patient_message,
            "barrier_signal": ai_result.get("detected_barrier"),
            "signal_strength": ai_result.get("barrier_confidence"),
            "session_date": str(date.today()),
        }
    ).execute()

    supabase.table("patient_conversations").insert(
        {
            "patient_id": patient_id,
            "role": "companion",
            "message": response_text,
            "session_date": str(date.today()),
        }
    ).execute()

    update_data = {"last_checkin_at": _utcnow_iso()}

    adherence_today = ai_result.get("adherence_taken_today")
    if adherence_today is True:
        days = (patient_profile.get("consecutive_days_tracked") or 0) + 1
        current_rate = float(patient_profile.get("adherence_rate") or 100)
        new_rate = ((current_rate * (days - 1)) + 100) / days
        update_data["adherence_rate"] = round(new_rate, 2)
        update_data["consecutive_days_tracked"] = days
    elif adherence_today is False:
        days = (patient_profile.get("consecutive_days_tracked") or 0) + 1
        current_rate = float(patient_profile.get("adherence_rate") or 100)
        new_rate = ((current_rate * (days - 1)) + 0) / days
        update_data["adherence_rate"] = round(new_rate, 2)
        update_data["consecutive_days_tracked"] = days

    detected_barrier = ai_result.get("detected_barrier")
    barrier_confidence = ai_result.get("barrier_confidence")
    if detected_barrier and barrier_confidence in ("High", "Medium"):
        update_data["primary_barrier"] = detected_barrier
        update_data["barrier_confidence"] = barrier_confidence
        update_data["barrier_details"] = ai_result.get("barrier_details")
        update_data["barrier_detected_at"] = _utcnow_iso()

    supabase.table("patient_profiles").update(update_data).eq(
        "id", patient_id
    ).execute()

    alert_triggered = bool(ai_result.get("trigger_care_team_alert"))
    if alert_triggered:
        supabase.table("care_team_alerts").insert(
            {
                "patient_id": patient_id,
                "patient_code": patient_profile.get("patient_code"),
                "drug_name": patient_profile.get("drug_name"),
                "alert_type": "Barrier Detected",
                "alert_message": (
                    f"Patient has confirmed {detected_barrier} barrier. "
                    f"{ai_result.get('barrier_details') or ''}"
                ).strip(),
                "barrier_type": detected_barrier,
                "barrier_details": ai_result.get("barrier_details"),
                "recommended_action": get_recommended_action(detected_barrier),
                "status": "Pending",
            }
        ).execute()

    audio_data = None
    if include_audio and response_text:
        audio_result = await text_to_speech(response_text)
        if audio_result.get("success"):
            audio_data = {
                "audio_base64": audio_result.get("audio_base64"),
                "content_type": audio_result.get("content_type"),
            }

    return {
        "success": True,
        "response_text": response_text,
        "detected_barrier": detected_barrier,
        "barrier_confidence": barrier_confidence,
        "alert_triggered": alert_triggered,
        "audio": audio_data,
    }


@router.post("/start-session")
async def start_patient_session(request: dict):
    """Gets the opening message for a new patient check-in session."""
    patient_id = (request or {}).get("patient_id")
    if not patient_id:
        raise HTTPException(status_code=400, detail="patient_id is required")

    patient_result = (
        supabase.table("patient_profiles")
        .select("*")
        .eq("id", patient_id)
        .single()
        .execute()
    )
    if not patient_result.data:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient_profile = patient_result.data
    session_number = (patient_profile.get("consecutive_days_tracked") or 0) + 1

    opening_message = await generate_opening_message(patient_profile, session_number)

    audio_data = None
    audio_result = await text_to_speech(opening_message)
    if audio_result.get("success"):
        audio_data = {
            "audio_base64": audio_result.get("audio_base64"),
            "content_type": "audio/mpeg",
        }

    return {
        "opening_message": opening_message,
        "patient_name": patient_profile.get("patient_name"),
        "session_number": session_number,
        "audio": audio_data,
    }


@router.get("/patients")
async def get_all_patients():
    """Returns all patient profiles for the dashboard."""
    result = (
        supabase.table("patient_profiles")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return {"patients": result.data or [], "count": len(result.data or [])}


@router.get("/patients/{patient_id}/history")
async def get_patient_history(patient_id: str):
    """Returns conversation history for a specific patient (chronological)."""
    result = (
        supabase.table("patient_conversations")
        .select("*")
        .eq("patient_id", patient_id)
        .order("created_at", desc=False)
        .execute()
    )
    return {"conversations": result.data or []}
