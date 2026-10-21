from strands import Agent, tool
from strands_tools import http_request
from typing import Dict, Any


TRAVEL_AGENT_PROMPT = """You are a travel assistant that can help customers book their travel.
Think step-by-step. Limit your answers to the user prompt.
Tools available:
- Use the flight_search tool to provide flight carrier choices for their destination.
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


def handler(event: Dict[str, Any], _context) -> str:
    travel_agent = Agent(
        model="us.amazon.nova-lite-v1:0",
        system_prompt=TRAVEL_AGENT_PROMPT,
        tools=[flight_search, http_request],
    )
    response = travel_agent(event.get("prompt"))
    return str(response)
