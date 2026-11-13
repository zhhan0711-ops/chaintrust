from fastapi import APIRouter
from app.schemas.chain_data import ProfileRequest, ContractProfile
from app.schemas.release_brief import BriefRequest, BriefResponse
from app.services.mock_chain_provider import MockChainDataProvider
from app.services.sepolia_provider import SepoliaRpcProvider
from app.services.release_brief import build_brief
from app.services.source_binding import binding
router=APIRouter(prefix='/api/v1',tags=['risk-intelligence'])
@router.post('/profiles',response_model=ContractProfile)
async def profile(payload: ProfileRequest):
    return await (MockChainDataProvider() if payload.mode=='sandbox' else SepoliaRpcProvider()).get_contract_profile(payload.contract_address,payload.activity_limit)
@router.post('/release-briefs',response_model=BriefResponse)
async def brief(payload: BriefRequest):
    has_source=bool(payload.source_code); has_address=bool(payload.contract_address); mode='source + address review' if has_source and has_address else 'source-only review' if has_source else 'address-only review'; profile_data=None; verified=None
    if has_address:
        provider=MockChainDataProvider() if payload.mode=='sandbox' else SepoliaRpcProvider(); profile_data=await provider.get_contract_profile(payload.contract_address,10)
        if payload.mode=='live':
            result=await provider._explorer('getsourcecode',address=payload.contract_address); verified=result[0].get('SourceCode') if isinstance(result,list) and result else None
    source_binding=binding(payload.source_code,verified,mode)
    link='sample' if payload.mode=='sandbox' else source_binding['source_match_status']
    return BriefResponse(input_mode=mode,source_address_link=link,source_binding=source_binding,profile=profile_data,brief=build_brief(profile_data,mode,source_binding['source_match_status']))