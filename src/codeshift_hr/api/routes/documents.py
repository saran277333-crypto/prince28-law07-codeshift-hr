"""Document endpoints backed by PostgreSQL."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from codeshift_hr.api.deps import get_repo
from codeshift_hr.db.repository import FILTER_KEY, DocumentRepository

router = APIRouter(prefix="/v1/documents", tags=["documents"])


@router.get("")
async def list_documents(
    request: Request,
    q: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    repo: DocumentRepository = Depends(get_repo),  # noqa: B008
):
    """Get documents with search, metadata filters and pagination."""

    reserved = {"q", "limit", "offset"}
    filters = {}

    for key, value in request.query_params.items():
        if key in reserved:
            continue

        if not FILTER_KEY.fullmatch(key):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid filter name: '{key}'.",
            )

        filters[key] = value

    total, items = await repo.list(
        q=q,
        filters=filters,
        limit=limit,
        offset=offset,
    )

    return {
        "total": total,
        "items": items,
    }


@router.get("/{document_id}")
async def get_document(
    document_id: str,
    repo: DocumentRepository = Depends(get_repo),  # noqa: B008
):
    """Get one document using its ID."""

    document = await repo.get(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail=f"No document with id '{document_id}'.",
        )

    return document
