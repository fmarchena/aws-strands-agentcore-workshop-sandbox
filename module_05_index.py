from strands import Agent, tool
from strands_tools import http_request, current_time, retrieve
from strands.session.s3_session_manager import S3SessionManager
from strands.tools.mcp.mcp_client import MCPClient
from mcp.client.streamable_http import streamablehttp_client
from typing import Dict, Any
import os
import requests
import mcp.types as mcp_types
import mcp.shared.version as mcp_version


# The workshop's prebuilt Lambda layer offers MCP 2025-06-18, while newly
# created AgentCore gateways negotiate 2025-11-25 or 2026-07-28.
# For this temporary lab, select the gateway's legacy handshake version.
mcp_types.LATEST_PROTOCOL_VERSION = "2025-11-25"
if "2025-11-25" not in mcp_version.SUPPORTED_PROTOCOL_VERSIONS:
    mcp_version.SUPPORTED_PROTOCOL_VERSIONS.append("2025-11-25")


TRAVEL_AGENT_PROMPT = """You are a travel assistant that can help customers book their travel.
Think step-by-step. Limit your answers to the user prompt.
Tools available:
- Use the flight_search tool to provide flight carrier choices for their destination.
- Use the retrieve tool to get validated list of tour operators for different kinds of tours and activities that we support.
- Use list_attractions, reserve_ticket and cancel_ticket tools to provide attractions management service.
Weather Forecast:
- ONLY provide weather forecast if the user explicitly asks for it.
- To fetch weather data, follow these steps strictly:
  1. Make HTTP requests to the National Weather Service API using ONLY GET method
  2. For Seattle: latitude 47.6061°N, longitude 122.3328°W
  3. Get grid info: https://api.weather.gov/points/{latitude},{longitude}
  4. Get forecast: use the returned forecast URL
  5. Provide ONLY a 5-day summary with key conditions (temperature, precipitation, alerts)
  6. Do NOT include detailed daily/nightly breakdowns or extended forecasts
"""


@tool
def flight_search(city: str) -> dict:
    """Get available flight options to a city.

    Args:
        city: The name of the city
    """
    flights = {
        "Atlanta": ["Delta Airlines", "Spirit Airlines"],
        "Seattle": ["Alaska Airlines", "Delta Airlines"],
        "New York": ["United Airlines", "JetBlue"],
    }
    return flights[city]


def fetch_access_token() -> str:
    response = requests.post(
        os.environ["DOMAIN_URL"] + "/oauth2/token",
        data={"grant_type": "client_credentials"},
        auth=(os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"]),
        timeout=15,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def create_streamable_http_transport(access_token: str):
    return streamablehttp_client(
        os.environ["GATEWAY_URL"],
        headers={
            "Authorization": f"Bearer {access_token}",
            "MCP-Protocol-Version": "2025-11-25",
        },
    )


def handler(event: Dict[str, Any], _context) -> str:
    session_manager = S3SessionManager(
        session_id=event["user"]["session_id"],
        bucket=os.environ["SESSIONS_BUCKET"],
        prefix="agent-sessions",
    )
    access_token = fetch_access_token()
    mcp_client = MCPClient(lambda: create_streamable_http_transport(access_token))
    with mcp_client:
        tools_mcp = mcp_client.list_tools_sync()
        tools_mcp += [flight_search, http_request, current_time, retrieve]
        travel_agent = Agent(
            model="us.amazon.nova-lite-v1:0",
            system_prompt=TRAVEL_AGENT_PROMPT,
            tools=tools_mcp,
            session_manager=session_manager,
        )
        return str(travel_agent(event.get("prompt")))
