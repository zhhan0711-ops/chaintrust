from dataclasses import dataclass
import re

@dataclass
class RuleFinding:
    rule_id: str
    title: str
    severity: str
    evidence: str
    description: str
    suggestion: str

def _line(code: str, pos: int) -> str:
    line_no = code[:pos].count("\n") + 1
    return f"Line {line_no}: {code.splitlines()[line_no - 1].strip()}"

def scan(code: str) -> list[RuleFinding]:
    findings: list[RuleFinding] = []
    patterns = [
        ("TX_ORIGIN", "tx.origin authentication", "high", r"tx\.origin", "tx.origin can be controlled through an intermediary contract.", "Use msg.sender and explicit role-based access control."),
        ("DELEGATECALL", "delegatecall usage", "high", r"\.delegatecall\s*\(", "delegatecall executes another contract's code in this contract's storage context.", "Restrict implementation targets and validate upgrade authorization."),
    ]
    for rule_id, title, severity, pattern, description, suggestion in patterns:
        for match in re.finditer(pattern, code):
            findings.append(RuleFinding(rule_id, title, severity, _line(code, match.start()), description, suggestion))
    for match in re.finditer(r"\.call\s*\{?[^;\n]*\}?\s*\([^;\n]*\)\s*;", code):
        line_start = code.rfind("\n", 0, match.start()) + 1
        assignment = code[line_start:match.start()]
        result_var = re.search(r"bool\s+(\w+)", assignment)
        is_checked = bool(result_var and re.search(rf"(?:require|if)\s*\(\s*{re.escape(result_var.group(1))}\b", code[match.end():match.end() + 280]))
        if "=" not in assignment or not is_checked:
            findings.append(RuleFinding("UNCHECKED_LOW_LEVEL_CALL", "Unchecked low-level external call", "medium", _line(code, match.start()), "A low-level call result appears to be ignored, causing silent failure.", "Capture the success flag and revert or handle failure explicitly."))
    for match in re.finditer(r"function\s+(?:withdraw|setOwner|set[A-Z]\w*|upgrade\w*)\s*\([^)]*\)\s*(?:external|public)", code):
        window = code[match.start():min(len(code), match.end() + 220)]
        if not re.search(r"onlyOwner|onlyRole|require\s*\(.*msg\.sender", window, re.S):
            findings.append(RuleFinding("UNPROTECTED_PRIVILEGED", "Potentially unprotected privileged function", "high", _line(code, match.start()), "A sensitive-looking public/external function lacks a nearby access-control pattern.", "Add appropriate authorization and tests for all privileged paths."))
    external = list(re.finditer(r"(?:\.call|\.transfer|\.send)\s*(?:\{|\()", code))
    for event in external:
        before = code[max(0, event.start() - 350):event.start()]
        after = code[event.start():min(len(code), event.start() + 500)]
        if re.search(r"(balance|balances|credit)\s*\[.*\]\s*(?:-=|=\s*0)", after) and not re.search(r"(balance|balances|credit)\s*\[.*\]\s*(?:-=|=\s*0)", before):
            findings.append(RuleFinding("REENTRANCY_PATTERN", "Reentrancy-related interaction ordering", "high", _line(code, event.start()), "An external value transfer appears before a nearby balance update.", "Apply checks-effects-interactions and consider a reentrancy guard."))
    return findings
