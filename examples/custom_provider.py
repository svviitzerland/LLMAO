"""Example 4: Custom Provider

Using a provider that is NOT in the built-in registry.
"""
from llmao_py import LLMClient

# Define custom provider config
custom_config = {
    "my_custom_llm/model-v1": {
        "base_url": "https://api.openai.com/v1",  # Using OpenAI as a "custom" endpoint for demo
        "keys": ["sk-placeholder"],
        "headers": {
            "X-Custom-Header": "custom-value"
        },
        "param_mappings": {
             "max_completion_tokens": "max_tokens"
        }
    }
}

client = LLMClient(config=custom_config)

print("Sending request to custom provider...")
try:
    # Note: We use the full "provider/model" key here
    response = client.completion(
        model="my_custom_llm/model-v1",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(f"Response: {response}")
except Exception as e:
    print(f"Error: {e}")
