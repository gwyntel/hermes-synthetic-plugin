"""Synthetic.new search plugin for Hermes Agent."""

from hermes_plugins.synthetic.search import synthetic_zdr_search_handler, synthetic_zdr_search_check
from hermes_plugins.synthetic.quota import synthetic_quota_check_handler, synthetic_quota_check_fn


def register(ctx):
    """Register Synthetic.new tools."""

    # ── synthetic_zdr_search tool ──
    ctx.register_tool(
        name="synthetic_zdr_search",
        toolset="synthetic",
        schema={
            "name": "synthetic_zdr_search",
            "description": (
                "Search the web using Synthetic.new ZDR API. "
                "Returns results with titles, URLs, and descriptions. "
                "Synthetic is fast and privacy-focused. "
                "Note: Synthetic does NOT support page extraction — "
                "use web_extract for full page content."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look up on the web",
                    },
                },
                "required": ["query"],
            },
        },
        handler=synthetic_zdr_search_handler,
        check_fn=synthetic_zdr_search_check,
        requires_env=["SYNTHETIC_API_KEY"],
        is_async=False,
        description="Search the web using Synthetic.new ZDR API",
        emoji="🔬",
    )

    # ── synthetic_quota_check tool ──
    ctx.register_tool(
        name="synthetic_quota_check",
        toolset="synthetic",
        schema={
            "name": "synthetic_quota_check",
            "description": (
                "Check your Synthetic.new API quota — remaining requests, "
                "search limits, and token budget. This call is free and "
                "doesn't count against your limits."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
        handler=synthetic_quota_check_handler,
        check_fn=synthetic_quota_check_fn,
        requires_env=["SYNTHETIC_API_KEY"],
        is_async=False,
        description="Check Synthetic.new API quota",
        emoji="📊",
    )
