"""Disabled-by-default endpoint for a future approved questionnaire study."""
import json
import sqlite3

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from backend.app.research import responses

router = APIRouter(prefix="/research", tags=["research (disabled by default)"])
MAX_REQUEST_BYTES = 32 * 1024


@router.post("/responses", status_code=201)
async def create_research_response(request: Request):
    # Check before reading/parsing the body: disabled requests cause no DB access/write.
    if not responses.collection_enabled():
        raise HTTPException(status_code=503, detail="Research response collection is disabled")
    if request.headers.get("content-type", "").split(";", 1)[0].strip().lower() != "application/json":
        raise HTTPException(status_code=415, detail="Questionnaire requests must use JSON")
    content_length = request.headers.get("content-length")
    if content_length:
        try:
            declared_length = int(content_length)
        except ValueError as error:
            raise HTTPException(status_code=400, detail="Invalid request length") from error
        if declared_length < 0:
            raise HTTPException(status_code=400, detail="Invalid request length")
        if declared_length > MAX_REQUEST_BYTES:
            raise HTTPException(status_code=413, detail="Questionnaire request is too large")
    body = bytearray()
    async for chunk in request.stream():
        body.extend(chunk)
        if len(body) > MAX_REQUEST_BYTES:
            raise HTTPException(status_code=413, detail="Questionnaire request is too large")
    try:
        payload = json.loads(body)
        submission = responses.QuestionnaireSubmission.model_validate(payload)
    except (json.JSONDecodeError, ValidationError, ValueError, TypeError) as error:
        raise HTTPException(status_code=422, detail="Invalid questionnaire response") from error

    path = responses.default_database_path()
    if not path.is_file():
        raise HTTPException(status_code=503, detail="Research invitations are unavailable")
    try:
        _, duplicate = responses.submit_questionnaire(path, submission)
    except responses.ConsentVerificationRequired as error:
        raise HTTPException(status_code=403, detail="Research consent verification is unavailable") from error
    except responses.InvitationError as error:
        detail = str(error)
        status = 410 if detail == "Invitation has expired" else 404 if detail == "Invitation is invalid" else 409
        raise HTTPException(status_code=status, detail=detail) from error
    except sqlite3.Error as error:
        # Never include SQL, tokens, or submitted answer data in client responses.
        raise HTTPException(status_code=503, detail="Research response could not be stored") from error
    return JSONResponse(status_code=200 if duplicate else 201,
                        content={"status": "received", "duplicate_retry": duplicate})
