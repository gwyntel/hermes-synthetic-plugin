# Synthetic.new Plugin for Hermes Agent

Adds `synthetic_zdr_search` (web search) and `synthetic_quota_check` (quota check) tools.

## Install

1. `hermes plugins install gwyntel/hermes-synthetic-plugin`
2. Add `SYNTHETIC_API_KEY=your-key` to `~/.hermes/.env`
3. `hermes tools enable synthetic`
4. `/reset`

Get an API key at https://synthetic.new

## Agent Prompt

```
Install the Synthetic.new search plugin for Hermes Agent. This adds `synthetic_zdr_search` (web search via Synthetic.new ZDR API) and `synthetic_quota_check` (check remaining API quota, free call).

1. Install the plugin: `hermes plugins install gwyntel/hermes-synthetic-plugin`
2. Ensure `SYNTHETIC_API_KEY` is set in `~/.hermes/.env`. If missing, ask the user for their key (get one at https://synthetic.new) and append it.
3. Enable the synthetic toolset: `hermes tools enable synthetic`
4. Tell the user to `/reset` or start a new session for changes to take effect.

Repo: https://github.com/gwyntel/hermes-synthetic-plugin
```

## Tools

- **`synthetic_zdr_search`** — Web search via Synthetic.new ZDR API. Returns titles, URLs, descriptions. No page extraction (use `web_extract` separately).
- **`synthetic_quota_check`** — Check remaining API quota. Free call, doesn't count against limits.

## License

WTFPL
