"""
Test handling of JSON string input for urls parameter.
This simulates the actual bug that occurred.
"""
import asyncio
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import directly the underlying function for testing
from utils import download_and_upload_image


async def simulate_tool_call_with_json_string():
    """
    Simulate the actual tool call that caused the bug.
    The urls parameter comes in as a JSON string instead of a list.
    """
    print("=" * 80)
    print("TEST: JSON String Input (Simulating Actual Bug)")
    print("=" * 80)

    # This is what the tool receives (from your bug report)
    args = {
        'urls': '["https://www.thesun.co.uk/wp-content%2Fuploads%2F2025%2F10%2FMM-OFF-PLATFORM-strand.jpg?quality%3D90%26", "https://www.thesun.co.uk/wp-content%2Fuploads%2F2025%2F10%2Fcrop-37070567.jpg?quality%3D90%26", "https://www.thesun.co.uk/wp-content%2Fuploads%2F2025%2F10%2Fnewspress-collage-e20tc2xkx-1760973095829.jpg?quality%3D90%26"]',
        'app_token': 'WJ47bnLAfaoRFGsPreucdSoknXd'
    }

    print(f"Input args:")
    print(f"  urls type: {type(args['urls'])}")
    print(f"  urls value (first 100 chars): {str(args['urls'])[:100]}...")
    print()

    # Parse the JSON string
    urls_input = args.get('urls')

    try:
        if isinstance(urls_input, str):
            urls = json.loads(urls_input)
            print(f"✓ Successfully parsed JSON string")
            print(f"  Result type: {type(urls)}")
            print(f"  Number of URLs: {len(urls)}")
            print()

            # Print decoded URLs
            print("Decoded URLs:")
            for i, url in enumerate(urls, 1):
                # URL decode the %2F and %3D
                from urllib.parse import unquote
                decoded_url = unquote(url)
                print(f"  {i}. {decoded_url}")

            return urls
        else:
            print(f"✗ urls is not a string: {type(urls_input)}")
            return None

    except json.JSONDecodeError as e:
        print(f"✗ Failed to parse JSON: {e}")
        return None


async def test_with_list_input():
    """Test with normal list input (should also work)."""
    print("\n" + "=" * 80)
    print("TEST: Normal List Input")
    print("=" * 80)

    args = {
        'urls': [
            "https://www.thesun.co.uk/wp-content/uploads/2025/10/newspress-collage-3360p1dwp-1760952779727.jpg?quality=90&"
        ],
        'app_token': 'WJ47bnLAfaoRFGsPreucdSoknXd'
    }

    urls_input = args.get('urls')

    if isinstance(urls_input, list):
        print(f"✓ Input is already a list")
        print(f"  Number of URLs: {len(urls_input)}")
        return urls_input
    else:
        print(f"✗ Input is not a list: {type(urls_input)}")
        return None


async def test_url_decoding():
    """Test URL decoding for the encoded URLs."""
    print("\n" + "=" * 80)
    print("TEST: URL Decoding")
    print("=" * 80)

    from urllib.parse import unquote

    # URL from the bug report (with %2F encoding)
    encoded_url = "https://www.thesun.co.uk/wp-content%2Fuploads%2F2025%2F10%2FMM-OFF-PLATFORM-strand.jpg?quality%3D90%26"
    decoded_url = unquote(encoded_url)

    print(f"Encoded URL:")
    print(f"  {encoded_url}")
    print()
    print(f"Decoded URL:")
    print(f"  {decoded_url}")
    print()

    # Test if both work for downloading
    app_token = 'WJ47bnLAfaoRFGsPreucdSoknXd'

    print("Testing download with ENCODED URL...")
    try:
        token1 = await download_and_upload_image(
            image_url=encoded_url,
            app_token=app_token,
            max_retries=1
        )
        if token1:
            print(f"  ✓ Encoded URL works: {token1}")
        else:
            print(f"  ✗ Encoded URL failed")
    except Exception as e:
        print(f"  ✗ Encoded URL error: {e}")

    print()
    print("Testing download with DECODED URL...")
    try:
        token2 = await download_and_upload_image(
            image_url=decoded_url,
            app_token=app_token,
            max_retries=1
        )
        if token2:
            print(f"  ✓ Decoded URL works: {token2}")
        else:
            print(f"  ✗ Decoded URL failed")
    except Exception as e:
        print(f"  ✗ Decoded URL error: {e}")


async def test_robust_url_handling():
    """Test various edge cases for URL input."""
    print("\n" + "=" * 80)
    print("TEST: Robust URL Handling")
    print("=" * 80)

    test_cases = [
        {
            'name': 'JSON string with URLs',
            'input': '["https://example.com/1.jpg", "https://example.com/2.jpg"]',
            'expected_type': list,
            'expected_count': 2
        },
        {
            'name': 'Normal list',
            'input': ["https://example.com/1.jpg"],
            'expected_type': list,
            'expected_count': 1
        },
        {
            'name': 'Single URL string (not JSON)',
            'input': "https://example.com/single.jpg",
            'expected_type': list,
            'expected_count': 1
        },
        {
            'name': 'Empty list',
            'input': '[]',
            'expected_type': list,
            'expected_count': 0
        },
    ]

    for test in test_cases:
        print(f"\n--- {test['name']} ---")
        urls_input = test['input']

        # Simulate the parsing logic from lark.py
        if isinstance(urls_input, str):
            try:
                urls = json.loads(urls_input)
            except json.JSONDecodeError:
                urls = [urls_input]
        elif isinstance(urls_input, list):
            urls = urls_input
        else:
            urls = None

        if urls is not None and isinstance(urls, test['expected_type']) and len(urls) == test['expected_count']:
            print(f"  ✓ PASS: Got {type(urls)} with {len(urls)} items")
        else:
            print(f"  ✗ FAIL: Expected {test['expected_type']} with {test['expected_count']} items")
            print(f"         Got {type(urls)} with {len(urls) if urls else 'N/A'} items")


async def main():
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 22 + "JSON STRING INPUT TEST" + " " * 34 + "║")
    print("╚" + "=" * 78 + "╝")
    print()

    await simulate_tool_call_with_json_string()
    await test_with_list_input()
    await test_url_decoding()
    await test_robust_url_handling()

    print()
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 30 + "TESTS COMPLETE" + " " * 34 + "║")
    print("╚" + "=" * 78 + "╝")


if __name__ == "__main__":
    asyncio.run(main())
