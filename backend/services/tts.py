"""PharmaBridge Text-to-Speech Service (ElevenLabs).

Used by the Patient Companion to make Aria speak in a warm, human voice.
Returns base64-encoded MP3 so the response can be sent as JSON.
"""

import base64
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")


async def text_to_speech(text: str) -> dict:
    """Converts text to speech using ElevenLabs and returns base64-encoded MP3."""
    if not ELEVENLABS_API_KEY:
        return {
            "audio_base64": None,
            "success": False,
            "error": "ELEVENLABS_API_KEY is not set in .env",
        }

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY,
    }

    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.6,
            "similarity_boost": 0.8,
            "style": 0.2,
            "use_speaker_boost": True,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()

            audio_base64 = base64.b64encode(response.content).decode("utf-8")

            return {
                "audio_base64": audio_base64,
                "content_type": "audio/mpeg",
                "success": True,
            }

    except httpx.HTTPStatusError as e:
        try:
            error_body = e.response.json()
        except Exception:  # noqa: BLE001
            error_body = e.response.text
        return {
            "audio_base64": None,
            "success": False,
            "error": f"ElevenLabs TTS HTTP {e.response.status_code}: {error_body}",
        }
    except Exception as e:  # noqa: BLE001
        return {"audio_base64": None, "success": False, "error": str(e)}
