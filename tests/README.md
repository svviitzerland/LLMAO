# LLMAO Test Suite

Comprehensive tests for LLMAO streaming and non-streaming functionality.

## Test Files

### `test_completion.py`
Complete test suite covering:
- ✅ Non-streaming completion
- ✅ Streaming completion with iterator pattern
- ✅ Space preservation in streaming
- ✅ Tool calling
- ✅ All providers

### `test_providers.py`
Quick smoke tests for each provider:
- OpenAI
- Cerebras
- Groq
- MiniMax
- OpenRouter

## Running Tests

### All Tests
```bash
cd /home/lian/Documents/tools/llmao
poetry run python tests/test_completion.py
```

### Provider Tests Only
```bash
poetry run python tests/test_providers.py
```

### Quick Test (Single Model)
```python
from llmao_py import LLMClient

client = LLMClient()

# Non-streaming
response = client.completion(
    model="cerebras/llama-3.3-70b",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response["choices"][0]["message"]["content"])

# Streaming
for chunk in client.completion(
    model="cerebras/llama-3.3-70b",
    messages=[{"role": "user", "content": "Count to 5"}],
    stream=True
):
    if content := chunk["choices"][0]["delta"].get("content"):
        print(content, end="", flush=True)
```

## Requirements

- LLMAO installed: `poetry run maturin develop --release`
- API keys configured in `~/.llmao/config.json` or environment variables
- Active internet connection

## Expected Results

All tests should pass with:
- ✓ Streaming preserves spaces
- ✓ Tool calls work (where supported)
- ✓ All configured providers respond
- ✓ No character concatenation issues

## Troubleshooting

**Spaces missing in streaming output?**
- Check backend uses chunk-based sending, not character-by-character
- Verify frontend doesn't strip whitespace

**Provider not working?**
- Check API key in config or environment
- Verify provider is in `config.json`
- Test with `curl` to isolate LLMAO vs provider issues
