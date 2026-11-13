from pydantic import BaseModel
from .chain_data import EvidenceType, Confidence, ContractProfile

class BriefItem(BaseModel):
    statement: str; evidence_type: EvidenceType; evidence: list[str]; confidence: Confidence; recommended_action: str | None = None
class ReleaseRiskBrief(BaseModel):
    executive_summary: list[BriefItem]; release_blockers: list[BriefItem]; privilege_and_upgradeability_review: list[BriefItem]
    onchain_observations: list[BriefItem]; required_manual_checks: list[BriefItem]; evidence_and_confidence: list[BriefItem]; review_limitations: list[str]
class BriefRequest(BaseModel):
    source_code: str | None = None; contract_address: str | None = None; mode: str = 'live'
class BriefResponse(BaseModel):
    input_mode: str; source_address_link: Confidence; source_binding: dict; profile: ContractProfile | None; brief: ReleaseRiskBrief
