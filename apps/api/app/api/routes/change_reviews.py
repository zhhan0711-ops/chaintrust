from fastapi import APIRouter
from app.schemas.change_review import ChangeReviewRequest
from app.services.change_review import review
router=APIRouter(prefix='/api/v1',tags=['change-review'])
SAMPLE_BASELINE='contract Vault { function deposit() external public {} }'
SAMPLE_CANDIDATE='contract Vault { function deposit() external public {} function upgradeTo(address implementation) external public {} }'
@router.post('/change-reviews')
async def create_change_review(payload:ChangeReviewRequest):
    baseline,candidate=(SAMPLE_BASELINE,SAMPLE_CANDIDATE) if payload.sandbox else (payload.baseline_source,payload.candidate_source)
    result=review(baseline,candidate)
    result['input_mode']='sandbox' if payload.sandbox else 'source_to_source'
    result['deployed_address']=payload.deployed_address
    return result