import re
from hashlib import sha256
NORMALIZATION_VERSION='solidity-v1'
def normalize_source(value:str)->str:
    lines=[line.rstrip() for line in value.replace('\r\n','\n').replace('\r','\n').split('\n')]
    output=[]; blank=False
    for line in lines:
        if not line:
            if not blank: output.append('')
            blank=True
        else: output.append(line); blank=False
    return '\n'.join(output).strip()+'\n'
def source_hash(value:str)->str: return sha256(normalize_source(value).encode()).hexdigest()
def binding(submitted:str|None, verified:str|None, input_mode:str)->dict:
    if input_mode!='source + address review': return {'submitted_source_hash':source_hash(submitted) if submitted else None,'verified_source_hash':None,'source_match_status':'not_applicable','verification_method':'not_applicable','limitation':None}
    submitted_hash=source_hash(submitted or '')
    if not verified: return {'submitted_source_hash':submitted_hash,'verified_source_hash':None,'source_match_status':'unavailable','verification_method':'explorer_verified_source','limitation':'Verified source is unavailable or could not be parsed.'}
    verified_hash=source_hash(verified); status='matched' if submitted_hash==verified_hash else 'mismatch'
    return {'submitted_source_hash':submitted_hash,'verified_source_hash':verified_hash,'source_match_status':status,'verification_method':'normalized_sha256','limitation':None if status=='matched' else 'Submitted source does not match explorer verified source.'}