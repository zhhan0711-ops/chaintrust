from typing import Protocol
from app.schemas.chain_data import ContractProfile
class ChainDataProvider(Protocol):
    async def get_contract_profile(self, address: str, activity_limit: int) -> ContractProfile: ...
