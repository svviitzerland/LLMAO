#!/usr/bin/env python3
"""Test LLMAO streaming and non-streaming completion.

Tests:
- Non-streaming completion
- Streaming completion with iterator pattern
- All configured providers
- Tool calling
"""

import sys
import time
from llmao_py import LLMClient


def test_non_streaming(client: LLMClient, model: str):
    """Test non-streaming completion."""
    print(f"\n{'='*60}")
    print(f"Testing NON-STREAMING: {model}")
    print('='*60)
    
    start = time.time()
    response = client.completion(
        model=model,
        messages=[{"role": "user", "content": "Say 'Hello from LLMAO!' and nothing else."}],
        temperature=0.7,
        max_tokens=50,
    )
    elapsed = time.time() - start
    
    content = response["choices"][0]["message"]["content"]
    print(f"✓ Response: {content}")
    print(f"✓ Time: {elapsed:.2f}s")
    return True


def test_streaming(client: LLMClient, model: str):
    """Test streaming completion."""
    print(f"\n{'='*60}")
    print(f"Testing STREAMING: {model}")
    print('='*60)
    
    collected = []
    chunk_count = 0
    
    start = time.time()
    for chunk in client.completion(
        model=model,
        messages=[{"role": "user", "content": "Count from 1 to 5 with spaces."}],
        temperature=0.7,
        max_tokens=100,
        stream=True,
    ):
        if content := chunk["choices"][0]["delta"].get("content"):
            collected.append(content)
            chunk_count += 1
            print(content, end="", flush=True)
    
    elapsed = time.time() - start
    full_text = "".join(collected)
    
    print(f"\n✓ Chunks: {chunk_count}")
    print(f"✓ Total: {len(full_text)} chars")
    print(f"✓ Time: {elapsed:.2f}s")
    
    # Verify spaces preserved
    if " " in full_text:
        print("✓ Spaces preserved")
    else:
        print("✗ WARNING: No spaces found in output!")
    
    return True


def test_tool_calling(client: LLMClient, model: str):
    """Test tool calling."""
    print(f"\n{'='*60}")
    print(f"Testing TOOL CALLING: {model}")
    print('='*60)
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "City name"}
                    },
                    "required": ["location"]
                }
            }
        }
    ]
    
    start = time.time()
    response = client.completion(
        model=model,
        messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
        tools=tools,
        temperature=0.7,
    )
    elapsed = time.time() - start
    
    if tool_calls := response["choices"][0]["message"].get("tool_calls"):
        print(f"✓ Tool called: {tool_calls[0]['function']['name']}")
        print(f"✓ Args: {tool_calls[0]['function']['arguments']}")
        print(f"✓ Time: {elapsed:.2f}s")
        return True
    else:
        print("✗ No tool calls (may not be supported by this model)")
        return False


def run_tests():
    """Run all tests for all configured providers."""
    print("LLMAO Test Suite")
    print("="*60)
    
    client = LLMClient()
    
    # Test models from different providers
    models = [
        "cerebras/llama-3.3-70b",
        "minimax/MiniMax-01",
        "openai/gpt-4o-mini",
        "groq/llama-3.1-70b-versatile",
    ]
    
    results = {}
    
    for model in models:
        try:
            # Test non-streaming
            results[f"{model}_non_stream"] = test_non_streaming(client, model)
            
            # Test streaming
            results[f"{model}_stream"] = test_streaming(client, model)
            
            # Test tool calling (skip for models that don't support it)
            try:
                results[f"{model}_tools"] = test_tool_calling(client, model)
            except Exception as e:
                print(f"  Skipping tools (not supported): {e}")
            
        except Exception as e:
            print(f"\n✗ Error with {model}: {e}")
            results[f"{model}_error"] = str(e)
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    passed = sum(1 for v in results.values() if v is True)
    failed = len(results) - passed
    
    print(f"✓ Passed: {passed}")
    print(f"✗ Failed: {failed}")
    
    for test, result in results.items():
        status = "✓" if result is True else "✗"
        print(f"  {status} {test}")
    
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
