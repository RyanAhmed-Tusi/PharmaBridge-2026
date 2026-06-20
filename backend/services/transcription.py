"""PharmaBridge Speech-to-Text Service.

Provider selection (automatic, based on .env):
  - If OPENAI_API_KEY is set -> use OpenAI Whisper (whisper-1)
  - If not set              -> use ElevenLabs Scribe (scribe_v1)

To switch to Whisper when you get OpenAI access:
    1. Add OPENAI_API_KEY=sk-... to backend/.env
    2. Restart the backend server
    3. Done. No code changes needed.
"""

import os
import tempfile

import httpx
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()

_USE_OPENAI = bool(OPENAI_API_KEY)

if _USE_OPENAI:
    import openai as _openai_sdk

    _openai_client = _openai_sdk.OpenAI(api_key=OPENAI_API_KEY)
    print("STT Provider: OpenAI Whisper (whisper-1)")
else:
    _openai_client = None
    print(
        "STT Provider: ElevenLabs Scribe (scribe_v1) "
        "- add OPENAI_API_KEY to switch to Whisper"
    )


# ──────────────────────────────────────────────
# PUBLIC API
# ──────────────────────────────────────────────


async def transcribe_audio(audio_bytes: bytes, filename: str = "audio.webm") -> dict:
    """Transcribes audio bytes to text using whichever STT provider is configured.

    Returns:
        Success: {"transcript": "...", "success": True, "provider": "..."}
        Failure: {"transcript": "", "success": False, "error": "...", "provider": "..."}
    """
    if _USE_OPENAI:
        return await _transcribe_with_whisper(audio_bytes, filename)
    return await _transcribe_with_elevenlabs(audio_bytes, filename)


# ──────────────────────────────────────────────
# PROVIDER A: OpenAI Whisper
# ──────────────────────────────────────────────


async def _transcribe_with_whisper(audio_bytes: bytes, filename: str) -> dict:
    """OpenAI Whisper (whisper-1). Activated automatically when OPENAI_API_KEY is set."""
    suffix = _get_suffix(filename)
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as audio_file:
            transcription = _openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en",
                prompt=(
                    "Medical Science Liaison debrief. Pharmaceutical discussion covering "
                    "KOL meetings, clinical trials, adverse events, pharmacovigilance, "
                    "drug safety observations, and patient adherence."
                ),
            )
        return {
            "transcript": transcription.text,
            "success": True,
            "provider": "openai_whisper",
        }
    except Exception as e:  # noqa: BLE001
        return {
            "transcript": "",
            "success": False,
            "error": f"Whisper transcription failed: {e}",
            "provider": "openai_whisper",
        }
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


# ──────────────────────────────────────────────
# PROVIDER B: ElevenLabs Scribe (primary fallback)
# ──────────────────────────────────────────────


async def _transcribe_with_elevenlabs(audio_bytes: bytes, filename: str) -> dict:
    """ElevenLabs Scribe v1. PRIMARY provider when OPENAI_API_KEY is not configured."""
    if not ELEVENLABS_API_KEY:
        return {
            "transcript": "",
            "success": False,
            "error": "Neither OPENAI_API_KEY nor ELEVENLABS_API_KEY is set in .env",
            "provider": "elevenlabs_scribe",
        }

    url = "https://api.elevenlabs.io/v1/speech-to-text"
    mime_type = _get_mime_type(filename)

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url,
                headers={"xi-api-key": ELEVENLABS_API_KEY},
                files={"file": (filename, audio_bytes, mime_type)},
                data={"model_id": "scribe_v1", "language_code": "en"},
            )
            response.raise_for_status()
            data = response.json()

        transcript = (data.get("text") or "").strip()

        return {
            "transcript": transcript,
            "success": bool(transcript),
            "provider": "elevenlabs_scribe",
        }

    except httpx.HTTPStatusError as e:
        try:
            error_body = e.response.json().get("detail", str(e))
        except Exception:  # noqa: BLE001
            error_body = str(e)
        return {
            "transcript": "",
            "success": False,
            "error": f"ElevenLabs STT HTTP error {e.response.status_code}: {error_body}",
            "provider": "elevenlabs_scribe",
        }
    except Exception as e:  # noqa: BLE001
        return {
            "transcript": "",
            "success": False,
            "error": f"ElevenLabs STT failed: {e}",
            "provider": "elevenlabs_scribe",
        }


# ──────────────────────────────────────────────
# UTILITIES
# ──────────────────────────────────────────────


def _get_suffix(filename: str) -> str:
    ext = os.path.splitext(filename)[-1].lower()
    return ext if ext else ".webm"


def _get_mime_type(filename: str) -> str:
    mapping = {
        ".webm": "audio/webm",
        ".mp4": "audio/mp4",
        ".wav": "audio/wav",
        ".mp3": "audio/mpeg",
        ".ogg": "audio/ogg",
        ".m4a": "audio/mp4",
        ".flac": "audio/flac",
    }
    ext = os.path.splitext(filename)[-1].lower()
    return mapping.get(ext, "audio/webm")


def get_stt_provider_info() -> dict:
    """Returns which STT provider is currently active. Useful for debugging."""
    return {
        "active_provider": "openai_whisper" if _USE_OPENAI else "elevenlabs_scribe",
        "openai_configured": _USE_OPENAI,
        "elevenlabs_configured": bool(ELEVENLABS_API_KEY),
        "note": "Add OPENAI_API_KEY to .env to switch to Whisper automatically",
    }
