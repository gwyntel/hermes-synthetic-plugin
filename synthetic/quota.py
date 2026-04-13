"""Synthetic.new quota check implementation."""

import json
import logging
import os

logger = logging.getLogger(__name__)

_SYNTHETIC_QUOTA_URL = "https://api.synthetic.new/v2/quotas"


def synthetic_quota_check_fn() -> bool:
    """Return True when SYNTHETIC_API_KEY is available."""
    return bool(os.getenv("SYNTHETIC_API_KEY", "").strip())


def synthetic_quota_check_handler(args, **kwargs) -> str:
    """Handle synthetic_quota_check tool calls.

    Calls GET https://api.synthetic.new/v2/quotas with Bearer auth.
    This endpoint is free — doesn't count against limits.
    Returns raw quota JSON for the agent to interpret.
    """
    api_key = os.getenv("SYNTHETIC_API_KEY")
    if not api_key:
        return json.dumps({
            "error": "SYNTHETIC_API_KEY not set. Get your key at https://synthetic.new",
            "success": False,
        })

    try:
        import httpx
        response = httpx.get(
            _SYNTHETIC_QUOTA_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=15.0,
        )
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPStatusError as e:
        return json.dumps({
            "error": f"Quota API error: {e.response.status_code}",
            "success": False,
        })
    except httpx.TimeoutException:
        return json.dumps({"error": "Quota API timed out", "success": False})
    except Exception as e:
        return json.dumps({"error": f"Quota check failed: {e}", "success": False})

    # Add a human-readable summary at the top
    sub = data.get("subscription", {})
    search = data.get("search", {}).get("hourly", {})
    free_tools = data.get("freeToolCalls", {})
    weekly = data.get("weeklyTokenLimit", {})

    summary_lines = [
        f"**Synthetic Quota**",
        f"Subscription: {sub.get('requests', '?')}/{sub.get('limit', '?')} requests",
        f"Search (hourly): {search.get('requests', '?')}/{search.get('limit', '?')}",
        f"Free tool calls: {free_tools.get('requests', '?')}/{free_tools.get('limit', '?')}",
    ]
    if weekly.get("percentRemaining") is not None:
        summary_lines.append(f"Weekly token budget: {weekly['percentRemaining']:.1f}% remaining")

    data["_summary"] = "\n".join(summary_lines)

    return json.dumps(data, indent=2, ensure_ascii=False)
