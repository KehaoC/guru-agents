"""
Test the lark.py tool function directly.
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lark import upload_images_to_lark


async def test_lark_tool():
    """Test the upload_images_to_lark tool function."""
    print("=" * 80)
    print("TEST: upload_images_to_lark Tool Function")
    print("=" * 80)

    # Test URLs from RSS feeds
    test_urls = [
        "https://www.thesun.co.uk/wp-content/uploads/2025/10/newspress-collage-3360p1dwp-1760952779727.jpg?quality=90&",
        "https://www.thesun.co.uk/wp-content/uploads/2025/10/crop-37070567.jpg?quality=90&"
    ]

    # Simulate the args that would come from the MCP tool
    args = {
        'urls': test_urls,
        'app_token': 'WJ47bnLAfaoRFGsPreucdSoknXd'
    }

    print(f"Testing with {len(test_urls)} URLs")
    print(f"App token: {args['app_token']}")
    print()

    try:
        result = await upload_images_to_lark(args)

        print("✓ Function executed successfully")
        print()
        print("Result:")
        print(result['content'][0]['text'])

    except Exception as e:
        print(f"✗ Function failed: {e}")
        import traceback
        traceback.print_exc()


async def test_without_app_token():
    """Test with default app_token (should use the default)."""
    print("\n" + "=" * 80)
    print("TEST: upload_images_to_lark Without Explicit app_token")
    print("=" * 80)

    test_urls = [
        "https://www.thesun.co.uk/wp-content/uploads/2025/10/newspress-collage-3360p1dwp-1760952779727.jpg?quality=90&"
    ]

    # Only provide urls, no app_token
    args = {
        'urls': test_urls
    }

    print(f"Testing with {len(test_urls)} URLs")
    print("App token: <using default>")
    print()

    try:
        result = await upload_images_to_lark(args)

        print("✓ Function executed successfully with default app_token")
        print()
        print("Result:")
        print(result['content'][0]['text'])

    except Exception as e:
        print(f"✗ Function failed: {e}")
        import traceback
        traceback.print_exc()


async def main():
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 25 + "LARK TOOL TEST" + " " * 39 + "║")
    print("╚" + "=" * 78 + "╝")
    print()

    await test_lark_tool()
    await test_without_app_token()

    print()
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 30 + "TESTS COMPLETE" + " " * 34 + "║")
    print("╚" + "=" * 78 + "╝")


if __name__ == "__main__":
    asyncio.run(main())
