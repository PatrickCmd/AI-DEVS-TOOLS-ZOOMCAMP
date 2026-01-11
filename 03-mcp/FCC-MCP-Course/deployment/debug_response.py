"""
Debug script to inspect the OpenAI response object structure
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

# Configure MCP tool
mcp_tool = {
    "type": "mcp",
    "server_label": "freedcodecamp-content",
    "server_url": "https://freedcodecamp-content.fastmcp.app/mcp",
    "require_approval": "never",
}

print("Creating response...")

response = client.responses.create(
    model="gpt-5-mini",
    instructions="You are a helpful programming assistant.",
    tools=[mcp_tool],
    input="Find Python tutorials",
    max_output_tokens=500,
)

print("\n" + "="*70)
print("RESPONSE OBJECT INSPECTION")
print("="*70)

print(f"\nType: {type(response)}")
print(f"\nDir: {[attr for attr in dir(response) if not attr.startswith('_')]}")

print("\n" + "="*70)
print("ATTRIBUTES")
print("="*70)

# Check all possible output attributes
output_attrs = ['output_text', 'output', 'text', 'content', 'message', 'choices']

for attr in output_attrs:
    if hasattr(response, attr):
        value = getattr(response, attr)
        print(f"\n{attr}:")
        print(f"  Type: {type(value)}")
        print(f"  Value: {value}")

print("\n" + "="*70)
print("USAGE")
print("="*70)

if hasattr(response, 'usage'):
    print(f"\nInput tokens: {response.usage.input_tokens}")
    print(f"Output tokens: {response.usage.output_tokens}")
    print(f"Total tokens: {response.usage.total_tokens}")

print("\n" + "="*70)
print("RAW RESPONSE (as dict)")
print("="*70)

# Try to convert to dict
if hasattr(response, 'model_dump'):
    print(json.dumps(response.model_dump(), indent=2, default=str))
elif hasattr(response, 'dict'):
    print(json.dumps(response.dict(), indent=2, default=str))
else:
    print(f"Cannot convert to dict. Type: {type(response)}")
