"""Synthetic.new search implementation."""

import json
import logging
import os

logger = logging.getLogger(__name__)

_SYNTHETIC_SEARCH_URL = "https://api.synthetic.new/v2/search"


def synthetic_zdr_search_check() -> bool:
    """Return True when SYNTHETIC_API_KEY is available."""
    return bool(os.getenv("SYNTHETIC_API_KEY", "").strip())


def synthetic_zdr_search_handler(args, **kwargs) -> str:
    """Handle synthetic_zdr_search tool calls.

    Calls POST https://api.synthetic.new/v2/search with Bearer auth.
    Returns JSON matching Hermes web search format:
    {success: bool, data: {web: [{url, title, description, position}]}}
    """
    query = args.get("query", "")
    if not query:
        return json.dumps({"error": "No search query provided", "success": False})

    # Check for interrupt
    try:
        from tools.interrupt import is_interrupted
        if is_interrupted():
            return json.dumps({"error": "Interrupted", "success": False})
    except ImportError:
        pass

    api_key = os.getenv("SYNTHETIC_API_KEY")
    if not api_key:
        return json.dumps({
            "error": "SYNTHETIC_API_KEY not set. Get your key at https://synthetic.new",
            "success": False,
        })

    logger.info("Synthetic ZDR search: '%s'", query)

    try:
        import httpx
        response = httpx.post(
            _SYNTHETIC_SEARCH_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            json={"query": query},
            timeout=30.0,
        )
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPStatusError as e:
        return json.dumps({
            "error": f"Synthetic API error: {e.response.status_code}",
            "success": False,
        })
    except httpx.TimeoutException:
        return json.dumps({"error": "Synthetic API timed out (30s)", "success": False})
    except Exception as e:
        return json.dumps({"error": f"Synthetic search failed: {e}", "success": False})

    # Normalize to Hermes web search format
    web_results = []
    for i, result in enumerate(data.get("results", [])):
        web_results.append({
            "url": result.get("url", ""),
            "title": result.get("title", ""),
            "description": result.get("text", ""),
            "position": i + 1,
        })

    return json.dumps({"success": True, "data": {"web": web_results}}, indent=2, ensure_ascii=False)
