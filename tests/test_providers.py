#!/usr/bin/env python3
"""Test all LLMAO providers individually.

Quick smoke test for each provider to verify configuration.
"""

import sys
from llmao_py import LLMClient


PROVIDERS = {
    "OpenAI": ["openai/gpt-4o-mini", "openai/gpt-3.5-turbo"],
    "Cerebras": ["cerebras/llama-3.3-70b", "cerebras/llama-3.1-8b"],
    "Groq": ["groq/llama-3.1-70b-versatile", "groq/mixtral-8x7b-32768"],
    "MiniMax": ["minimax/MiniMax-01"],
    "OpenRouter": ["openrouter/anthropic/claude-3.5-sonnet"],
}


def test_provider(provider_name: str, models: list[str]):
    """Test a provider with quick requests."""
    print(f"\n{'='*60}")
    print(f"Testing Provider: {provider_name}")
    print('='*60)
    
    client = LLMClient()
    results = []
    
    for model in models:
        try:
            print(f"\n  Testing {model}... ", end="", flush=True)
            
            # Quick non-streaming test
            response = client.completion(
                model=model,
                messages=[{"role": "user", "content": "Say OK"}],
                max_tokens=10,
            )
            
            content = response["choices"][0]["message"]["content"]
            print(f"✓ ({content.strip()[:20]})")
            results.append(True)
            
        except Exception as e:
            print(f"✗ Error: {e}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    print(f"\n  {provider_name}: {passed}/{total} passed")
    
    return passed == total


def main():
    """Test all providers."""
    print("LLMAO Provider Test Suite")
    print("="*60)
    print("Testing all configured providers...")
    
    all_passed = []
    
    for provider, models in PROVIDERS.items():
        passed = test_provider(provider, models)
        all_passed.append(passed)
    
    # Summary
    print(f"\n{'='*60}")
    print("PROVIDER SUMMARY")
    print('='*60)
    
    total_passed = sum(all_passed)
    total_providers = len(all_passed)
    
    print(f"Providers working: {total_passed}/{total_providers}")
    
    return total_passed == total_providers


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
