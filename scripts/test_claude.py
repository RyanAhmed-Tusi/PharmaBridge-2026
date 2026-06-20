"""Quick smoke test for the Anthropic Claude API.

Run before seeding to confirm ANTHROPIC_API_KEY is valid:
    cd pharmabridge/scripts
    python test_claude.py
"""

import os
import sys

# Use the Windows / OS native certificate store for TLS — required on
# corporate networks where outbound HTTPS is SSL-inspected.
import truststore

truststore.inject_into_ssl()

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "backend", ".env"))

import anthropic  # noqa: E402


def main() -> int:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY missing from backend/.env")
        return 1

    client = anthropic.Anthropic(api_key=api_key)

    print("Calling Claude (claude-sonnet-4-6)...")
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=60,
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: PharmaBridge connection OK.",
            }
        ],
    )
    text = response.content[0].text.strip()
    print(f"Claude said: {text}")

    if "PharmaBridge connection OK" in text:
        print("PASS — Claude API is reachable and the key works.")
        return 0
    print("WARN — Claude responded but with unexpected text. Key is valid though.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
