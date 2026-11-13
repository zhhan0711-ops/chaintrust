from hashlib import sha256

def digest(value: str) -> str:
    return "0x" + sha256(value.encode("utf-8")).hexdigest()
