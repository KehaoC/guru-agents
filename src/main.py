from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, query, create_sdk_mcp_server
from cli_tools import parse_and_print_message, parser, print_rich_message, get_user_input
from rich.console import Console
from topic import topic_server
import os
from dotenv import load_dotenv
import prompt

# cheapest one for test
load_dotenv()

MODEL = "haiku"
FEISHU_APP_ID = os.getenv("APP_ID")
FEISHU_SECRET_KEY = os.getenv("APP_SECRET")

async def main():
    console = Console() 
    args = parser.parse_args()

    welcoming_message = "GURU GREATEERBAY AGENT"
    print_rich_message('system', welcoming_message, console)

    options = ClaudeAgentOptions(
        system_prompt = prompt.SYSTEM_PROMPT,
        setting_sources=["project"],
        model = MODEL,
        mcp_servers={
            "topic": topic_server,
            "lark-mcp": {
                "command": "npx",
                "args": [
                    "-y",
                    "@larksuiteoapi/lark-mcp",
                    "mcp",
                    "-a",
                    FEISHU_APP_ID,
                    "-s",
                    FEISHU_SECRET_KEY,
                    "--oauth"
                ]
            }
        },
        allowed_tools = [
            # Topic
            "mcp__topic__fetch_trends_from_rss",  # 从 RSS 源获取热点趋势

            # Feishu (Lark) - Bitable APIs (多维表格)
            "mcp__lark-mcp__bitable_v1_app_create",              # 创建多维表格应用
            "mcp__lark-mcp__bitable_v1_appTable_create",         # 在多维表格中创建数据表
            "mcp__lark-mcp__bitable_v1_appTableField_list",      # 列出数据表的所有字段
            "mcp__lark-mcp__bitable_v1_appTable_list",           # 列出应用中的所有数据表
            "mcp__lark-mcp__bitable_v1_appTableRecord_create",   # 在数据表中创建记录
            "mcp__lark-mcp__bitable_v1_appTableRecord_search",   # 搜索/查询数据表记录
            "mcp__lark-mcp__bitable_v1_appTableRecord_update",   # 更新数据表记录

            # Feishu (Lark) - Contact APIs (通讯录)
            "mcp__lark-mcp__contact_v3_user_batchGetId",         # 批量获取用户 ID (通过邮箱/手机号)

            # Feishu (Lark) - Document APIs (文档)
            "mcp__lark-mcp__docx_v1_document_rawContent",        # 获取飞书文档原始内容
            "mcp__lark-mcp__docx_builtin_search",                # 搜索飞书文档
            "mcp__lark-mcp__docx_builtin_import",                # 导入文档到飞书

            # Feishu (Lark) - Drive APIs (云盘)
            "mcp__lark-mcp__drive_v1_permissionMember_create",   # 添加云盘文件/文件夹的访问权限

            # Feishu (Lark) - IM APIs (即时消息)
            "mcp__lark-mcp__im_v1_chat_create",                  # 创建群聊
            "mcp__lark-mcp__im_v1_chat_list",                    # 获取群聊列表
            "mcp__lark-mcp__im_v1_chatMembers_get",              # 获取群成员列表
            "mcp__lark-mcp__im_v1_message_create",               # 发送消息 (支持文本/图片/卡片等)
            "mcp__lark-mcp__im_v1_message_list",                 # 获取消息列表/历史记录

            # Feishu (Lark) - Wiki APIs (知识库)
            "mcp__lark-mcp__wiki_v1_node_search",                # 搜索知识库节点
            "mcp__lark-mcp__wiki_v2_space_getNode",              # 获取知识库空间节点信息

            # Other tools
            "WebFetch"  # 从网页抓取内容
        ]
    )

    async with ClaudeSDKClient(options) as client:
        while True:
            user_input = get_user_input(console)
            parse_and_print_message(user_input, console)

            if user_input == "quit":
                break
                
            await client.query(user_input)
            async for message in client.receive_response():
                parse_and_print_message(message, console)
    
    goodbye_message = "GG-Bond: See u next time!"
    print_rich_message('system', goodbye_message, console)


if __name__ == "__main__":
    import asyncio
    import nest_asyncio

    nest_asyncio.apply()
    asyncio.run(main())