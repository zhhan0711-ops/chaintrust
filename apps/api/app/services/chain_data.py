from typing import Literal
from pydantic import BaseModel, Field, field_validator

EvidenceType = Literal['source_code', 'onchain_data', 'heuristic', 'unavailable', 'sample']
Confidence = Literal['confirmed', 'heuristic', 'unavailable', 'sample', 'mismatch']

class Deployment(BaseModel):
    transaction_hash: str | None = None; deployer: str | None = None; block_number: int | None = None; timestamp: str | None = None; data_status: Confidence
class Interaction(BaseModel):
    transaction_hash: str; timestamp: str | None = None; block_number: int | None = None; status: Literal['success','failed','unknown']; source: EvidenceType
class PrivilegeSignal(BaseModel):
    function_name: str; category: str; access_signal: str; evidence: str; evidence_type: EvidenceType; confidence: Confidence
class ProxyAnalysis(BaseModel):
    classification: Literal['confirmed_proxy','delegatecall_signal','no_signal','unavailable']; confidence: Confidence; evidence: list[str] = []
class ContractProfile(BaseModel):
    address: str; chain_id: int = 11155111; has_code: bool; balance_wei: str | None = None; deployment: Deployment
    interactions: list[Interaction] = []; interaction_count: int | None = None; failed_transaction_count: int | None = None
    privileges: list[PrivilegeSignal] = []; proxy_analysis: ProxyAnalysis; data_mode: Literal['live','sandbox']; source_link_status: Confidence = 'unavailable'
class ProfileRequest(BaseModel):
    contract_address: str = Field(min_length=42, max_length=42); chain_id: int = 11155111; mode: Literal['live','sandbox'] = 'live'; activity_limit: int = Field(default=10, ge=1, le=25)
    @field_validator('contract_address')
    @classmethod
    def address(cls, v: str):
        if not v.startswith('0x'): raise ValueError('Expected an EVM address.')
        return v
    @field_validator('chain_id')
    @classmethod
    def sepolia_only(cls, v: int):
        if v != 11155111: raise ValueError('ChainTrust V2 supports Sepolia only (11155111).')
        return v
