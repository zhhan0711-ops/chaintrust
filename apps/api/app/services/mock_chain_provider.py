import json
from pathlib import Path
from app.schemas.chain_data import ContractProfile
class MockChainDataProvider:
    async def get_contract_profile(self, address: str, activity_limit: int) -> ContractProfile:
        data=json.loads((Path(__file__).parent.parent/'fixtures'/'sepolia_sample_profile.json').read_text())
        data['address']=address; data['interactions']=data['interactions'][:activity_limit]
        return ContractProfile.model_validate(data)
