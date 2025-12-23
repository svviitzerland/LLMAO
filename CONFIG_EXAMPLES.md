# LLMAO Configuration Examples

## Example 1: Simple Single Model

```json
{
  "cerebras/llama3.1-70b": {
    "keys": ["csk-your-api-key-here"],
    "rotation_strategy": "round_robin"
  }
}
```

## Example 2: Provider with Multiple Models 

```json
{
  "cerebras": {
    "models": ["llama3.1-70b", "llama3.3-70b"],
    "keys": [
      "csk-key1",
      "csk-key2",
      "csk-key3"
    ],
    "rotation_strategy": "round_robin"
  }
}
```

## Example 3: Multiple Providers

```json
{
  "cerebras/llama3.1-70b": {
    "keys": ["csk-key1", "csk-key2"]
  },
  "groq/llama-3.1-70b-versatile": {
    "keys": ["gsk-key1"]
  },
  "openai/gpt-4": {
    "keys": ["sk-proj-xxx"]
  }
}
```

## Example 4: Custom Provider

```json
{
  "my_custom_llm": {
    "base_url": "https://api.mycustom.com/v1",
    "models": ["custom-model-v1"],
    "keys": ["custom-api-key"],
    "headers": {
      "X-Custom-Header": "value"
    }
  }
}
```

## Example 5: Complex Mix

```json
{
  "cerebras": {
    "models": ["llama3.1-70b", "llama3.3-70b"],
    "keys": ["csk-key1", "csk-key2"],
    "rotation_strategy": "round_robin"
  },
  "groq/llama-3.1-8b-instant": {
    "keys": ["gsk-fast-key"]
  },
  "my_custom_api/model-v1": {
    "base_url": "https://api.custom.ai/v1",
    "keys": ["custom-key"],
    "param_mappings": {
      "max_completion_tokens": "max_tokens"
    }
  }
}
```
