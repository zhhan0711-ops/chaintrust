import json
import httpx
from app.core.config import settings

ETHERSCAN_V2_URL = "https://api.etherscan.io/v2/api"

def resolve_sepolia_source(address: str) -> str:
    """Fetch verified source from Etherscan V2 for Sepolia only; never queries a production chain."""
    if not settings.etherscan_api_key or settings.etherscan_api_key == "[TO CONFIGURE]":
        raise ValueError("Sepolia address analysis needs ETHERSCAN_API_KEY. It is currently [TO CONFIGURE].")
    params = {"chainid": "11155111", "module": "contract", "action": "getsourcecode", "address": address, "apikey": settings.etherscan_api_key}
    try:
        response = httpx.get(ETHERSCAN_V2_URL, params=params, timeout=10.0)
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPError as exc:
        raise ValueError("Could not retrieve verified Sepolia source from the configured explorer.") from exc
    result = data.get("result") or []
    item = result[0] if isinstance(result, list) and result else {}
    source = item.get("SourceCode", "")
    if not source:
        raise ValueError("No verified source code was returned for this Sepolia address.")
    if source.startswith("{{") and source.endswith("}}"):
        source = source[1:-1]
    try:
        parsed = json.loads(source)
        files = parsed.get("sources", {})
        if files:
            source = "\n\n".join(file.get("content", "") for file in files.values())
    except (ValueError, AttributeError):
        pass
    return source
