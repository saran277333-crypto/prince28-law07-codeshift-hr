from fastapi import APIRouter, Depends, HTTPException, Query

from codeshift_hr.api.deps import get_store
from codeshift_hr.store import RecordStore

router = APIRouter(prefix="/v1/documents", tags=["documents"])


# Get all documents with search and pagination
@router.get("")
def list_documents(
    q: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    store: RecordStore = Depends(get_store),  # noqa: B008
):
    records = store.get_all()

    # Search documents
    if q:
        search_text = q.lower()

        records = [
            record
            for record in records
            if any(
                search_text in str(value).lower()
                for value in record.values()
                if value is not None
            )
        ]

    # Pagination
    total = len(records)
    items = records[offset : offset + limit]

    return {"total": total, "items": items}


# Get one document using its ID
@router.get("/{document_id}")
def get_document(
    document_id: str,
    store: RecordStore = Depends(get_store),  # noqa: B008
):
    document = store.get_by_id(document_id)

    if document is None:
        raise HTTPException(
            status_code=404, detail=f"No document with id '{document_id}'."
        )

    return document
