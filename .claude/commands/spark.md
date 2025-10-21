---
allowed-tools: All
description: Find heated topic from online to generate insipiration for ads.
model: claude-sonnet-4-5-20250929
---

1. Using fetch_trends_from_rss tools get heated topic from online.
2. Format and refactor the information as inspiration seed.
3. Select 5 best ideas that are relevant to "Find Difference" game product.
4. For each selected topic, evaluate and generate:
   - **实时热度** (Real-time Heat Score): AI evaluation score from 1-5 based on topic popularity, trend velocity, and relevance
   - **热点日期** (Hot Date): Today's date when the command is triggered (format: yyyy/MM/dd)
6. Create new rows in lark bitable [https://scnmrtumk0zm.feishu.cn/wiki/I1iAwzwT3i1b6BkhgCecjeHvnkc?table=wkfNU1GEwuXZQJJK] with:

## Tool Use Example

```python
mcp__lark-mcp__bitable_v1_appTableRecord_create(
    path={
        'app_token': 'WJ47bnLAfaoRFGsPreucdSoknXd',
        'table_id': 'tbl0VpizbLm3697f'
    },
    data={
        'fields': {
            'Idea': 'AI换脸挑战',
            '来源': ['热点'],
            '设计师参考图片需求': '对比真实明星照片与AI换脸后的细节差异，如眼神、肤质、五官比例等微妙变化',
            '实时热度（系统预测）': 4,
            '热点日期': 1737331200000,
            '目标产品': ['APFD'],
            'url': 'https://example.com/trending-topic'
        }
    },
    useUAT=True
)
```

## Field Requirements

**Topic名称 (Topic field, fldyHisKlR)**:
- Must include SPECIFIC KEYWORDS that instantly reveal what's hot
- Maximum 15-20 characters, make every word count
- Capture the most eye-catching, concrete detail of the trend
- Use vivid, specific terms over generic descriptions
- Examples:
  - ❌ Bad: "AI绘画爆火" (too vague)
  - ✅ Good: "AI绘制赛博朋克城市"
  - ❌ Bad: "春节红包大战"
  - ✅ Good: "支付宝发10亿红包雨"
  - ❌ Bad: "世界杯热潮"
  - ✅ Good: "梅西捧杯刷屏全网"

**来源 (Source field, fld4z23xmO)**:
- Always set to: "热点" (固定值)
- No need to specify detailed source

**图片需求 (Image Requirements field, fldPesZfWW)**:
- Brief description of what visual elements would work for "Find Difference" game
- Connect the topic to game mechanics (what differences to spot)
- Keep under 100 characters

**Topic标签 (Tags field, fldC9OPibT)**:
- Select appropriate tag from: "热点", "出量素材迭代", "节日", "经典IP"
- Default to "热点" for trending topics

**实时热度 (Real-time Heat)**:
- AI-generated score (1-5) based on:
  - Topic search volume and mentions
  - Trend velocity (rising/stable/declining)
  - Relevance to target audience
  - Potential for viral content

**热点日期 (Hot Date field, fld4EznD38)**:
- Use the actual publication date from the fetched RSS content
- Extract the date from the RSS feed item's published/pubDate field
- Format: yyyy/MM/dd
- This represents when the trending topic was originally published, not when it was fetched

**URL (URL field)**:
- The source URL from the RSS feed where the topic was fetched
- Include the complete URL (e.g., https://example.com/trending-topic)
- This allows tracking the original source of each trending topic

## Product Context
Our product is **"Find Difference"** (找茬游戏), so you MUST:
- Select topics that can naturally connect to visual comparison/difference-finding gameplay
- Create descriptions that make the connection to the game obvious
- Avoid random topics that don't fit the game's creative direction 

## 优秀案例