"""Health and readiness endpoints."""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from codeshift_hr.api.deps import check_db

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/ready")
async def readiness_check(database: bool = Depends(check_db)):
    if not database:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "checks": {"database": False},
            },
        )

    return {
        "status": "ready",
        "checks": {"database": True},
    }
