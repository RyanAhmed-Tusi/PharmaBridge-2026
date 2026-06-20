"""Claude-powered MSL insight extraction service.

Takes a raw MSL debrief transcript and returns a structured set of insights
(safety observations, label questions, competitive intel, etc.) ready for DB
persistence.
"""

import json
import os

import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

MSL_MODEL = "claude-sonnet-4-6"


MSL_EXTRACTION_PROMPT = """You are PharmaBridge's MSL Intelligence Extraction Engine.
You are analyzing a voice debrief transcript from a Medical Science Liaison (MSL) after a KOL (Key Opinion Leader) meeting.

Your job is to extract every distinct insight from this transcript and return structured data.

INSIGHT TYPES (classify each insight as exactly one of these):
- "Safety Observation": Any mention of adverse events, side effects, patient safety concerns
- "Label Question": Questions about dosing, indications, label claims, contraindications
- "Competitive Intel": Mentions of competitor drugs, rival trial data, comparative effectiveness
- "Unmet Need": Clinical gaps, patient populations not served, conditions without good treatment options
- "Evidence Gap": Missing data, requested studies, questions the MSL couldn't answer
- "Advocacy": Positive endorsement, willingness to speak at events, recommend prescribing
- "Other": Doesn't fit above categories

CONFIDENCE SCORING:
- "High": The insight is explicit and unambiguous in the transcript
- "Medium": The insight is implied or partially mentioned
- "Low": Uncertain, would need clarification

URGENCY:
- "Urgent": Safety observations or regulatory matters - must reach the right team within hours
- "Normal": Standard intelligence, route within 24-48 hours
- "Low": Background information, can wait for weekly report

ROUTING TARGETS:
- Safety Observation -> "Pharmacovigilance"
- Label Question -> "Medical Affairs"
- Competitive Intel -> "Commercial"
- Evidence Gap -> "Medical Affairs" or "R&D"
- Advocacy -> "Medical Affairs"
- Unmet Need -> "R&D"

KOL SENTIMENT toward the specific drug mentioned:
- "Positive": Enthusiastic, recommending, favorable
- "Neutral": Factual, no strong opinion
- "Skeptical": Questioning, doubting, comparing unfavorably
- "Negative": Critical, not recommending, concerned

Return ONLY valid JSON, no markdown, no explanation. Use this exact structure:

{
  "insights": [
    {
      "insight_type": "Safety Observation",
      "drug_name": "Drug name or 'Unspecified'",
      "indication": "Disease/condition or 'Unspecified'",
      "kol_name": "Name or 'Unknown'",
      "kol_institution": "Institution or 'Unknown'",
      "kol_specialty": "Specialty or 'Unknown'",
      "description": "Clear, concise description of the insight (2-3 sentences)",
      "confidence": "High",
      "urgency": "Normal",
      "routing_target": "Medical Affairs",
      "kol_sentiment": "Neutral"
    }
  ],
  "overall_kol_sentiment": "Neutral",
  "debrief_summary": "2-3 sentence summary of the entire meeting",
  "msl_region": "Region if mentioned, else 'Unspecified'"
}

TRANSCRIPT TO ANALYZE:
"""


def _strip_code_fence(text: str) -> str:
    """Removes ```json fences Claude may wrap its JSON in."""
    text = text.strip()
    if not text.startswith("```"):
        return text
    # Drop the opening fence and any language hint
    lines = text.splitlines()
    lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()


async def extract_msl_insights(
    transcript: str, msl_name: str = "Anonymous MSL"
) -> dict:
    """Sends MSL transcript to Claude for structured insight extraction.

    Returns:
        {"success": bool, "insights": [...], "overall_kol_sentiment": str,
         "debrief_summary": str, "msl_region": str, "insight_count": int}
        or {"success": False, "error": "...", "insights": []}
    """
    if not transcript or len(transcript.strip()) < 20:
        return {
            "success": False,
            "error": "Transcript too short to extract insights",
            "insights": [],
        }

    try:
        message = client.messages.create(
            model=MSL_MODEL,
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": MSL_EXTRACTION_PROMPT + transcript,
                }
            ],
        )

        response_text = _strip_code_fence(message.content[0].text)
        extracted_data = json.loads(response_text)

        for insight in extracted_data.get("insights", []):
            insight["msl_name"] = msl_name

        return {
            "success": True,
            "insights": extracted_data.get("insights", []),
            "overall_kol_sentiment": extracted_data.get(
                "overall_kol_sentiment", "Neutral"
            ),
            "debrief_summary": extracted_data.get("debrief_summary", ""),
            "msl_region": extracted_data.get("msl_region", "Unspecified"),
            "insight_count": len(extracted_data.get("insights", [])),
        }

    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Claude returned invalid JSON: {e}",
            "insights": [],
        }
    except Exception as e:  # noqa: BLE001
        return {"success": False, "error": str(e), "insights": []}
