import xml.etree.ElementTree as ET
from io import BytesIO
import os
from pathlib import Path
from urllib.parse import urlparse

import httpx
from dotenv import load_dotenv

load_dotenv()


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

            # Extract image URL from media:thumbnail or media:content
            image_url = ''
            media_thumbnail = entry.find('media:thumbnail', ns)
            if media_thumbnail is not None:
                image_url = media_thumbnail.get('url', '')
            else:
                media_content = entry.find('media:content', ns)
                if media_content is not None:
                    image_url = media_content.get('url', '')

            # Create unified item structure
            item = {
                'title': title,
                'url': url,
                # 'description': description,
                'published': published,
                'image_url': image_url
            }

            items.append(item)

    elif source == 'google' or source == 'tiktok':
        # RSS 2.0 format for Google News
        # Define namespaces for media elements
        ns = {'media': 'http://search.yahoo.com/mrss/',
              'content': 'http://purl.org/rss/1.0/modules/content/'}

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

            # Extract image URL from multiple possible sources
            image_url = ''

            # Try media:thumbnail first
            media_thumbnail = item_elem.find('media:thumbnail', ns)
            if media_thumbnail is not None:
                image_url = media_thumbnail.get('url', '')

            # Try media:content if no thumbnail
            if not image_url:
                media_content = item_elem.find('media:content', ns)
                if media_content is not None:
                    image_url = media_content.get('url', '')

            # Try enclosure tag (common in RSS 2.0)
            if not image_url:
                enclosure = item_elem.find('enclosure')
                if enclosure is not None and enclosure.get('type', '').startswith('image/'):
                    image_url = enclosure.get('url', '')

            # Create unified item structure
            item = {
                'title': title,
                'url': url,
                # 'description': description,
                'published': published,
                'image_url': image_url
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
            print(f"Image URL: {item.get('image_url', 'No image')}")
            print()

    asyncio.run(test_feeds())


async def get_tenant_access_token(app_id: str = None, app_secret: str = None) -> str:
    """
    Get Feishu tenant_access_token for API authentication.

    Args:
        app_id: Feishu app ID (defaults to env APP_ID)
        app_secret: Feishu app secret (defaults to env APP_SECRET)

    Returns:
        tenant_access_token string

    Raises:
        httpx.HTTPError: If the request fails
    """
    if app_id is None:
        app_id = os.getenv("APP_ID")
    if app_secret is None:
        app_secret = os.getenv("APP_SECRET")

    if not app_id or not app_secret:
        raise ValueError("APP_ID and APP_SECRET must be provided or set in environment")

    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"

    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        result = response.json()

        if result.get("code") != 0:
            raise Exception(f"Failed to get tenant_access_token: {result.get('msg')}")

        return result["tenant_access_token"]


async def download_image(url: str, timeout: float = 10.0) -> tuple[bytes, str]:
    """
    Download image from URL.

    Args:
        url: Image URL to download
        timeout: Request timeout in seconds (default 10.0)

    Returns:
        Tuple of (image_data as bytes, filename)

    Raises:
        httpx.HTTPError: If download fails
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(url)
        response.raise_for_status()

        # Extract filename from URL or generate one
        parsed_url = urlparse(url)
        filename = Path(parsed_url.path).name

        # If no filename or extension, generate one based on content type
        if not filename or '.' not in filename:
            content_type = response.headers.get('content-type', '')
            ext = 'jpg'  # default
            if 'png' in content_type:
                ext = 'png'
            elif 'jpeg' in content_type or 'jpg' in content_type:
                ext = 'jpg'
            elif 'gif' in content_type:
                ext = 'gif'
            elif 'webp' in content_type:
                ext = 'webp'
            filename = f"image.{ext}"

        return response.content, filename


async def upload_image_to_lark(
    image_data: bytes,
    filename: str,
    app_token: str,
    tenant_access_token: str = None,
    parent_type: str = "bitable_image"
) -> str:
    """
    Upload image to Feishu/Lark and get file_token.

    Args:
        image_data: Image binary data
        filename: Image filename
        app_token: Bitable app_token (used as parent_node)
        tenant_access_token: Authentication token (will auto-fetch if not provided)
        parent_type: Upload point type (default: "bitable_image")

    Returns:
        file_token string that can be used in bitable attachment fields

    Raises:
        httpx.HTTPError: If upload fails
    """
    # Get token if not provided
    if tenant_access_token is None:
        tenant_access_token = await get_tenant_access_token()

    url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"

    # Prepare multipart form data
    files = {
        'file_name': (None, filename),
        'parent_type': (None, parent_type),
        'parent_node': (None, app_token),
        'size': (None, str(len(image_data))),
        'file': (filename, image_data, 'application/octet-stream')
    }

    headers = {
        'Authorization': f'Bearer {tenant_access_token}'
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, headers=headers, files=files)
        response.raise_for_status()
        result = response.json()

        if result.get("code") != 0:
            raise Exception(f"Failed to upload image: {result.get('msg')}")

        return result["data"]["file_token"]


async def download_and_upload_image(
    image_url: str,
    app_token: str,
    tenant_access_token: str = None,
    max_retries: int = 3
) -> str | None:
    """
    Download image from URL and upload to Feishu, with retry logic.

    Args:
        image_url: URL of image to download
        app_token: Bitable app_token
        tenant_access_token: Authentication token (will auto-fetch if not provided)
        max_retries: Maximum number of retry attempts (default: 3)

    Returns:
        file_token string on success, None on failure
    """
    for attempt in range(max_retries):
        try:
            # Download image
            image_data, filename = await download_image(image_url)

            # Upload to Lark
            file_token = await upload_image_to_lark(
                image_data=image_data,
                filename=filename,
                app_token=app_token,
                tenant_access_token=tenant_access_token
            )

            return file_token

        except Exception as e:
            if attempt < max_retries - 1:
                # Wait before retry (exponential backoff)
                import asyncio
                await asyncio.sleep(2 ** attempt)
                continue
            else:
                # Log error and return None on final failure
                print(f"Failed to download and upload image {image_url}: {e}")
                return None

