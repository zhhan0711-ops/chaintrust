import json
from datetime import datetime, timezone
from uuid import uuid4
from fastapi import APIRouter, HTTPException, Request
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.services.hashing import digest
from app.services.llm_reporter import generate_report
from app.services.rules import scan
from app.services.source_resolver import resolve_sepolia_source
from app.db.models import AnalysisRecord
from app.db.session import SessionLocal
from app.core.rate_limit import limiter

router = APIRouter(prefix="/api/v1/analyses", tags=["analyses"])

@router.post("", response_model=AnalysisResponse)
@limiter.limit("10/minute")
async def create_analysis(payload: AnalysisRequest, request: Request):
    try:
        source = payload.source_code if payload.input_type == "code" else resolve_sepolia_source(payload.contract_address or "")
        assert source is not None
        findings = scan(source)
        report = generate_report(source, findings)
        created_at = datetime.now(timezone.utc).isoformat()
        response = AnalysisResponse(id=str(uuid4()), input_type=payload.input_type, source_hash=digest(source), report_hash=digest(json.dumps(report.model_dump(), sort_keys=True)), report=report, created_at=created_at)
        with SessionLocal() as db:
            db.add(AnalysisRecord(id=response.id, input_type=response.input_type, source_hash=response.source_hash, report_hash=response.report_hash, report_json=report.model_dump_json(), created_at=datetime.fromisoformat(created_at)))
            db.commit()
        return response
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception:
        raise HTTPException(status_code=502, detail="Analysis could not be completed. Check server configuration and try again.")
