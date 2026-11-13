import re

def funcs(s): return set(re.findall(r'function\s+(\w+)\s*\([^)]*\)\s*(?:external|public)',s))
def vars(s): return dict(re.findall(r'\b([A-Za-z]\w*)\s+(?:public|private|internal)?\s*(\w+)\s*;',s))
def review(base,candidate):
 b,c=funcs(base),funcs(candidate); added=sorted(c-b); removed=sorted(b-c)
 high=[x for x in added if re.search(r'upgrade|delegatecall|mint|burn|withdraw|pause|admin|owner',x,re.I)]
 low_call=bool(re.search(r'\.call|\.delegatecall',candidate)) and not bool(re.search(r'\.call|\.delegatecall',base))
 risks=[{'kind':'new_low_level_call','confidence':'heuristic'}] if low_call else []
 readiness='blocked' if any(re.search(r'delegatecall|upgrade',x,re.I) for x in high) else 'review_required' if high or risks else 'ready' if base and candidate else 'unknown'
 return {'release_readiness':readiness,'material_changes':{'added_functions':added,'removed_functions':removed},'newly_introduced_risks':risks,'removed_risks':[],'privilege_surface_changes':[x for x in high if re.search(r'pause|admin|owner|mint|burn|withdraw',x,re.I)],'upgradeability_changes':[x for x in high if re.search(r'upgrade|delegatecall',x,re.I)],'required_manual_checks':['Confirm storage layout compatibility; static source diff cannot reliably prove layout safety.'],'evidence_and_confidence':[{'evidence_type':'source_code','confidence':'heuristic'}],'limitations':['This Change Review supports engineering review workflows and does not replace a professional security audit.']}