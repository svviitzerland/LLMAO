# LLMAO Examples

This directory contains examples demonstrating different ways to configure and use LLMAO.

## Examples

- **[`simple_chat.py`](simple_chat.py)**:  
  Basic usage. Relies on environment variables or default registry settings.

- **[`multi_provider.py`](multi_provider.py)**:  
  Demonstrates how to use a `config.json` file to manage multiple providers and API keys (with rotation).

- **[`programmatic_config.py`](programmatic_config.py)**:  
  **New!** Shows how to configure LLMAO entirely in code using a dictionary, without needing external config files.

- **[`custom_provider.py`](custom_provider.py)**:  
  Shows how to use a provider that isn't in the built-in registry by specifying a `base_url`.

## Running the Examples

Make sure you have installed the package:
```bash
pip install llmao-py
```

Then run any example:
```bash
python simple_chat.py
```
