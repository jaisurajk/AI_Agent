import asyncio
import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from dotenv import load_dotenv
load_dotenv()

# --------------------------
# Tools
# --------------------------
def get_weather(city: str) -> dict:
    if city.lower() == "new york":
        return {"status": "success", "report": "Sunny, ~25°C."}
    return {"status": "error", "error_message": f"No weather info for {city}"}

def get_current_time(city: str) -> dict:
    if city.lower() == "new york":
        now = datetime.datetime.now(ZoneInfo("America/New_York"))
        return {"status": "success", "report": f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"}
    return {"status": "error", "error_message": f"No time info for {city}"}

# --------------------------
# Config
# --------------------------
APP_NAME = "weather_time_app"
USER_ID = "user_1"
SESSION_ID = "session_001"

# --------------------------
# Create session service
# --------------------------
session_service = InMemorySessionService()

# --------------------------
# Create agent
# --------------------------
root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.5-flash",
    description="Agent to answer time/weather questions.",
    instruction="Answer user questions about weather and local time.",
    tools=[get_weather, get_current_time],
)

# --------------------------
# Create Runner with the same session_service
# --------------------------
runner = Runner(
    agent=root_agent,
    session_service=session_service,
    app_name=APP_NAME
)

# --------------------------
# Setup session
# --------------------------
async def setup_session():
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

# --------------------------
# Main
# --------------------------
async def main():
    # Create session BEFORE running
    await setup_session()

    # User message
    content = Content(
        role="user",
        parts=[Part(text="Tell me weather in New York")]
    )

    # Run agent
    events = runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,  # Use the same session ID
        new_message=content
    )

    # Print final response
    async for event in events:
        if event.is_final_response():
            print("Agent:", event.content)

# --------------------------
# Execute
# --------------------------
if __name__ == "__main__":
    asyncio.run(main())