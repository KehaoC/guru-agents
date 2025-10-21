"""
Test image upload functionality with real URLs from RSS feeds.
"""
import asyncio
import sys
import os

# Add parent directory to path to import utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import (
    download_image,
    get_tenant_access_token,
    upload_image_to_lark,
    download_and_upload_image
)
from dotenv import load_dotenv

load_dotenv()


async def test_get_tenant_access_token():
    """Test getting tenant access token."""
    print("=" * 80)
    print("TEST 1: Get Tenant Access Token")
    print("=" * 80)

    try:
        token = await get_tenant_access_token()
        print(f"✓ Successfully got tenant_access_token")
        print(f"  Token (first 20 chars): {token[:20]}...")
        print(f"  Token length: {len(token)}")
        return token
    except Exception as e:
        print(f"✗ Failed to get tenant_access_token: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_download_image():
    """Test downloading image from a real URL."""
    print("\n" + "=" * 80)
    print("TEST 2: Download Image from Real URL")
    print("=" * 80)

    # Use a real image URL from thesun.co.uk (from the example you provided)
    test_url = "https://www.thesun.co.uk/wp-content/uploads/2025/10/newspress-collage-3360p1dwp-1760952779727.jpg?quality=90&strip=all&1760956390"

    print(f"Testing URL: {test_url}")

    try:
        image_data, filename = await download_image(test_url)
        print(f"✓ Successfully downloaded image")
        print(f"  Filename: {filename}")
        print(f"  Size: {len(image_data)} bytes ({len(image_data) / 1024:.2f} KB)")
        print(f"  Size within limit: {len(image_data) < 20 * 1024 * 1024}")
        return image_data, filename
    except Exception as e:
        print(f"✗ Failed to download image: {e}")
        import traceback
        traceback.print_exc()
        return None, None


async def test_upload_image_to_lark(image_data, filename, token):
    """Test uploading image to Lark."""
    print("\n" + "=" * 80)
    print("TEST 3: Upload Image to Lark")
    print("=" * 80)

    if not image_data or not token:
        print("✗ Skipping - missing image_data or token from previous tests")
        return None

    # Get app_token from environment or use default from spark.md
    app_token = os.getenv("APP_TOKEN", "WJ47bnLAfaoRFGsPreucdSoknXd")

    print(f"Using app_token: {app_token}")
    print(f"Image filename: {filename}")
    print(f"Image size: {len(image_data)} bytes")

    try:
        file_token = await upload_image_to_lark(
            image_data=image_data,
            filename=filename,
            app_token=app_token,
            tenant_access_token=token
        )
        print(f"✓ Successfully uploaded image to Lark")
        print(f"  File token: {file_token}")
        return file_token
    except Exception as e:
        print(f"✗ Failed to upload image to Lark: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_download_and_upload():
    """Test the combined download and upload function."""
    print("\n" + "=" * 80)
    print("TEST 4: Download and Upload (Combined Function)")
    print("=" * 80)

    test_url = "https://www.thesun.co.uk/wp-content/uploads/2025/10/newspress-collage-3360p1dwp-1760952779727.jpg?quality=90&strip=all&1760956390"
    app_token = os.getenv("APP_TOKEN", "WJ47bnLAfaoRFGsPreucdSoknXd")

    print(f"Testing URL: {test_url}")
    print(f"App token: {app_token}")

    try:
        file_token = await download_and_upload_image(
            image_url=test_url,
            app_token=app_token
        )

        if file_token:
            print(f"✓ Successfully downloaded and uploaded image")
            print(f"  File token: {file_token}")
        else:
            print(f"✗ Function returned None (failed after retries)")

        return file_token
    except Exception as e:
        print(f"✗ Unexpected exception: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_multiple_images():
    """Test uploading multiple images (like the actual use case)."""
    print("\n" + "=" * 80)
    print("TEST 5: Upload Multiple Images")
    print("=" * 80)

    # Multiple real URLs from RSS feeds
    test_urls = [
        "https://www.thesun.co.uk/wp-content/uploads/2025/10/newspress-collage-3360p1dwp-1760952779727.jpg?quality=90&",
        "https://www.thesun.co.uk/wp-content/uploads/2025/10/crop-37070567.jpg?quality=90&",
        "https://www.thesun.co.uk/wp-content/uploads/2025/10/MJ-OFF-PLATFORM-strand.jpg?quality=90&"
    ]

    app_token = os.getenv("APP_TOKEN", "WJ47bnLAfaoRFGsPreucdSoknXd")

    url_token_dict = {}

    print(f"Testing {len(test_urls)} images...")

    for i, url in enumerate(test_urls, 1):
        print(f"\n--- Image {i}/{len(test_urls)} ---")
        print(f"URL: {url[:60]}...")

        try:
            file_token = await download_and_upload_image(
                image_url=url,
                app_token=app_token
            )

            if file_token:
                print(f"✓ Success - token: {file_token}")
                url_token_dict[url] = file_token
            else:
                print(f"✗ Failed - returned None")
                url_token_dict[url] = None

        except Exception as e:
            print(f"✗ Exception: {e}")
            url_token_dict[url] = None

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total: {len(test_urls)}")
    print(f"Success: {sum(1 for v in url_token_dict.values() if v is not None)}")
    print(f"Failed: {sum(1 for v in url_token_dict.values() if v is None)}")

    return url_token_dict


async def main():
    """Run all tests."""
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "IMAGE UPLOAD TEST SUITE" + " " * 35 + "║")
    print("╚" + "=" * 78 + "╝")

    # Test 1: Get token
    token = await test_get_tenant_access_token()

    # Test 2: Download image
    image_data, filename = await test_download_image()

    # Test 3: Upload image
    if token and image_data:
        await test_upload_image_to_lark(image_data, filename, token)

    # Test 4: Combined function
    await test_download_and_upload()

    # Test 5: Multiple images
    await test_multiple_images()

    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 30 + "TESTS COMPLETE" + " " * 34 + "║")
    print("╚" + "=" * 78 + "╝")


if __name__ == "__main__":
    asyncio.run(main())
