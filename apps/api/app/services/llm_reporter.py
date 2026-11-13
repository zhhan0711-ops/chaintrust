import json
from openai import OpenAI
from app.core.config import settings
from app.schemas.report import Finding, RiskReport
from app.services.rules import RuleFinding

SYSTEM = """You explain evidence-backed smart-contract static scan signals for engineering review teams. This does not replace a professional security audit. Do not claim safety, completeness, exploitability, or certainty. Return only the requested JSON."""

def fallback(findings: list[RuleFinding]) -> RiskReport:
    order = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
    level = max((f.severity for f in findings), key=lambda x: order[x], default="low")
    return RiskReport(overall_risk_level=level, findings=[Finding(title=f.title, severity=f.severity, description=f.description, code_evidence=f.evidence, potential_impact="Unexpected authorization, state, or asset-handling behavior may be possible if this pattern is exploitable in context.", recommended_fix=f.suggestion) for f in findings], limitations=["This rule-based scan does not model all execution paths or Solidity semantics.", "Findings are evidence-backed signals for engineering review; they are not a security guarantee and do not replace a professional security audit."])

def generate_report(source: str, rule_findings: list[RuleFinding]) -> RiskReport:
    if not settings.openai_api_key:
        return fallback(rule_findings)
    client = OpenAI(api_key=settings.openai_api_key)
    payload = {"source_excerpt": source[:12000], "rule_findings": [f.__dict__ for f in rule_findings]}
    response = client.chat.completions.create(model=settings.openai_model, messages=[{"role":"system","content":SYSTEM},{"role":"user","content":json.dumps(payload)}], response_format={"type":"json_schema", "json_schema":{"name":"risk_report","strict":True,"schema":{"type":"object","properties":{"overall_risk_level":{"type":"string","enum":["low","medium","high","critical","unknown"]},"findings":{"type":"array","items":{"type":"object","properties":{"title":{"type":"string"},"severity":{"type":"string","enum":["info","low","medium","high","critical"]},"description":{"type":"string"},"code_evidence":{"type":"string"},"potential_impact":{"type":"string"},"recommended_fix":{"type":"string"}},"required":["title","severity","description","code_evidence","potential_impact","recommended_fix"],"additionalProperties":False}},"limitations":{"type":"array","items":{"type":"string"}}},"required":["overall_risk_level","findings","limitations"],"additionalProperties":False}}})
    return RiskReport.model_validate_json(response.choices[0].message.content)
