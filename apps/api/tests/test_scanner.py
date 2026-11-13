from app.services.rules import scan

def test_detects_requested_rule_types():
    code = '''contract Demo { mapping(address=>uint) balances; address owner; function withdraw() external { (bool ok,) = msg.sender.call{value: balances[msg.sender]}(\"\"); balances[msg.sender] = 0; } function setOwner(address x) external { owner=x; } function auth() external view returns(bool) { return tx.origin == owner; } function proxy(address x, bytes memory d) external { x.delegatecall(d); }}'''
    found = {x.rule_id for x in scan(code)}
    assert {"TX_ORIGIN", "DELEGATECALL", "UNPROTECTED_PRIVILEGED", "REENTRANCY_PATTERN"}.issubset(found)
