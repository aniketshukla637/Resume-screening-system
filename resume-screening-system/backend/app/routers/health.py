from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/ping")
def ping():
    """Simple health-check endpoint to confirm the server is alive."""
    return {"status": "ok", "message": "Server is running"}
