"""
Simple configuration example with multiple providers.

This example demonstrates the new simplified config format
with both specific model and provider-level configurations.
"""

import json
import tempfile
import os
from llmao import LLMClient

# Example: Simple multi-provider configuration
SIMPLE_CONFIG = {
    # Specific model with multiple keys
    "cerebras/llama3.1-70b": {
        "keys": ["csk-key1", "csk-key2", "csk-key3"],
        "rotation_strategy": "round_robin"
    },
    
    # Another specific model
    "groq/llama-3.1-70b-versatile": {
        "keys": ["gsk-key1"]
    }
}

# Example: Provider-level configuration
PROVIDER_LEVEL_CONFIG = {
    # All Cerebras models share the same keys
    "cerebras": {
        "models": ["llama3.1-70b", "llama3.3-70b"],
        "keys": ["csk-key1", "csk-key2"],
        "rotation_strategy": "round_robin"
    }
}

def demo_simple_config():
    """Demo simple specific model configuration."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(SIMPLE_CONFIG, f)
        config_path = f.name
    
    try:
        client = LLMClient(config_path=config_path)
        print("Simple config - Configured models:")
        print("  - cerebras/llama3.1-70b (3 keys)")
        print("  - groq/llama-3.1-70b-versatile (1 key)")
    finally:
        os.unlink(config_path)

def demo_provider_level_config():
    """Demo provider-level configuration."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(PROVIDER_LEVEL_CONFIG, f)
        config_path = f.name
    
    try:
        client = LLMClient(config_path=config_path)
        print("\nProvider-level config - Configured models:")
        print("  - cerebras/llama3.1-70b (2 keys, shared)")
        print("  - cerebras/llama3.3-70b (2 keys, shared)")
    finally:
        os.unlink(config_path)

if __name__ == "__main__":
    demo_simple_config()
    demo_provider_level_config()
