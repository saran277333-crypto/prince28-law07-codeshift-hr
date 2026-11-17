from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/ready")
def readiness_check(request: Request):

    store = request.app.state.store

    records_loaded = len(store.get_all()) > 0

    if not records_loaded:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "checks": {"records_loaded": False}},
        )

    return {"status": "ready", "checks": {"records_loaded": True}}
