import os
import time
import logging
from supabase import create_client, Client # type: ignore

logger = logging.getLogger("uvicorn.error")

def create_supabase_client() -> Client:
    supabase_uri = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    return create_client(supabase_uri, supabase_key)

def get_user_with_retry(supabase: Client, access_token: str, max_retries: int = 5):
    for attempt in range(max_retries):
        try:
            return supabase.auth.get_user(access_token)
        except Exception as e:
            error_msg = str(e)
            if "ConnectionTerminated" in error_msg and attempt < max_retries - 1:
                wait_time = 0.1 * (2 ** attempt)
                logger.warning(f"ConnectionTerminated, reintentando en {wait_time}s (intento {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                raise