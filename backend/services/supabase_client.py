"""Supabase client singleton for PharmaBridge backend.

Uses the service role key to bypass Row Level Security so the backend
can read/write every table directly.
"""

import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()


def get_supabase_client() -> Client:
    """Returns an authenticated Supabase client using the service role key."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")

    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env")

    return create_client(url, key)


# Singleton client instance — imported by every service that needs DB access.
supabase: Client = get_supabase_client()
