from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, query, create_sdk_mcp_server
from cli_tools import parse_and_print_message, parser, print_rich_message, get_user_input
from rich.console import Console
from topic import topic_server
import prompt

# cheapest one for test
MODEL = "haiku"

async def main():
    console = Console() 
    args = parser.parse_args()

    welcoming_message = "GURU GREATEERBAY AGENT"
    print_rich_message('system', welcoming_message, console)

    options = ClaudeAgentOptions(
        system_prompt = prompt.SYSTEM_PROMPT,
        model = MODEL,
        mcp_servers={"topic": topic_server},
        allowed_tools = [
            "mcp__topic__fetch_trends_from_rss",
            "WebFetch"
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