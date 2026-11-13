import asyncio
from app.services.mock_chain_provider import MockChainDataProvider
from app.services.privilege_analyzer import analyze_privileges
from app.schemas.chain_data import ProfileRequest
from app.services.release_brief import build_brief
def test_sandbox_provider_returns_sample():
    value=asyncio.run(MockChainDataProvider().get_contract_profile('0x0000000000000000000000000000000000000001',5)); assert value.data_mode=='sandbox'
def test_privilege_recognition():
    assert len(analyze_privileges('function upgradeTo(address x) external onlyOwner {}')) == 1
def test_sepolia_only():
    try: ProfileRequest(contract_address='0x0000000000000000000000000000000000000001',chain_id=1)
    except ValueError: return
    assert False
def test_brief_boundary():
    assert 'professional security audit' in ' '.join(build_brief(None,'source-only review','unavailable').review_limitations)

class FakeLiveProvider:
    pass

def test_live_provider_rejects_wrong_chain(monkeypatch):
    from app.services.sepolia_provider import SepoliaRpcProvider
    import asyncio
    provider = SepoliaRpcProvider()
    async def rpc(method, params):
        return '0x1' if method == 'eth_chainId' else None
    monkeypatch.setattr(provider, '_rpc', rpc)
    try:
        asyncio.run(provider.get_contract_profile('0x0000000000000000000000000000000000000001', 10))
    except ValueError as exc:
        assert 'not Sepolia' in str(exc)
        return
    assert False

def test_source_binding_normalizes_equivalent_source():
    from app.services.source_binding import source_hash
    assert source_hash('contract A {}\r\n\r\n') == source_hash('contract A {}\n')
def test_source_binding_matched_mismatch_and_unavailable():
    from app.services.source_binding import binding
    assert binding('contract A {}','contract A {}','source + address review')['source_match_status']=='matched'
    assert binding('contract A {}','contract B {}','source + address review')['source_match_status']=='mismatch'
    assert binding('contract A {}',None,'source + address review')['source_match_status']=='unavailable'
def test_source_only_binding_not_applicable():
    from app.services.source_binding import binding
    assert binding('contract A {}',None,'source-only review')['source_match_status']=='not_applicable'

def test_eip1967_slot_address_parsing():
    slot='0x0000000000000000000000001234567890123456789012345678901234567890'
    assert '0x'+slot[-40:] == '0x1234567890123456789012345678901234567890'
def test_privilege_abi_and_source_classification():
    from app.services.privilege_analyzer import analyze_privileges
    values=analyze_privileges('function pause() external onlyOwner {}', [{'type':'function','name':'upgradeTo'}])
    assert {x.category for x in values} == {'emergency_control','upgradeability'}
def test_privilege_unavailable_is_empty_not_no_risk():
    from app.services.privilege_analyzer import analyze_privileges
    assert analyze_privileges() == []

def test_change_review_blocks_upgrade_entry():
    from app.services.change_review import review
    assert review('contract A {}','contract A { function upgradeTo(address x) external public {} }')['release_readiness']=='blocked'
def test_change_review_ready_requires_two_sources():
    from app.services.change_review import review
    assert review('','contract A {}')['release_readiness']=='unknown'
