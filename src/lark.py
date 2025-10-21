import json
from dotenv import load_dotenv
from claude_agent_sdk import create_sdk_mcp_server, tool
from utils import download_and_upload_image
from typing import Any
import os

load_dotenv()

FEISHU_APP_ID = os.getenv("APP_ID")
FEISHU_SECRET_KEY = os.getenv("APP_SECRET")

lark_server = {
    "command": "lark-mcp",
    "args": [
        "mcp",
        "-a",
        FEISHU_APP_ID,
        "-s",
        FEISHU_SECRET_KEY,
        "--oauth"
    ]
}

@tool("upload_images_to_lark", "Download url image to native and then upload to lark to get file token", {"urls": [str], "app_token": str})
async def upload_images_to_lark(args: dict[str: Any]):
    urls_input = args.get('urls')
    app_token = args.get('app_token', 'WJ47bnLAfaoRFGsPreucdSoknXd')  # Default to the app_token from spark.md
    url_token_dict = {}

    try:
        # Handle multiple input formats for urls parameter
        if isinstance(urls_input, str):
            # Try JSON array format first: '["url1", "url2"]'
            if urls_input.strip().startswith('['):
                try:
                    urls = json.loads(urls_input)
                except json.JSONDecodeError:
                    # If JSON parsing fails, fall through to comma-split
                    urls = None
            else:
                urls = None

            # If not JSON, try comma-separated format: 'url1,url2,url3'
            if urls is None:
                if ',' in urls_input:
                    urls = [u.strip() for u in urls_input.split(',') if u.strip()]
                else:
                    # Single URL string
                    urls = [urls_input.strip()] if urls_input.strip() else []

        elif isinstance(urls_input, list):
            urls = urls_input
        else:
            raise ValueError(f"Invalid urls parameter type: {type(urls_input)}. Expected list or string.")

        # Validate that urls is now a list
        if not isinstance(urls, list):
            raise ValueError(f"After parsing, urls is not a list: {type(urls)}")

        # Validate URLs are non-empty strings
        valid_urls = []
        for url in urls:
            if isinstance(url, str) and url.strip():
                valid_urls.append(url.strip())
            else:
                print(f"Warning: Skipping invalid URL: {url}")

        if not valid_urls:
            raise ValueError("No valid URLs provided")

        print(f"Processing {len(valid_urls)} image URLs...")

        # Process each URL
        for i, url in enumerate(valid_urls, 1):
            print(f"[{i}/{len(valid_urls)}] Uploading: {url[:80]}...")
            token = await download_and_upload_image(
                image_url=url,
                app_token=app_token
            )
            url_token_dict[url] = token

            if token:
                print(f"  ✓ Success: {token}")
            else:
                print(f"  ✗ Failed (returned None)")

        # Summary
        success_count = sum(1 for v in url_token_dict.values() if v is not None)
        print(f"\nSummary: {success_count}/{len(valid_urls)} images uploaded successfully")

        return {
            "content": [{
                "type": "text",
                "text": json.dumps(url_token_dict, indent=2)
            }]
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        error_msg = f"Error uploading image to lark: {str(e)}\n\nDetails:\n{error_details}"
        print(error_msg)  # Print to console for debugging
        return {
            "content": [{
                "type": "text",
                "text": error_msg
            }]
        }

custom_lark_server = create_sdk_mcp_server(
    name = "custom-lark-mcp",
    version = "1.0.0",
    tools = [upload_images_to_lark]
)