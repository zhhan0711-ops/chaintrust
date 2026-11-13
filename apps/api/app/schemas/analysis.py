from typing import Literal
from pydantic import BaseModel, Field, field_validator
from .report import RiskReport

class AnalysisRequest(BaseModel):
    input_type: Literal["code", "sepolia_address"]
    source_code: str | None = Field(default=None, max_length=100_000)
    contract_address: str | None = None

    @field_validator("contract_address")
    @classmethod
    def validate_address(cls, value: str | None):
        if value is not None and (not value.startswith("0x") or len(value) != 42):
            raise ValueError("Expected an EVM address (0x followed by 40 hexadecimal characters).")
        return value

    def model_post_init(self, __context):
        if self.input_type == "code" and not self.source_code:
            raise ValueError("source_code is required for code analysis.")
        if self.input_type == "sepolia_address" and not self.contract_address:
            raise ValueError("contract_address is required for Sepolia address analysis.")

class AnalysisResponse(BaseModel):
    id: str
    input_type: str
    source_hash: str
    report_hash: str
    report: RiskReport
    created_at: str
