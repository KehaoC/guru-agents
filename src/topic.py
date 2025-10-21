import json, requests, xml.etree.ElementTree as ET
from claude_agent_sdk import create_sdk_mcp_server, tool
from utils import parse_feeds
from typing import Any

RSS_DICT = {
    # "raddit": "https://www.reddit.com/r/worldnews/.rss", # raddit/worldnews
    # "google": "https://news.google.com/rss?hl=en-SG&gl=SG&ceid=SG:en", # sg first as a test kinda serious
    "tiktok": "https://www.thesun.co.uk/topic/tiktok/feed/"
}


async def _fetch_trends_from_rss():
    trends = []
    for source, url in RSS_DICT.items():
        items = await parse_feeds(url, source)

        for item in items:
            trends.append(item)
    return trends


@tool("fetch_trends_from_rss", "Fetching heated topics from selected rss source.", {})
async def fetch_trends_from_rss(args: dict[str: Any]):
    try:
        all_trends = await _fetch_trends_from_rss()
        print(f"DEBUG: Fetched {len(all_trends)} trends")  # 调试信息

        # 暂时先返回前几条 方便调试
        trends = all_trends[:5]

        # 按照 SDK 要求的格式返回
        result = {
            "total_count": len(all_trends),
            "returned_count": len(trends),
            "trends": trends
        }

        # 注意啊，有标准形式 {"content": [{"type": "text", "text": "..."}]}
        return {
            "content": [{
                "type": "text",
                "text": json.dumps(result, ensure_ascii=False, indent=2)
            }]
        }
    except Exception as e:
        import traceback
        error_msg = f"Error fetching trends: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)  # 调试用
        return {
            "content": [{
                "type": "text",
                "text": f"Error: {error_msg}"
            }]
        }

topic_server = create_sdk_mcp_server(
    "topic-mcp",
    "1.0.0",
    [fetch_trends_from_rss]
)

if __name__ == "__main__":
    import asyncio
    # trends = fetch_trends()
    # print(json.dumps(trends, ensure_ascii=False, indent=2))

    trends = asyncio.run(_fetch_trends_from_rss())
    for item in trends:
        print(json.dumps(item, indent=4))
        break