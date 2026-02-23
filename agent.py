import logging
import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

from google.auth.transport.requests import Request
from google.auth import default
import sys

server_url="http://127.0.0.1:8001/mcp/"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

load_dotenv()

SYSTEM_INSTRUCTION = (
    "You are a helpful assistant for a Github assistant for a developer."
    "You should use ONLY the tools provided to you to answer the user's questions about their Github repositories, issues, pull requests, and more."
    "If requested, you can also perform actions on the user's Github account such as creating issues, commenting on pull requests, and more using the provided tools."
)

TestAgent = LlmAgent(
    name="TestAgent",
    model="gemini-2.5-pro",
    description="Handles Github requests and ticket creation.",
    instruction=SYSTEM_INSTRUCTION,
    tools=[
            MCPToolset(
                connection_params=StreamableHTTPConnectionParams(
                    url=server_url
              )
            )
        ],
)

root_agent = TestAgent
