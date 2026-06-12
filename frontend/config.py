import os

# Get API base URL from environment variable or use localhost as fallback
API_BASE = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/") + "/api"

def get_api_url():
    """Return the current API base URL."""
    return API_BASE
