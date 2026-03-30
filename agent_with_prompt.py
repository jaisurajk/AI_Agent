import datetime
from zoneinfo import ZoneInfo
import google.generativeai as genai
import os

# Configure API
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# ---- Tools ----
def get_weather(city: str) -> dict:
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": "The weather in New York is sunny, 25°C"
        }
    return {"status": "error", "error_message": f"Weather not available for {city}"}

def get_current_time(city: str) -> dict:
    if city.lower() == "new york":
        tz = ZoneInfo("America/New_York")
        now = datetime.datetime.now(tz)
        return {
            "status": "success",
            "report": now.strftime("%Y-%m-%d %H:%M:%S")
        }
    return {"status": "error", "error_message": f"Time not available for {city}"}

# ---- Model ----
model = genai.GenerativeModel("gemini-2.5-flash")

# ---- Agent Logic ----
def run_agent(user_input: str):
    prompt = f"""
You are an agent with access to tools:

1. get_weather(city)
2. get_current_time(city)

User question: {user_input}

Decide which tool(s) to call and respond in JSON:
{{
  "tools": ["tool_name"],
  "city": "city_name"
}}
"""

    response = model.generate_content(prompt)
    decision = response.text.strip()

    print("\nModel decision:", decision)

    # Simple logic (demo purpose)
    result = {}

    if "weather" in decision.lower():
        result["weather"] = get_weather("New York")

    if "time" in decision.lower():
        result["time"] = get_current_time("New York")

    if not result:
        result = {"status": "error", "error_message": "Could not determine intent"}

    return result


# ---- Main loop (USER INPUT) ----
if __name__ == "__main__":
    print("🤖 Weather & Time Agent (type 'exit' to quit)\n")

    while True:
        user_input = input("Enter your question: ")

        if user_input.lower() == "exit":
            print("Goodbye 👋")
            break

        output = run_agent(user_input)
        print("Final Result:", output)
        print("-" * 50)