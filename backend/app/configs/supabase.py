import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env.local")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Initialize Supabase client
supabase: Client = None

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_supabase() -> Client:
    """Get Supabase client instance."""
    return supabase


def check_supabase_connection() -> dict:
    """Check if Supabase connection is alive."""
    if not supabase:
        return {
            "status": "disconnected",
            "service": "supabase",
            "error": "Supabase credentials not configured"
        }
    
    try:
        # Try a simple query to verify connection
        result = supabase.table("_health_check_dummy").select("*").limit(1).execute()
        return {
            "status": "connected",
            "service": "supabase",
            "url": SUPABASE_URL
        }
    except Exception as e:
        error_str = str(e)
        # If error is about table not existing, connection is still working
        if "does not exist" in error_str or "relation" in error_str:
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
