from app.schemas.release_brief import ReleaseRiskBrief, BriefItem
from app.schemas.chain_data import ContractProfile
def build_brief(profile: ContractProfile | None, input_mode: str, link_status: str) -> ReleaseRiskBrief:
    evidence=[]; privilege=[]; chain=[]
    if profile:
        chain.append(BriefItem(statement=f'Profile data mode: {profile.data_mode}.', evidence_type='sample' if profile.data_mode=='sandbox' else 'onchain_data', evidence=[f'address: {profile.address}'], confidence='sample' if profile.data_mode=='sandbox' else 'unavailable'))
        privilege=[BriefItem(statement=f'{p.function_name} is classified as {p.category}.',evidence_type=p.evidence_type,evidence=[p.evidence],confidence=p.confidence,recommended_action='Confirm authorization, operational controls, and release intent.') for p in profile.privileges]
    limitations=['This platform supports engineering review workflows and does not replace a professional security audit.','Findings are evidence-backed signals, not a security guarantee.']
    if link_status in ('unavailable','mismatch'): limitations.append('Source/address linkage was not confirmed; evidence was not silently merged.')
    return ReleaseRiskBrief(executive_summary=[BriefItem(statement=f'{input_mode} Release Risk Brief created.',evidence_type='heuristic',evidence=['input classification'],confidence='heuristic')],release_blockers=[],privilege_and_upgradeability_review=privilege,onchain_observations=chain,required_manual_checks=[BriefItem(statement='Validate release authority, deployment parameters, and source/address linkage before release.',evidence_type='heuristic',evidence=[],confidence='heuristic',recommended_action='Complete team security review.')],evidence_and_confidence=evidence,review_limitations=limitations)
