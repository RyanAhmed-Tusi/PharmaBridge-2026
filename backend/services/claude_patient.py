"""Claude-powered Patient Adherence Companion conversation service.

Drives Aria, the warm patient companion. Each turn:
  - Detects which of six adherence barriers (Cost, Side Effect, Forgetfulness,
    Belief, Complexity, Access) the patient might be facing
  - Returns a 2-3 sentence empathetic response
  - Flags when a care-team alert should be triggered
"""

import json
import os

import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

PATIENT_MODEL = "claude-sonnet-4-6"


PATIENT_SYSTEM_PROMPT = """You are a warm, empathetic patient adherence companion for PharmaBridge.
Your name is Aria. You have a single purpose: to gently understand why a patient may be struggling with their medication and to support them in continuing their treatment.

YOU ARE NOT a doctor and should never give medical advice. If a patient has a serious concern, you direct them to their care team.

THE SIX BARRIER TYPES you must listen for:
1. "Cost" - mentions of price, co-pay, can't afford, expensive, splitting pills
2. "Side Effect" - mentions of feeling tired, nausea, headache, stomach issues, any physical symptom they link to medication
3. "Forgetfulness" - mentions of forgetting, missing doses, not remembering, irregular schedule
4. "Belief" - mentions of feeling fine already, not needing medication, don't think it works, skepticism
5. "Complexity" - mentions of taking many pills, confusing schedule, multiple medications
6. "Access" - mentions of pharmacy distance, running out, hard to get prescription, transportation

CONVERSATION STYLE:
- Warm and human, never clinical or robotic
- Ask ONE question at a time, never multiple
- Listen actively - reflect what the patient said before asking your next question
- Do not push or pressure. Be gentle.
- Keep responses SHORT - 2-3 sentences maximum
- If the patient says they took their medication, celebrate it warmly

WHEN YOU DETECT A BARRIER:
- Do NOT reveal that you've detected a barrier
- Continue the conversation naturally but ask targeted follow-up questions to confirm it
- Once confirmed, mention gently that you'll pass this along to their care team

RESPONSE FORMAT:
Always return valid JSON only, no markdown:
{
  "response_text": "Your warm response to the patient",
  "detected_barrier": "Side Effect" or null,
  "barrier_confidence": "High" or "Medium" or "Low" or null,
  "barrier_details": "Specific detail about the barrier" or null,
  "trigger_care_team_alert": false,
  "adherence_taken_today": true or false or null
}

trigger_care_team_alert should be true ONLY when:
- barrier_confidence is "High" (confirmed with multiple signals)
- The barrier is confirmed enough to warrant clinical review

Set adherence_taken_today to true if patient says they took medication, false if they skipped, null if unclear.
"""


def _strip_code_fence(text: str) -> str:
    text = (text or "").strip()
    if not text.startswith("```"):
        return text
    lines = text.splitlines()
    lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()


async def patient_chat(
    patient_message: str,
    conversation_history: list,
    patient_profile: dict,
) -> dict:
    """Runs one turn of the patient companion conversation.

    Args:
        patient_message: What the patient just said
        conversation_history: List of {"role": "user"|"assistant", "content": "..."}
        patient_profile: Patient's current row from patient_profiles

    Returns:
        Dict with response_text, detected_barrier, trigger_care_team_alert,
        adherence_taken_today, success, etc.
    """
    patient_context = f"""
PATIENT CONTEXT:
- Patient code: {patient_profile.get('patient_code', 'Unknown')}
- Condition: {patient_profile.get('condition', 'Unknown')}
- Medication: {patient_profile.get('drug_name', 'their medication')}
- Enrolled since: {patient_profile.get('created_at', 'recently')}
- Current detected barrier: {patient_profile.get('primary_barrier', 'Unknown')}
- Barrier confidence: {patient_profile.get('barrier_confidence', 'Low')}
- Adherence rate: {patient_profile.get('adherence_rate', 100)}%
- Today's session number: {patient_profile.get('session_count', 1)}
"""

    messages = []
    for turn in conversation_history or []:
        role = turn.get("role") if isinstance(turn, dict) else getattr(turn, "role", None)
        content = (
            turn.get("content")
            if isinstance(turn, dict)
            else getattr(turn, "content", None)
        )
        if role and content:
            messages.append({"role": role, "content": content})

    messages.append(
        {
            "role": "user",
            "content": f"{patient_context}\n\nPatient says: {patient_message}",
        }
    )

    try:
        response = client.messages.create(
            model=PATIENT_MODEL,
            max_tokens=500,
            system=PATIENT_SYSTEM_PROMPT,
            messages=messages,
        )

        response_text = _strip_code_fence(response.content[0].text)
        result = json.loads(response_text)

        return {"success": True, **result}

    except json.JSONDecodeError:
        return {
            "success": True,
            "response_text": "Thank you for sharing that with me. How are you feeling today?",
            "detected_barrier": None,
            "barrier_confidence": None,
            "barrier_details": None,
            "trigger_care_team_alert": False,
            "adherence_taken_today": None,
        }
    except Exception as e:  # noqa: BLE001
        return {
            "success": False,
            "error": str(e),
            "response_text": "I'm having a brief connection issue. Can you try again in a moment?",
            "detected_barrier": None,
            "trigger_care_team_alert": False,
        }


async def generate_opening_message(patient_profile: dict, session_number: int) -> str:
    """Generates a personalized opening message for each daily check-in."""
    prompt = f"""Generate a warm, brief opening message (1-2 sentences only) for a patient adherence check-in.
Patient is on {patient_profile.get('drug_name', 'their medication')} for {patient_profile.get('condition', 'their condition')}.
This is day {session_number} of their check-in.
Known barrier (if any): {patient_profile.get('primary_barrier', 'None detected yet')}.
Make the message feel personal and caring, not clinical. Ask about how they're doing AND whether they took their medication today.
Return ONLY the message text, no JSON, no quotes."""

    try:
        response = client.messages.create(
            model=PATIENT_MODEL,
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()
    except Exception:  # noqa: BLE001
        return "Good morning! How are you feeling today? Did you take your medication this morning?"
