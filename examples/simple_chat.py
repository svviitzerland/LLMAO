"""Example 1: Simple Single Model

Basic usage with default configuration (from environment variables or default registry).
"""
import os
from llmao_py import LLMClient

# Ensure key is set
# os.environ["CEREBRAS_API_KEY"] = "your-key-here"

client = LLMClient()

print("Sending request...")
response = client.completion(
    model="cerebras/llama3.1-70b",
    messages=[{"role": "user", "content": "Hello! Say hi in one word."}]
)

print(f"Response: {response['choices'][0]['message']['content']}")
