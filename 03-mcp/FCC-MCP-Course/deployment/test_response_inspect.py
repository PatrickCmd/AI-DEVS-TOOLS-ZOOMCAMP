"""
Inspect the OpenAI Responses API response to see its structure
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

def inspect_response():
    """Inspect what the Responses API returns."""
    client = OpenAI()

    # Simple tool definition
    tools = [
        {
            "type": "function",
            "name": "get_weather",
            "description": "Get the weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["location"]
            },
            "strict": False
        }
    ]

    print("Making request to Responses API with tools...")

    response = client.responses.create(
        model="gpt-5-mini",
        instructions="You are a helpful assistant. When asked about weather, use the get_weather tool.",
        tools=tools,
        input="What's the weather in San Francisco?",
    )

    print("\n" + "="*70)
    print("Response Object Attributes:")
    print("="*70)
    for attr in dir(response):
        if not attr.startswith('_'):
            print(f"  - {attr}")

    print("\n" + "="*70)
    print("Response Details:")
    print("="*70)
    print(f"\noutput_text: {response.output_text}")
    print(f"\nmodel: {response.model}")
    print(f"\nid: {response.id}")

    # Check for tool calls or other attributes
    if hasattr(response, 'tool_calls'):
        print(f"\ntool_calls: {response.tool_calls}")

    if hasattr(response, 'choices'):
        print(f"\nchoices: {response.choices}")

    if hasattr(response, 'output'):
        print(f"\noutput: {response.output}")

    # Try to convert to dict
    try:
        print("\n" + "="*70)
        print("Response as dict:")
        print("="*70)
        print(json.dumps(response.model_dump(), indent=2))
    except:
        print("Could not convert response to dict")

if __name__ == "__main__":
    inspect_response()
