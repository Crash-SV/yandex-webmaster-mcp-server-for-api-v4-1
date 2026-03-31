"""Yandex Webmaster MCP Server — full API v4.1 coverage (37 tools)."""

import json
import os
from fastmcp import FastMCP
from yandex_webmaster_mcp.client import WebmasterClient, WebmasterAPIError

mcp = FastMCP(
    "Yandex Webmaster",
    description="MCP server for Yandex Webmaster API v4.1 — indexing, search queries, diagnostics, recrawl, sitemaps, links, and more.",
)

_client: WebmasterClient | None = None


def get_client() -> WebmasterClient:
    global _client
    if _client is None:
        _client = WebmasterClient()
    return _client


def _ok(data) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def _err(e: WebmasterAPIError) -> str:
    return json.dumps(
        {"error": True, "error_code": e.error_code, "message": e.message, "status": e.status_code},
        ensure_ascii=False,
    )


# ═══════════════════════════════════════════════════════════════
# 1. USER & HOSTS
# ═══════════════════════════════════════════════════════════════


@mcp.tool
def get_user_id() -> str:
    """Get authenticated Yandex Webmaster user ID."""
    try:
        data = get_client().get("/user")
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_hosts(user_id: str) -> str:
    """Get list of all sites added to Yandex Webmaster.

    Args:
        user_id: Yandex Webmaster user ID
    """
    try:
        data = get_client().get(f"/user/{user_id}/hosts")
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def add_host(user_id: str, host_url: str) -> str:
    """Add a new site to Yandex Webmaster.

    Args:
        user_id: Yandex Webmaster user ID
        host_url: Site URL to add (e.g. https://example.com)
    """
    try:
        data = get_client().post(f"/user/{user_id}/hosts", json_body={"host_url": host_url})
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_host_info(user_id: str, host_id: str) -> str:
    """Get detailed information about a specific site.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
    """
    try:
        c = get_client()
        data = c.get(f"{c.host_url(user_id, host_id)}")
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def delete_host(user_id: str, host_id: str) -> str:
    """Remove a site from Yandex Webmaster.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
    """
    try:
        c = get_client()
        c.delete(f"{c.host_url(user_id, host_id)}")
        return _ok({"status": "deleted", "host_id": host_id})
    except WebmasterAPIError as e:
        return _err(e)


# ═══════════════════════════════════════════════════════════════
# 2. VERIFICATION
# ═══════════════════════════════════════════════════════════════


@mcp.tool
def get_verification_status(user_id: str, host_id: str) -> str:
    """Get site verification status.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
    """
    try:
        c = get_client()
        data = c.get(f"{c.host_url(user_id, host_id)}/verification")
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def verify_host(user_id: str, host_id: str, verification_type: str) -> str:
    """Start site verification process.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        verification_type: Verification method: DNS, HTML_FILE, or META_TAG
    """
    try:
        c = get_client()
        data = c.post(
            f"{c.host_url(user_id, host_id)}/verification",
            params={"verification_type": verification_type},
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_host_owners(user_id: str, host_id: str) -> str:
    """Get list of verified site owners/managers.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
    """
    try:
        c = get_client()
        data = c.get(f"{c.host_url(user_id, host_id)}/owners")
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


# ═══════════════════════════════════════════════════════════════
# 3. SUMMARY & SQI
# ═══════════════════════════════════════════════════════════════


@mcp.tool
def get_summary(user_id: str, host_id: str) -> str:
    """Get site summary: SQI, indexed pages count, site problems count.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
    """
    try:
        c = get_client()
        data = c.get(f"{c.host_url(user_id, host_id)}/summary")
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_sqi_history(
    user_id: str,
    host_id: str,
    date_from: str | None = None,
    date_to: str | None = None,
) -> str:
    """Get Site Quality Index (SQI/ИКС) history over time.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        date_from: Start date (YYYY-MM-DD), optional
        date_to: End date (YYYY-MM-DD), optional
    """
    try:
        c = get_client()
        data = c.get(
            f"{c.host_url(user_id, host_id)}/sqi-history",
            params={"date_from": date_from, "date_to": date_to},
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


# ═══════════════════════════════════════════════════════════════
# 4. SEARCH QUERIES
# ═══════════════════════════════════════════════════════════════


@mcp.tool
def get_popular_queries(
    user_id: str,
    host_id: str,
    date_from: str,
    date_to: str,
    order_by: str = "TOTAL_SHOWS",
    query_indicator: str | None = None,
    device_type_indicator: str | None = None,
    limit: int = 500,
    offset: int = 0,
) -> str:
    """Get TOP-3000 popular search queries with indicators (shows, clicks, positions).

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        date_from: Start date (YYYY-MM-DD)
        date_to: End date (YYYY-MM-DD)
        order_by: Sort by TOTAL_SHOWS or TOTAL_CLICKS
        query_indicator: Comma-separated indicators: TOTAL_SHOWS,TOTAL_CLICKS,AVG_SHOW_POSITION,AVG_CLICK_POSITION
        device_type_indicator: ALL, DESKTOP, MOBILE, PHONE, TABLET
        limit: Results per page (1-500, default 500)
        offset: Pagination offset
    """
    try:
        c = get_client()
        indicators = query_indicator.split(",") if query_indicator else None
        data = c.get(
            f"{c.host_url(user_id, host_id)}/search-queries/popular",
            params={
                "order_by": order_by,
                "query_indicator": indicators,
                "device_type_indicator": device_type_indicator,
                "date_from": date_from,
                "date_to": date_to,
                "limit": limit,
                "offset": offset,
            },
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_query_history(
    user_id: str,
    host_id: str,
    date_from: str,
    date_to: str,
    query_indicator: str | None = None,
    device_type_indicator: str | None = None,
) -> str:
    """Get aggregated search query statistics (all queries) over time — shows, clicks, positions by day.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        date_from: Start date (YYYY-MM-DD)
        date_to: End date (YYYY-MM-DD)
        query_indicator: Comma-separated: TOTAL_SHOWS,TOTAL_CLICKS,AVG_SHOW_POSITION,AVG_CLICK_POSITION
        device_type_indicator: ALL, DESKTOP, MOBILE, PHONE, TABLET
    """
    try:
        c = get_client()
        indicators = query_indicator.split(",") if query_indicator else None
        data = c.get(
            f"{c.host_url(user_id, host_id)}/search-queries/all/history",
            params={
                "query_indicator": indicators,
                "device_type_indicator": device_type_indicator,
                "date_from": date_from,
                "date_to": date_to,
            },
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_single_query_history(
    user_id: str,
    host_id: str,
    query_id: str,
    date_from: str,
    date_to: str,
    query_indicator: str | None = None,
    device_type_indicator: str | None = None,
) -> str:
    """Get search statistics history for a specific query (by query_id from get_popular_queries).

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        query_id: Query ID from get_popular_queries response
        date_from: Start date (YYYY-MM-DD)
        date_to: End date (YYYY-MM-DD)
        query_indicator: Comma-separated: TOTAL_SHOWS,TOTAL_CLICKS,AVG_SHOW_POSITION,AVG_CLICK_POSITION
        device_type_indicator: ALL, DESKTOP, MOBILE, PHONE, TABLET
    """
    try:
        c = get_client()
        indicators = query_indicator.split(",") if query_indicator else None
        data = c.get(
            f"{c.host_url(user_id, host_id)}/search-queries/{query_id}/history",
            params={
                "query_indicator": indicators,
                "device_type_indicator": device_type_indicator,
                "date_from": date_from,
                "date_to": date_to,
            },
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_query_analytics(
    user_id: str,
    host_id: str,
    limit: int = 20,
    offset: int = 0,
    device_type_indicator: str = "ALL",
    text_indicator: str = "QUERY",
    text_filter: str | None = None,
    text_filter_operation: str = "TEXT_CONTAINS",
    sort_field: str | None = None,
    sort_date: str | None = None,
    sort_direction: str = "DESC",
    region_ids: str | None = None,
) -> str:
    """Advanced search query analytics (POST). Data for last 2 weeks only.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        limit: Results per page (1-500, default 20)
        offset: Pagination offset
        device_type_indicator: ALL, DESKTOP, MOBILE_AND_TABLET, MOBILE, TABLET
        text_indicator: QUERY (group by query) or URL (group by URL)
        text_filter: Text filter value (e.g. "купить" to filter queries containing this word)
        text_filter_operation: TEXT_CONTAINS, TEXT_MATCH, TEXT_DOES_NOT_CONTAIN
        sort_field: Sort by: IMPRESSIONS, POSITION, CLICKS, CTR, DEMAND
        sort_date: Date to sort by (YYYY-MM-DD)
        sort_direction: ASC or DESC
        region_ids: Comma-separated region IDs (e.g. "225" for Russia)
    """
    try:
        c = get_client()
        body: dict = {
            "offset": offset,
            "limit": limit,
            "device_type_indicator": device_type_indicator,
            "text_indicator": text_indicator,
        }
        if text_filter:
            body["filters"] = {
                "text_filters": [{"text_indicator": text_indicator, "operation": text_filter_operation, "value": text_filter}]
            }
        if sort_field and sort_date:
            body["sort_by_date"] = {"date": sort_date, "statistic_field": sort_field, "by": sort_direction}
        if region_ids:
            body["region_ids"] = [int(x.strip()) for x in region_ids.split(",")]

        data = c.post(f"{c.host_url(user_id, host_id)}/query-analytics/list", json_body=body)
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


# ═══════════════════════════════════════════════════════════════
# 5. RECRAWL
# ═══════════════════════════════════════════════════════════════


@mcp.tool
def get_recrawl_quota(user_id: str, host_id: str) -> str:
    """Get daily recrawl quota (how many URLs can be submitted per day).

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
    """
    try:
        c = get_client()
        data = c.get(f"{c.host_url(user_id, host_id)}/recrawl/quota")
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def request_recrawl(user_id: str, host_id: str, url: str) -> str:
    """Submit a URL for recrawl/reindexing by Yandex.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        url: Full URL to recrawl (e.g. https://example.com/page/)
    """
    try:
        c = get_client()
        data = c.post(f"{c.host_url(user_id, host_id)}/recrawl/queue", json_body={"url": url})
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_recrawl_tasks(
    user_id: str,
    host_id: str,
    date_from: str | None = None,
    date_to: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> str:
    """Get list of recrawl tasks.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        date_from: Filter by date from (YYYY-MM-DD)
        date_to: Filter by date to (YYYY-MM-DD)
        limit: Results per page (default 50)
        offset: Pagination offset
    """
    try:
        c = get_client()
        data = c.get(
            f"{c.host_url(user_id, host_id)}/recrawl/queue",
            params={"date_from": date_from, "date_to": date_to, "limit": limit, "offset": offset},
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_recrawl_task_status(user_id: str, host_id: str, task_id: str) -> str:
    """Get status of a specific recrawl task.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        task_id: Recrawl task UUID
    """
    try:
        c = get_client()
        data = c.get(f"{c.host_url(user_id, host_id)}/recrawl/queue/{task_id}")
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


# ═══════════════════════════════════════════════════════════════
# 6. DIAGNOSTICS
# ═══════════════════════════════════════════════════════════════


@mcp.tool
def get_diagnostics(user_id: str, host_id: str) -> str:
    """Get site diagnostics — problems and recommendations (FATAL, CRITICAL, etc.).

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
    """
    try:
        c = get_client()
        data = c.get(f"{c.host_url(user_id, host_id)}/diagnostics")
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


# ═══════════════════════════════════════════════════════════════
# 7. INDEXING
# ═══════════════════════════════════════════════════════════════


@mcp.tool
def get_indexing_history(
    user_id: str,
    host_id: str,
    date_from: str,
    date_to: str,
) -> str:
    """Get indexing history — number of indexed pages by HTTP status over time.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        date_from: Start date (YYYY-MM-DD)
        date_to: End date (YYYY-MM-DD)
    """
    try:
        c = get_client()
        data = c.get(
            f"{c.host_url(user_id, host_id)}/indexing/history",
            params={"date_from": date_from, "date_to": date_to},
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_indexing_samples(
    user_id: str,
    host_id: str,
    limit: int = 50,
    offset: int = 0,
) -> str:
    """Get samples of indexed pages (up to 50,000 URLs).

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        limit: Results per page (1-100, default 50)
        offset: Pagination offset
    """
    try:
        c = get_client()
        data = c.get(
            f"{c.host_url(user_id, host_id)}/indexing/samples",
            params={"limit": limit, "offset": offset},
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


# ═══════════════════════════════════════════════════════════════
# 8. IMPORTANT URLS
# ═══════════════════════════════════════════════════════════════


@mcp.tool
def get_important_urls(user_id: str, host_id: str) -> str:
    """Get monitoring data for important pages — indexing status, search status, change indicators.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
    """
    try:
        c = get_client()
        data = c.get(f"{c.host_url(user_id, host_id)}/important-urls")
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_important_url_history(user_id: str, host_id: str, url: str) -> str:
    """Get monitoring history for a specific important URL.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        url: Full URL to check history for (e.g. https://example.com/page/)
    """
    try:
        c = get_client()
        data = c.get(
            f"{c.host_url(user_id, host_id)}/important-urls/history",
            params={"url": url},
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


# ═══════════════════════════════════════════════════════════════
# 9. SEARCH URLS — pages in search
# ═══════════════════════════════════════════════════════════════


@mcp.tool
def get_search_urls_history(
    user_id: str,
    host_id: str,
    date_from: str,
    date_to: str,
) -> str:
    """Get history of pages count in Yandex search results over time.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        date_from: Start date (YYYY-MM-DD)
        date_to: End date (YYYY-MM-DD)
    """
    try:
        c = get_client()
        data = c.get(
            f"{c.host_url(user_id, host_id)}/search-urls/in-search/history",
            params={"date_from": date_from, "date_to": date_to},
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_search_urls_samples(
    user_id: str,
    host_id: str,
    limit: int = 50,
    offset: int = 0,
) -> str:
    """Get samples of pages currently in Yandex search results (up to 50,000).

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        limit: Results per page (1-100, default 50)
        offset: Pagination offset
    """
    try:
        c = get_client()
        data = c.get(
            f"{c.host_url(user_id, host_id)}/search-urls/in-search/samples",
            params={"limit": limit, "offset": offset},
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_search_urls_events_history(
    user_id: str,
    host_id: str,
    date_from: str,
    date_to: str,
) -> str:
    """Get history of pages appearing/disappearing from Yandex search.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        date_from: Start date (YYYY-MM-DD)
        date_to: End date (YYYY-MM-DD)
    """
    try:
        c = get_client()
        data = c.get(
            f"{c.host_url(user_id, host_id)}/search-urls/events/history",
            params={"date_from": date_from, "date_to": date_to},
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_search_urls_events_samples(
    user_id: str,
    host_id: str,
    limit: int = 50,
    offset: int = 0,
) -> str:
    """Get samples of pages that recently appeared or disappeared from Yandex search.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        limit: Results per page (1-100, default 50)
        offset: Pagination offset
    """
    try:
        c = get_client()
        data = c.get(
            f"{c.host_url(user_id, host_id)}/search-urls/events/samples",
            params={"limit": limit, "offset": offset},
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


# ═══════════════════════════════════════════════════════════════
# 10. SITEMAPS
# ═══════════════════════════════════════════════════════════════


@mcp.tool
def get_sitemaps(
    user_id: str,
    host_id: str,
    parent_id: str | None = None,
    limit: int = 10,
    offset_id: str | None = None,
) -> str:
    """Get auto-detected sitemaps.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        parent_id: Parent sitemap ID (for index sitemaps)
        limit: Results per page (1-100, default 10)
        offset_id: Cursor-based pagination (sitemap ID to start from)
    """
    try:
        c = get_client()
        data = c.get(
            f"{c.host_url(user_id, host_id)}/sitemaps",
            params={"parent_id": parent_id, "limit": limit, "from": offset_id},
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_sitemap_info(user_id: str, host_id: str, sitemap_id: str) -> str:
    """Get details of an auto-detected sitemap.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        sitemap_id: Sitemap ID
    """
    try:
        c = get_client()
        data = c.get(f"{c.host_url(user_id, host_id)}/sitemaps/{sitemap_id}")
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_user_added_sitemaps(
    user_id: str,
    host_id: str,
    limit: int = 100,
    offset: str | None = None,
) -> str:
    """Get list of user-added sitemaps.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        limit: Results per page (1-100, default 100)
        offset: Cursor-based pagination (sitemap ID)
    """
    try:
        c = get_client()
        data = c.get(
            f"{c.host_url(user_id, host_id)}/user-added-sitemaps",
            params={"limit": limit, "offset": offset},
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_user_added_sitemap_info(user_id: str, host_id: str, sitemap_id: str) -> str:
    """Get details of a user-added sitemap.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        sitemap_id: Sitemap ID
    """
    try:
        c = get_client()
        data = c.get(f"{c.host_url(user_id, host_id)}/user-added-sitemaps/{sitemap_id}")
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def add_sitemap(user_id: str, host_id: str, sitemap_url: str) -> str:
    """Add a sitemap to the site.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        sitemap_url: Full URL of the sitemap (e.g. https://example.com/sitemap.xml)
    """
    try:
        c = get_client()
        data = c.post(
            f"{c.host_url(user_id, host_id)}/user-added-sitemaps",
            json_body={"url": sitemap_url},
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def delete_sitemap(user_id: str, host_id: str, sitemap_id: str) -> str:
    """Delete a user-added sitemap.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        sitemap_id: Sitemap ID to delete
    """
    try:
        c = get_client()
        c.delete(f"{c.host_url(user_id, host_id)}/user-added-sitemaps/{sitemap_id}")
        return _ok({"status": "deleted", "sitemap_id": sitemap_id})
    except WebmasterAPIError as e:
        return _err(e)


# ═══════════════════════════════════════════════════════════════
# 11. LINKS
# ═══════════════════════════════════════════════════════════════


@mcp.tool
def get_external_links(
    user_id: str,
    host_id: str,
    limit: int = 10,
    offset: int = 0,
) -> str:
    """Get samples of external links (backlinks) pointing to the site.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        limit: Results per page (1-100, default 10)
        offset: Pagination offset
    """
    try:
        c = get_client()
        data = c.get(
            f"{c.host_url(user_id, host_id)}/links/external/samples",
            params={"limit": limit, "offset": offset},
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_external_links_history(user_id: str, host_id: str) -> str:
    """Get history of external links count over time.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
    """
    try:
        c = get_client()
        data = c.get(
            f"{c.host_url(user_id, host_id)}/links/external/history",
            params={"indicator": "LINKS_TOTAL_COUNT"},
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_internal_broken_links(
    user_id: str,
    host_id: str,
    indicator: str | None = None,
    limit: int = 10,
    offset: int = 0,
) -> str:
    """Get samples of broken internal links.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        indicator: Comma-separated: SITE_ERROR,DISALLOWED_BY_USER,UNSUPPORTED_BY_ROBOT
        limit: Results per page (1-100, default 10)
        offset: Pagination offset
    """
    try:
        c = get_client()
        indicators = indicator.split(",") if indicator else None
        data = c.get(
            f"{c.host_url(user_id, host_id)}/links/internal/broken/samples",
            params={"indicator": indicators, "limit": limit, "offset": offset},
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


@mcp.tool
def get_internal_broken_links_history(
    user_id: str,
    host_id: str,
    date_from: str | None = None,
    date_to: str | None = None,
) -> str:
    """Get history of broken internal links count over time.

    Args:
        user_id: Yandex Webmaster user ID
        host_id: Host ID (format: https:example.com:443)
        date_from: Start date (YYYY-MM-DD)
        date_to: End date (YYYY-MM-DD)
    """
    try:
        c = get_client()
        data = c.get(
            f"{c.host_url(user_id, host_id)}/links/internal/broken/history",
            params={"date_from": date_from, "date_to": date_to},
        )
        return _ok(data)
    except WebmasterAPIError as e:
        return _err(e)


# ═══════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════


def main():
    mcp.run()


if __name__ == "__main__":
    main()
