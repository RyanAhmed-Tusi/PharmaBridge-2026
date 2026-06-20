"""Claude-powered Bridge Layer service.

For a given drug, takes MSL field-intelligence and patient-adherence summaries
and asks Claude whether the two independent streams confirm the same clinical
signal.
"""

import json
import os

import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

BRIDGE_MODEL = "claude-sonnet-4-6"


BRIDGE_SYSTEM_PROMPT = """You are the PharmaBridge Convergent Signal Detection Engine.
Your job is to analyze two independent data streams - MSL field intelligence and patient adherence data - and determine if they are independently confirming the same clinical signal about a specific drug.

A CONVERGENT SIGNAL exists when:
- Multiple MSLs have reported similar clinical observations about a drug (not just one isolated report)
- Patient data shows a related adherence pattern or barrier for the same drug
- Both streams are pointing to the same underlying issue independently

SIGNAL TYPES:
- "Safety / Adherence" - A potential safety issue is causing patients to stop taking the drug
- "Efficacy Concern" - Both MSLs and patients questioning whether the drug is working
- "Tolerability" - Side effects mentioned by KOLs are confirmed by patient barrier data
- "Market / Competitive" - Competitive pressure is reducing MSL enthusiasm AND patient access
- "Unmet Need" - Both streams reveal a population or condition not adequately served

CONFIDENCE:
- "High" - Both streams have strong, multiple data points confirming the same issue
- "Medium" - Suggestive pattern from both streams, but limited data
- "Low" - Early signal, needs more data to confirm

VELOCITY:
- "Accelerating" - The signal is getting stronger over time (more reports each week)
- "Stable" - Consistent signal, not growing
- "Declining" - Signal was stronger before, now reducing

Return ONLY valid JSON:
{
  "convergent_signal_detected": true or false,
  "drug_name": "Drug name",
  "signal_type": "Safety / Adherence",
  "confidence": "High",
  "velocity": "Accelerating",
  "signal_summary": "2-3 sentence explanation of what both streams are independently confirming",
  "recommended_actions": [
    "Action 1",
    "Action 2",
    "Action 3"
  ],
  "reasoning": "Brief explanation of why this is or is not a convergent signal"
}

If no convergent signal detected, set convergent_signal_detected to false and explain briefly in reasoning.
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


async def scan_for_convergent_signals(
    drug_name: str, msl_summary: str, patient_summary: str
) -> dict:
    """Asks Claude whether the two streams independently confirm the same signal."""
    prompt = f"""
Analyze the following two independent data streams for {drug_name}:

MSL FIELD INTELLIGENCE (last 30 days):
{msl_summary}

PATIENT ADHERENCE DATA (last 30 days):
{patient_summary}

Determine if these two streams are independently confirming the same clinical signal.
"""

    try:
        response = client.messages.create(
            model=BRIDGE_MODEL,
            max_tokens=800,
            system=BRIDGE_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = _strip_code_fence(response.content[0].text)
        result = json.loads(response_text)
        return {"success": True, **result}

    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Bridge layer returned invalid JSON: {e}",
            "convergent_signal_detected": False,
        }
    except Exception as e:  # noqa: BLE001
        return {
            "success": False,
            "error": str(e),
            "convergent_signal_detected": False,
        }
