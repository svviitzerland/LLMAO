"""Example 2: Multiple Providers with Key Rotation

Using a config.json file to manage multiple keys and providers.
"""
import json
from llmao_py import LLMClient

# Create a temporary config file for demonstration
config = {
    "cerebras": {
        "models": ["llama3.1-70b", "llama3.3-70b"],
        "keys": ["csk-key1", "csk-key2"],
        "rotation_strategy": "round_robin"
    },
    "groq/llama-3.1-70b-versatile": {
        "keys": ["gsk-key1"]
    }
}

with open("demo_config.json", "w") as f:
    json.dump(config, f, indent=2)

print("Created demo_config.json")

# Initialize with config file
client = LLMClient("demo_config.json")

print("\n--- Testing Cerebras (should rotate keys) ---")
try:
    # This might fail with invalid keys, but shows the usage
    client.completion(
        model="cerebras/llama3.1-70b",
        messages=[{"role": "user", "content": "Hi"}]
    )
except Exception as e:
    print(f"Request failed (expected with fake keys): {e}")

print("\n--- Testing Groq ---")
try:
    client.completion(
        model="groq/llama-3.1-70b-versatile",
        messages=[{"role": "user", "content": "Hi"}]
    )
except Exception as e:
    print(f"Request failed (expected with fake keys): {e}")
