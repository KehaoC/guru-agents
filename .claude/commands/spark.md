---
allowed-tools: All
description: Find heated topic from online to generate insipiration for ads.
model: claude-sonnet-4-5-20250929
---

1. Fetch trending topics using `fetch_trends_from_rss` tools
2. Select **ONLY 3** best ideas relevant to "Find Difference" game
3. For each idea, generate `实时热度（系统预测）` (1-5) and extract `热点日期` timestamp from RSS pubDate
4. **Upload images** (BEFORE creating rows):
   - Extract `image_url` from the 3 ideas
   - Call `mcp__custom-lark-mcp__upload_images_to_lark(urls=[...], app_token='WJ47bnLAfaoRFGsPreucdSoknXd')`
   - Store URL-to-token mapping
5. Create 3 rows using exact field names from example below

## Example (from actual successful run)

```python
# Example from actual run:
mcp__lark-mcp__bitable_v1_appTableRecord_create(
    path={
        'app_token': 'WJ47bnLAfaoRFGsPreucdSoknXd',
        'table_id': 'tbl0VpizbLm3697f'
    },
    data={
        'fields': {
            'Idea': '曼联球迷长发挑战',
            '来源': ['热点-GGBond'],
            '设计师参考图片需求': '对比球迷不同阶段发型变化,找出发长、发型、脸部表情的细微差异',
            '实时热度（系统预测）': 4,
            '热点日期': 1729468800000,
            '目标产品': ['APFD'],
            'url': 'https://www.thesun.co.uk/sport/37071986/united-we-strand-frank-illett-haircut-manchester-utd-liverpool/',
            'Idea 图例': [{'file_token': 'NyxPbq3NNo1pa1xl33bcr8dNncz'}]
        }
    },
    useUAT=True
)
```

## Required Fields (Exact Field Names)

**CRITICAL**: Use these EXACT field names. Do NOT translate or modify them.

1. **`Idea`**: Topic title (15-20 chars max, specific keywords)
   - Example: "曼联球迷长发挑战", "梅西捧杯刷屏全网"

2. **`来源`**: Array with single value `["热点-GGBond"]` (always fixed)

3. **`设计师参考图片需求`**: Find-difference game description (<100 chars)
   - Example: "对比球迷不同阶段发型变化,找出发长、发型、脸部表情的细微差异"

4. **`实时热度（系统预测）`**: Integer 1-5 based on popularity/trend velocity

5. **`热点日期`**: Unix timestamp in milliseconds from RSS feed's pubDate
   - Extract from feed, convert to milliseconds: `1729468800000`

6. **`目标产品`**: Array with value `["APFD"]` (always fixed)

7. **`url`**: Source URL string from RSS feed

8. **`Idea 图例`**: Array of objects with file_token from step 5
   - Format: `[{"file_token": "NyxPbq3NNo1pa1xl33bcr8dNncz"}]`
   - Omit if no image or upload failed

## Product Context
Our product is **"Find Difference"** (找茬游戏), so you MUST:
- Select topics that can naturally connect to visual comparison/difference-finding gameplay
- Create descriptions that make the connection to the game obvious
- Avoid random topics that don't fit the game's creative direction 

## 优秀案例