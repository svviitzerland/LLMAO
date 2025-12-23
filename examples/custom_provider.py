"""
Custom provider configuration example.

This example shows how to configure custom providers and models
using the new simplified configuration format.
"""

import json
import tempfile
import os
from llmao import LLMClient

# New custom configuration format
CUSTOM_CONFIG = {
    # Provider-level config: all models share the same keys
    "groq": {
        "models": ["llama-3.1-70b-versatile", "llama-3.3-70b-versatile"],
        "keys": [
            os.getenv("GROQ_API_KEY", "your-groq-key"),
            os.getenv("GROQ_API_KEY_2", "your-groq-key-2")
        ],
        "rotation_strategy": "round_robin"
    },
    
    # Specific model config with custom base_url
    "my_custom_provider/my-model": {
        "base_url": "https://api.my-provider.com/v1",
        "keys": [os.getenv("MY_CUSTOM_API_KEY", "your-custom-key")],
        "headers": {
            "X-Custom-Header": "my-value"
        },
        "param_mappings": {
            "max_completion_tokens": "max_tokens"
        }
    }
}

def main():
    # Write custom config to a temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(CUSTOM_CONFIG, f)
        config_path = f.name
    
    try:
        # Create client with custom config
        client = LLMClient(config_path=config_path)
        
        print("Available providers:")
        for provider in client.providers():
            info = client.provider_info(provider)
            if info:
                print(f"  - {provider}: {info['base_url']}")
        
        print("\nConfigured models:")
        print("  - groq/llama-3.1-70b-versatile (2 keys, round robin)")
        print("  - groq/llama-3.3-70b-versatile (2 keys, round robin)")
        print("  - my_custom_provider/my-model (1 key)")
        
        # Example usage (uncomment if you have real keys):
        # response = client.completion(
        #     model="groq/llama-3.1-70b-versatile",
        #     messages=[{"role": "user", "content": "Hello!"}]
        # )
        # print(response["choices"][0]["message"]["content"])
        
    finally:
        os.unlink(config_path)

if __name__ == "__main__":
    main()
