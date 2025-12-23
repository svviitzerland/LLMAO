<div align="center">

<img src="assets/logo.svg" alt="LLMAO Logo" width="150" height="150" />

# LLMAO

**Lightweight LLM API Orchestrator**

*One interface for all your LLM APIs, fast and simple*

[![Python](https://img.shields.io/badge/python-3.9+-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/llmao/)
[![Rust](https://img.shields.io/badge/Built%20with-Rust-dea584?style=flat&logo=rust&logoColor=white)](https://www.rust-lang.org/)
[![License](https://img.shields.io/github/license/svviitzerland/llmao?style=flat)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/svviitzerland/llmao/ci.yml?style=flat&logo=github&label=CI)](https://github.com/svviitzerland/llmao/actions)

</div>

---

A unified Python interface for multiple LLM providers with automatic key rotation and rate limit handling. Built with Rust core for performance.

## Installation

```bash
pip install llmao-py
```

## Quick Start

```python
from llmao import LLMClient

client = LLMClient()

response = client.completion(
    model="groq/llama-3.1-70b-versatile",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response["choices"][0]["message"]["content"])
```

## Model Format

Use `provider/model` routing:

```python
# OpenAI
client.completion(model="openai/gpt-4o", messages=[...])

# Anthropic
client.completion(model="anthropic/claude-3-5-sonnet-20241022", messages=[...])

# Groq
client.completion(model="groq/llama-3.3-70b-versatile", messages=[...])

# Cerebras
client.completion(model="cerebras/llama3.1-70b", messages=[...])
```

## Supported Providers

<details>
<summary>View all providers</summary>

| Provider | Environment Variable |
|----------|---------------------|
| OpenAI | `OPENAI_API_KEY` |
| Anthropic | `ANTHROPIC_API_KEY` |
| Groq | `GROQ_API_KEY` |
| Cerebras | `CEREBRAS_API_KEY` |
| Together | `TOGETHER_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| DeepSeek | `DEEPSEEK_API_KEY` |
| Mistral | `MISTRAL_API_KEY` |
| Fireworks | `FIREWORKS_API_KEY` |
| Perplexity | `PERPLEXITY_API_KEY` |
| SambaNova | `SAMBANOVA_API_KEY` |
| NVIDIA | `NVIDIA_API_KEY` |
| Hyperbolic | `HYPERBOLIC_API_KEY` |
| DeepInfra | `DEEPINFRA_API_KEY` |
| Novita | `NOVITA_API_KEY` |
| Xiaomi MiMo | `XIAOMI_MIMO_API_KEY` |
| Venice AI | `VENICE_AI_API_KEY` |
| GLHF | `GLHF_API_KEY` |
| Lepton | `LEPTON_API_KEY` |
| Anyscale | `ANYSCALE_API_KEY` |
| Ollama | `OLLAMA_API_KEY` |
| LM Studio | `LMSTUDIO_API_KEY` |

</details>

## Key Rotation

Automatic failover when rate limited. Configure multiple keys in your `config.json`:

```json
{
  "openai/gpt-4": {
    "keys": ["sk-key1", "sk-key2", "sk-key3"],
    "rotation_strategy": "round_robin"
  }
}
```

Or use environment variables (suffix with `_2`, `_3`, etc.):
```bash
export OPENAI_API_KEY="sk-key1"
export OPENAI_API_KEY_2="sk-key2"
export OPENAI_API_KEY_3="sk-key3"
```

## Configuration

Create a `config.json` in your project to configure models and API keys:

### Format 1: Specific Model

Configure individual models with their own keys:

```json
{
  "cerebras/llama3.1-70b": {
    "keys": ["csk-key1", "csk-key2", "csk-key3"],
    "rotation_strategy": "round_robin"
  },
  "groq/llama-3.1-70b-versatile": {
    "keys": ["gsk-key1"]
  }
}
```

### Format 2: Provider Level

Configure multiple models from the same provider sharing keys:

```json
{
  "cerebras": {
    "models": ["llama3.1-70b", "llama3.3-70b"],
    "keys": ["csk-key1", "csk-key2"],
    "rotation_strategy": "round_robin"
  }
}
```

### Custom Providers

For providers not in the built-in registry, specify `base_url`:

```json
{
  "my_custom_llm/model-v1": {
    "base_url": "https://api.custom.com/v1",
    "keys": ["custom-key"],
    "headers": {
      "X-Custom-Header": "value"
    }
  }
}
```

**Configuration Options:**
- `keys` (required): List of API keys
- `models` (for provider-level): List of model names
- `rotation_strategy`: `"round_robin"` (default), `"random"`, or `"least_recently_used"`
- `base_url`: Custom API endpoint (required for unknown providers)
- `headers`: Custom HTTP headers
- `param_mappings`: Map parameter names (e.g., `max_completion_tokens` → `max_tokens`)

See [`CONFIG_EXAMPLES.md`](CONFIG_EXAMPLES.md) for more examples.

## Contributing Providers

Want to add a new provider to LLMAO's built-in registry? 

The `providers.json` file contains provider metadata (base URLs, default headers, etc.). Fork the repository, add your provider, and submit a pull request:

```json
{
  "your_provider": {
    "base_url": "https://api.yourprovider.com/v1",
    "api_key_env": "YOUR_PROVIDER_API_KEY"
  }
}
```

Once merged, all users can use your provider without specifying `base_url`!

## API Reference

```python
from llmao import LLMClient, completion

# Client-based
client = LLMClient(config_path="./config.json")
client.completion(model, messages, temperature=0.7, max_tokens=100)
client.providers()  # List available providers
client.provider_info("openai")  # Get provider details

# Quick function
completion(model, messages, **kwargs)
```

## Development

```bash
# Build from source
pip install maturin
maturin develop

# Run tests
cargo test
```

## License

MIT

