from fastapi import Request

from codeshift_hr.store import RecordStore


def get_store(request: Request) -> RecordStore:
    return request.app.state.store
