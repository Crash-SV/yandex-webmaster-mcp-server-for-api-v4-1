# Yandex Webmaster MCP Server

MCP server for Yandex Webmaster API v4.1 — full coverage of indexing, search queries, diagnostics, recrawl, sitemaps, links, and important URLs monitoring.

## Features

37 tools covering the complete Yandex Webmaster API:

- **User & Hosts** — list sites, add/remove hosts, get host info
- **Verification** — check verification status, start verification, list owners
- **Summary & SQI** — site summary with quality index, SQI history over time
- **Search Queries** — popular queries (TOP-3000), query history with positions/clicks/shows, single query history, advanced query analytics
- **Recrawl** — check quota, submit URLs for reindexing, track recrawl tasks
- **Diagnostics** — site problems and recommendations
- **Indexing** — indexing history by HTTP status, indexed page samples
- **Important URLs** — monitoring of critical pages, change tracking
- **Search URLs** — pages in search (history + samples), appearance/disappearance events
- **Sitemaps** — auto-detected and user-added sitemaps management
- **Links** — external backlinks, broken internal links

## Installation

```bash
pip install -e .
```

## Configuration

### Environment variable

```bash
export YANDEX_WEBMASTER_API_KEY=your_oauth_token
```

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "yandex-webmaster": {
      "command": "python",
      "args": ["/path/to/yandex-webmaster-mcp-server-python/src/yandex_webmaster_mcp/server.py"],
      "env": {
        "YANDEX_WEBMASTER_API_KEY": "your_oauth_token"
      }
    }
  }
}
```

### Claude Code

Add to your `settings.json`:

```json
{
  "mcpServers": {
    "yandex-webmaster": {
      "command": "python",
      "args": ["/path/to/yandex-webmaster-mcp-server-python/src/yandex_webmaster_mcp/server.py"],
      "env": {
        "YANDEX_WEBMASTER_API_KEY": "your_oauth_token"
      }
    }
  }
}
```

## Getting an OAuth Token

1. Create an app at https://oauth.yandex.ru/client/new
2. Select scopes: `webmaster:hostinfo` and `webmaster:verify`
3. Get token at: `https://oauth.yandex.ru/authorize?response_type=token&client_id=YOUR_CLIENT_ID`
4. Token is valid for 6 months

## Usage Examples

```
# Get your user ID
get_user_id()

# List all sites
get_hosts(user_id="12345")

# Get popular search queries with positions
get_popular_queries(
    user_id="12345",
    host_id="https:example.com:443",
    date_from="2026-03-01",
    date_to="2026-03-31",
    query_indicator="TOTAL_SHOWS,TOTAL_CLICKS,AVG_SHOW_POSITION"
)

# Submit a page for recrawl
request_recrawl(
    user_id="12345",
    host_id="https:example.com:443",
    url="https://example.com/updated-page/"
)

# Get important pages monitoring
get_important_urls(
    user_id="12345",
    host_id="https:example.com:443"
)
```

## host_id Format

Yandex Webmaster uses a special format for host IDs:
- `https:example.com:443` (not a URL — protocol:domain:port without slashes)
- `http:example.com:80`

The server automatically URL-encodes host_id in API requests.

## License

MIT
