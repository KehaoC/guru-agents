import json, requests, xml.etree.ElementTree as ET

RSS_URL_LIST = [
    "https://www.reddit.com/r/worldnews/.rss", # raddit/worldnews
]

def fetch_trends_from_rss_example():
    r = requests.get(RSS_URL_LIST[0], timeout=10)
    root = ET.fromstring(r.text)

    items = []
    for item in root.findall(".//item"):
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        pub_date = item.findtext("pubDate", "").strip()
        items.append({"title": title, "link": link, "pub_date": pub_date})

    return items

def fetch_trends_from_rss():
    items = []
    for url in RSS_URL_LIST:
        r = requests.get(url, timeout=3)
        root = ET.fromstring(r.text)

        for item in root.findall(".//item"):
            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            pub_date = item.findtext("pubDate", "").strip()
            print(f"{title}: {link} {pub_date}\n")



if __name__ == "__main__":
    # trends = fetch_trends()
    # print(json.dumps(trends, ensure_ascii=False, indent=2))

    fetch_trends_from_rss()