"""
Shared Supabase client factory.

Centralises the `get_supabase()` helper so every router can reuse the
same creation logic without duplicating env-var reads.
"""

from fastapi import HTTPException
from supabase import create_client, Client, ClientOptions
from config.env import settings


def get_supabase(access_token: str = None) -> Client:
    """Return a fresh Supabase client (stateless – one per request)."""
    if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
        raise HTTPException(
            status_code=500,
            detail="Supabase credentials not configured. "
                   "Please set SUPABASE_URL and SUPABASE_ANON_KEY.",
        )
    
    if access_token:
        options = ClientOptions(headers={"Authorization": f"Bearer {access_token}"})
        return create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY, options=options)
        
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
