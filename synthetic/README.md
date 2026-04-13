# Synthetic.new Plugin for Hermes Agent

Adds `synthetic_zdr_search` and `synthetic_quota_check` tools.

## Setup

1. **Set your API key** in `~/.hermes/.env`:
   ```
   SYNTHETIC_API_KEY=your-key-here
   ```
   Get a key at https://synthetic.new

2. **Copy the plugin** to your plugins directory:
   ```
   cp -r synthetic ~/.hermes/plugins/
   ```

3. **Enable the synthetic toolset** — run `hermes tools` and toggle 🔌 Synthetic on for each platform, or set it directly:
   ```
   hermes tools enable synthetic
   ```

4. **Start a new session** — toolset changes take effect on `/reset` or fresh session.

## Tools

- **`synthetic_zdr_search`** — Web search via Synthetic.new ZDR API. Returns titles, URLs, descriptions. No page extraction (use `web_extract` separately).
- **`synthetic_quota_check`** — Check remaining API quota. Free call, doesn't count against limits.

## File structure

```
synthetic/
├── plugin.yaml
├── __init__.py
├── search.py
└── quota.py
```
