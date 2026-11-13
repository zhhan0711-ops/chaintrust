from typing import Literal
from pydantic import BaseModel, Field

RiskLevel = Literal["low", "medium", "high", "critical", "unknown"]
Severity = Literal["info", "low", "medium", "high", "critical"]

class Finding(BaseModel):
    title: str
    severity: Severity
    description: str
    code_evidence: str
    potential_impact: str
    recommended_fix: str

class RiskReport(BaseModel):
    overall_risk_level: RiskLevel
    findings: list[Finding] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
