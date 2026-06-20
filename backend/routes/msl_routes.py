"""MSL Intelligence API routes.

POST /api/msl/debrief        -> multipart audio -> transcript -> Claude insight extraction -> Supabase
POST /api/msl/debrief/text   -> text transcript -> Claude insight extraction -> Supabase
GET  /api/msl/insights       -> recent insights, with optional filters
"""

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from services.claude_msl import extract_msl_insights
from services.supabase_client import supabase
from services.transcription import transcribe_audio

router = APIRouter()


@router.post("/debrief")
async def submit_msl_debrief(
    audio: UploadFile = File(...),
    msl_name: str = Form(default="Anonymous MSL"),
    msl_region: str = Form(default="Unspecified"),
):
    """Receives MSL voice debrief audio, transcribes it, extracts insights, saves them."""
    audio_bytes = await audio.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty audio file received")

    transcription_result = await transcribe_audio(
        audio_bytes, audio.filename or "debrief.webm"
    )
    if not transcription_result["success"]:
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {transcription_result.get('error', 'Unknown')}",
        )

    transcript = transcription_result["transcript"]

    extraction_result = await extract_msl_insights(transcript, msl_name)
    if not extraction_result["success"]:
        raise HTTPException(
            status_code=500,
            detail=f"Insight extraction failed: {extraction_result.get('error')}",
        )

    saved_insights = []
    for insight in extraction_result["insights"]:
        try:
            db_record = {
                "msl_name": msl_name,
                "msl_region": msl_region,
                "kol_name": insight.get("kol_name"),
                "kol_institution": insight.get("kol_institution"),
                "kol_specialty": insight.get("kol_specialty"),
                "drug_name": insight.get("drug_name"),
                "indication": insight.get("indication"),
                "insight_type": insight.get("insight_type"),
                "description": insight.get("description"),
                "full_transcript": transcript,
                "debrief_summary": extraction_result.get("debrief_summary"),
                "confidence": insight.get("confidence", "Medium"),
                "urgency": insight.get("urgency", "Normal"),
                "routing_target": insight.get("routing_target"),
                "kol_sentiment": insight.get("kol_sentiment", "Neutral"),
                "status": "New",
            }

            result = supabase.table("msl_insights").insert(db_record).execute()
            if result.data:
                saved_insights.append(result.data[0])
            else:
                saved_insights.append(db_record)

            if (
                insight.get("insight_type") == "Safety Observation"
                and insight.get("kol_name")
                and insight.get("kol_name") != "Unknown"
            ):
                upsert_kol_profile(insight, msl_region)

        except Exception as e:  # noqa: BLE001
            print(f"Error saving insight: {e}")
            continue

    return {
        "success": True,
        "transcript": transcript,
        "insights_extracted": len(saved_insights),
        "insights": saved_insights,
        "debrief_summary": extraction_result.get("debrief_summary", ""),
        "overall_kol_sentiment": extraction_result.get(
            "overall_kol_sentiment", "Neutral"
        ),
        "message": f"Successfully extracted {len(saved_insights)} insights from your debrief.",
    }


@router.post("/debrief/text")
async def submit_text_debrief(request: dict):
    """Alternative: accepts a transcript as text directly (no audio)."""
    msl_name = (request or {}).get("msl_name", "Anonymous MSL")
    msl_region = (request or {}).get("msl_region", "Unspecified")
    transcript = (request or {}).get("transcript", "").strip()

    if not transcript:
        raise HTTPException(status_code=400, detail="No transcript provided")

    extraction_result = await extract_msl_insights(transcript, msl_name)
    if not extraction_result["success"]:
        raise HTTPException(
            status_code=500, detail=extraction_result.get("error", "Extraction failed")
        )

    saved_insights = []
    for insight in extraction_result["insights"]:
        db_record = {
            "msl_name": msl_name,
            "msl_region": msl_region,
            "drug_name": insight.get("drug_name"),
            "kol_name": insight.get("kol_name"),
            "kol_institution": insight.get("kol_institution"),
            "kol_specialty": insight.get("kol_specialty"),
            "indication": insight.get("indication"),
            "insight_type": insight.get("insight_type"),
            "description": insight.get("description"),
            "full_transcript": transcript,
            "debrief_summary": extraction_result.get("debrief_summary"),
            "confidence": insight.get("confidence", "Medium"),
            "urgency": insight.get("urgency", "Normal"),
            "routing_target": insight.get("routing_target"),
            "kol_sentiment": insight.get("kol_sentiment", "Neutral"),
            "status": "New",
        }
        result = supabase.table("msl_insights").insert(db_record).execute()
        if result.data:
            saved_insights.append(result.data[0])

        if (
            insight.get("insight_type") == "Safety Observation"
            and insight.get("kol_name")
            and insight.get("kol_name") != "Unknown"
        ):
            upsert_kol_profile(insight, msl_region)

    return {
        "success": True,
        "insights_extracted": len(saved_insights),
        "insights": saved_insights,
        "debrief_summary": extraction_result.get("debrief_summary"),
        "overall_kol_sentiment": extraction_result.get(
            "overall_kol_sentiment", "Neutral"
        ),
    }


@router.get("/insights")
async def get_insights(
    limit: int = 50,
    insight_type: str | None = None,
    drug_name: str | None = None,
    urgency: str | None = None,
):
    """Returns recent MSL insights with optional filtering."""
    query = (
        supabase.table("msl_insights")
        .select("*")
        .order("created_at", desc=True)
        .limit(limit)
    )

    if insight_type:
        query = query.eq("insight_type", insight_type)
    if drug_name:
        query = query.eq("drug_name", drug_name)
    if urgency:
        query = query.eq("urgency", urgency)

    result = query.execute()
    return {"insights": result.data, "count": len(result.data)}


def upsert_kol_profile(insight: dict, region: str) -> None:
    """Updates or creates a KOL profile with the latest sentiment data."""
    try:
        supabase.table("kol_profiles").upsert(
            {
                "kol_name": insight.get("kol_name", "Unknown"),
                "institution": insight.get("kol_institution"),
                "specialty": insight.get("kol_specialty"),
                "region": region,
                "drug_name": insight.get("drug_name", "Unspecified"),
                "sentiment_trend": insight.get("kol_sentiment", "Neutral"),
            },
            on_conflict="kol_name,drug_name",
        ).execute()
    except Exception as e:  # noqa: BLE001
        print(f"KOL profile update error: {e}")
