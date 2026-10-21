from strands import Agent, tool
from typing import Dict, Any


# Define a travel-focused system prompt
TRAVEL_AGENT_PROMPT = """You are a travel assistant that can help customers book their travel.
Think step-by-step. Limit your answers to the user prompt.
Tools available:
- Use the flight_search tool to provide flight carrier choices for their destination.
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


# The handler function signature `def handler(event, context)` is what Lambda
# looks for when invoking your function.
def handler(event: Dict[str, Any], _context) -> str:
    travel_agent = Agent(
        model="us.amazon.nova-lite-v1:0",
        system_prompt=TRAVEL_AGENT_PROMPT,
        tools=[flight_search],
    )
    response = travel_agent(event.get("prompt"))
    return str(response)
