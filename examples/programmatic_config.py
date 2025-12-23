"""Example 3: Programmatic Configuration

Configuring LLMAO directly with a dictionary (no config file needed).
Useful for dynamic configuration or when config is loaded from other sources.
"""
import os
from llmao_py import LLMClient

# Define configuration in code
# This overrides any config files
my_config = {
    # Provider-level config with multiple models and keys
    "cerebras": {
        "models": ["llama3.1-70b"],
        "keys": [
            os.environ.get("CEREBRAS_API_KEY", "csk-placeholder"),
            "csk-backup-key" 
        ],
        "rotation_strategy": "round_robin"
    },
    
    # Specific model config
    "groq/llama-3.1-70b-versatile": {
        "keys": ["gsk-placeholder-key"]
    }
}

print("Initializing with dictionary config...")
client = LLMClient(config=my_config)

print("\nConfig loaded:")
info = client.provider_info("cerebras")
print(f"Cerebras models: {info.get('models')}")
print(f"Has keys: {info.get('has_keys')}")

print("\nSending request...")
try:
    response = client.completion(
        model="cerebras/llama3.1-70b",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(f"Response: {response['choices'][0]['message']['content']}")
except Exception as e:
    print(f"Error (likely due to placeholder keys): {e}")
