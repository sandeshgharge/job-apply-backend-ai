"""
Shared Supabase client factory.

Centralises the `get_supabase()` helper so every router can reuse the
same creation logic without duplicating env-var reads.
"""

from fastapi import HTTPException
from supabase import create_client, Client, ClientOptions
from config.env import settings


def get_supabase(access_token: str = None, refresh_token: str = None) -> Client:
    """Return a fresh Supabase client (stateless – one per request)."""
    if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
        raise HTTPException(
            status_code=500,
            detail="Supabase credentials not configured. "
                   "Please set SUPABASE_URL and SUPABASE_ANON_KEY.",
        )
    client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
    if access_token and refresh_token:
        # Full session — auth methods like update_user will work   
        client.auth.set_session(access_token, refresh_token)
        
    elif access_token:
        # DB queries only — auth methods won't work
        options = ClientOptions(headers={"Authorization": f"Bearer {access_token}"})
        return create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY, options=options)
    
       
    return client
