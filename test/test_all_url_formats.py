"""
Test all possible URL input formats.
"""
import json


def parse_urls(urls_input):
    """
    Simulate the parsing logic from lark.py
    """
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

    return valid_urls


def test_format(name, input_value, expected_count, expected_first_url=None):
    """Test a specific format."""
    print(f"\n{'=' * 80}")
    print(f"TEST: {name}")
    print(f"{'=' * 80}")
    print(f"Input type: {type(input_value)}")
    print(f"Input value (first 100 chars): {str(input_value)[:100]}...")
    print()

    try:
        result = parse_urls(input_value)
        print(f"✓ Successfully parsed")
        print(f"  Result count: {len(result)}")

        if expected_count is not None:
            if len(result) == expected_count:
                print(f"  ✓ Count matches expected: {expected_count}")
            else:
                print(f"  ✗ Count mismatch! Expected {expected_count}, got {len(result)}")
                return False

        if expected_first_url is not None and len(result) > 0:
            if result[0] == expected_first_url:
                print(f"  ✓ First URL matches expected")
            else:
                print(f"  ✗ First URL mismatch!")
                print(f"    Expected: {expected_first_url}")
                print(f"    Got:      {result[0]}")
                return False

        # Print all URLs
        if len(result) <= 5:
            print(f"\n  Parsed URLs:")
            for i, url in enumerate(result, 1):
                print(f"    {i}. {url}")
        else:
            print(f"\n  First 3 URLs:")
            for i, url in enumerate(result[:3], 1):
                print(f"    {i}. {url}")
            print(f"    ... and {len(result) - 3} more")

        return True

    except Exception as e:
        print(f"✗ Failed to parse: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 23 + "ALL URL FORMATS TEST" + " " * 35 + "║")
    print("╚" + "=" * 78 + "╝")

    test_cases = [
        # Format 1: Comma-separated string (THE NEW BUG)
        {
            'name': 'Comma-separated URLs (Current Bug)',
            'input': 'https://www.thesun.co.uk/wp-content%2Fuploads%2F2025%2F10%2FMM-OFF-PLATFORM-strand.jpg?quality%3D90%26,https://www.thesun.co.uk/wp-content%2Fuploads%2F2025%2F10%2Fcrop-37070567.jpg?quality%3D90%26,https://www.thesun.co.uk/wp-content%2Fuploads%2F2025%2F10%2Fnewspress-collage-e20tc2xkx-1760973095829.jpg?quality%3D90%26',
            'expected_count': 3,
            'expected_first': 'https://www.thesun.co.uk/wp-content%2Fuploads%2F2025%2F10%2FMM-OFF-PLATFORM-strand.jpg?quality%3D90%26'
        },
        # Format 2: JSON array string
        {
            'name': 'JSON Array String',
            'input': '["https://example.com/1.jpg", "https://example.com/2.jpg", "https://example.com/3.jpg"]',
            'expected_count': 3,
            'expected_first': 'https://example.com/1.jpg'
        },
        # Format 3: Python list
        {
            'name': 'Python List',
            'input': ["https://example.com/1.jpg", "https://example.com/2.jpg"],
            'expected_count': 2,
            'expected_first': 'https://example.com/1.jpg'
        },
        # Format 4: Single URL string
        {
            'name': 'Single URL String',
            'input': 'https://example.com/single.jpg',
            'expected_count': 1,
            'expected_first': 'https://example.com/single.jpg'
        },
        # Format 5: Empty string
        {
            'name': 'Empty String',
            'input': '',
            'expected_count': 0,
            'expected_first': None
        },
        # Format 6: Empty JSON array
        {
            'name': 'Empty JSON Array',
            'input': '[]',
            'expected_count': 0,
            'expected_first': None
        },
        # Format 7: Comma-separated with spaces
        {
            'name': 'Comma-separated with Spaces',
            'input': 'https://example.com/1.jpg, https://example.com/2.jpg , https://example.com/3.jpg',
            'expected_count': 3,
            'expected_first': 'https://example.com/1.jpg'
        },
    ]

    results = []
    for test_case in test_cases:
        result = test_format(
            test_case['name'],
            test_case['input'],
            test_case['expected_count'],
            test_case.get('expected_first')
        )
        results.append((test_case['name'], result))

    # Summary
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 32 + "SUMMARY" + " " * 39 + "║")
    print("╚" + "=" * 78 + "╝")

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")

    print()
    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")

    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

    print()
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 30 + "TESTS COMPLETE" + " " * 34 + "║")
    print("╚" + "=" * 78 + "╝")


if __name__ == "__main__":
    main()
