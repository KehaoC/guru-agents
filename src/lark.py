from dotenv import load_dotenv
import os

load_dotenv()

FEISHU_APP_ID = os.getenv("APP_ID")
FEISHU_SECRET_KEY = os.getenv("APP_SECRET")

lark_mcp = {
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