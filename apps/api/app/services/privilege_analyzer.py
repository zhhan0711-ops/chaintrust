import json,re
from app.schemas.chain_data import PrivilegeSignal
RULES=[('ownership','owner|admin|operator'),('emergency_control','pause|unpause'),('upgradeability','upgradeTo|upgradeAndCall|setImplementation'),('asset_authority','mint|burn|withdraw'),('ownership_mutation','transferOwnership|renounceOwnership')]
def analyze_privileges(source=None,abi=None):
    if not source and not abi: return []
    names=[]
    if abi:
        try: names += [x.get('name','') for x in (json.loads(abi) if isinstance(abi,str) else abi) if x.get('type')=='function']
        except (ValueError,TypeError): pass
    names += re.findall(r'function\s+(\w+)',source or '')
    out=[]
    for name in set(names):
        category=next((c for c,p in RULES if re.search(p,name,re.I)),None)
        if category:
            evidence=next((line.strip() for line in (source or '').splitlines() if f'function {name}' in line),name)
            confirmed=bool(re.search(r'onlyOwner|onlyRole|require\s*\(',evidence)) or bool(abi)
            out.append(PrivilegeSignal(function_name=name,category=category,access_signal='verified ABI' if abi else 'source function signature',evidence=evidence,evidence_type='source_code',confidence='confirmed' if confirmed else 'heuristic'))
    return out