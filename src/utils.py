import xml.etree.ElementTree as ET
from io import BytesIO

import httpx


async def parse_feeds(url: str, source: str) -> list[dict]:
    """
    Parse RSS/Atom feeds from different sources and extract items.

    Args:
        url: The RSS feed URL
        source: The source type ('reddit' or 'google')

    Returns:
        List of dictionaries containing feed items
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        content = response.content

    # Parse XML from response content
    tree = ET.parse(BytesIO(content))
    root = tree.getroot()

    items = []

    if source == 'reddit':
        # Atom namespace for Reddit feeds
        ns = {'atom': 'http://www.w3.org/2005/Atom',
              'media': 'http://search.yahoo.com/mrss/'}

        # Find all entry elements
        for entry in root.findall('atom:entry', ns):
            # Extract title
            title_elem = entry.find('atom:title', ns)
            title = title_elem.text if title_elem is not None else ''

            # Extract link (URL)
            link_elem = entry.find('atom:link', ns)
            url = link_elem.get('href') if link_elem is not None else ''

            # Extract content as description (HTML)
            content_elem = entry.find('atom:content', ns)
            description = content_elem.text if content_elem is not None else ''

            # Extract published date
            published_elem = entry.find('atom:published', ns)
            published = published_elem.text if published_elem is not None else ''

            # Create unified item structure
            item = {
                'title': title,
                'url': url,
                # 'description': description,
                'published': published
            }

            items.append(item)

    elif source == 'google' or source == 'tiktok':
        # RSS 2.0 format for Google News
        # Find all item elements (RSS 2.0 uses 'item' instead of 'entry')
        for item_elem in root.findall('.//item'):
            # Extract title
            title_elem = item_elem.find('title')
            title = title_elem.text if title_elem is not None else ''

            # Extract link (URL)
            link_elem = item_elem.find('link')
            url = link_elem.text if link_elem is not None else ''

            # Extract description (contains related articles in HTML)
            desc_elem = item_elem.find('description')
            description = desc_elem.text if desc_elem is not None else ''

            # Extract published date (pubDate in RSS 2.0)
            pub_date_elem = item_elem.find('pubDate')
            published = pub_date_elem.text if pub_date_elem is not None else ''

            # Create unified item structure
            item = {
                'title': title,
                'url': url,
                # 'description': description,
                'published': published
            }

            items.append(item)

    return items


# Example usage
if __name__ == '__main__':
    import asyncio

    async def test_feeds():
        # print("=" * 80)
        # print("Testing Reddit RSS Feed")
        # print("=" * 80)

        # # # Test Reddit RSS parsing
        # reddit_items = await parse_feeds("https://www.reddit.com/r/worldnews/.rss", "reddit")
        # print(f"Found {len(reddit_items)} Reddit items\n")

        # # Print first 2 items
        # for i, item in enumerate(reddit_items[:2], 1):
        #     print(f"--- Reddit Item {i} ---")
        #     print(f"Title: {item['title']}")
        #     print(f"URL: {item['url']}")
        #     print(f"Published: {item['published']}")
        #     print()

        # print("\n" + "=" * 80)
        # print("Testing Google News RSS Feed")
        # print("=" * 80)

        # # Test Google News RSS parsing
        # google_items = await parse_feeds(
        #     "https://news.google.com/rss?hl=en-SG&gl=SG&ceid=SG:en",
        #     "google"
        # )
        # print(f"Found {len(google_items)} Google News items\n")

        # # Print first 2 items
        # for i, item in enumerate(google_items[:2], 1):
        #     print(f"--- Google News Item {i} ---")
        #     print(f"Title: {item['title']}")
        #     print(f"URL: {item['url'][:80]}...")
        #     print(f"Published: {item['published']}")
        #     print()

        # Test Google News RSS parsing
        google_items = await parse_feeds(
            "https://www.thesun.co.uk/topic/tiktok/feed/",
            "tiktok"
        )
        print(f"Found {len(google_items)} Google News items\n")

        # Print first 2 items
        for i, item in enumerate(google_items[:2], 1):
            print(f"--- Google News Item {i} ---")
            print(f"Title: {item['title']}")
            print(f"URL: {item['url'][:80]}...")
            print(f"Published: {item['published']}")
            print()

    asyncio.run(test_feeds())

