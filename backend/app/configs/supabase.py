import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env.local")

SUPABASE_URL = os.getenv("SUPABASE_URL")
# Try both key names
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Store initialization error
_supabase: Client = None
_init_error: str = None


def get_supabase() -> Client:
    """Get Supabase client instance (lazy initialization)."""
    global _supabase, _init_error
    if _supabase is None and SUPABASE_URL and SUPABASE_KEY:
        try:
            _supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            _init_error = str(e)
    return _supabase


def check_supabase_connection() -> dict:
    """Check if Supabase connection is alive."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return {
            "status": "disconnected",
            "service": "supabase",
            "error": "Supabase credentials not configured. Set SUPABASE_URL and SUPABASE_KEY (or SUPABASE_SERVICE_KEY or SUPABASE_ANON_KEY)"
        }
    
    try:
        client = get_supabase()
        if not client:
            return {
                "status": "disconnected",
                "service": "supabase",
                "error": _init_error or "Failed to create Supabase client",
                "hint": "API key should start with 'eyJ...' (JWT format). Get it from Supabase Dashboard → Settings → API"
            }
        
        # Try a simple query to verify connection
        result = client.table("_health_check_dummy").select("*").limit(1).execute()
        return {
            "status": "connected",
            "service": "supabase",
            "url": SUPABASE_URL
        }
    except Exception as e:
        error_str = str(e)
        # If error is about table not existing, connection is still working
        if any(x in error_str for x in ["does not exist", "relation", "PGRST", "Could not find"]):
            return {
                "status": "connected",
                "service": "supabase",
                "url": SUPABASE_URL
            }
        return {
            "status": "disconnected",
            "service": "supabase",
            "error": error_str
        }