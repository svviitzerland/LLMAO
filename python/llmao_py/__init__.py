"""
LLMAO - Lightweight LLM API Orchestrator

A fast, multi-provider LLM client with rate limiting and key rotation.
"""

from ._llmao import LLMClient as _RustLLMClient, completion as _rust_completion, __version__
from typing import Any, Iterator, Union
import queue
import threading


class LLMClient:
    """
    Python wrapper for LLMClient that provides clean streaming API.
    
    Example:
        # Non-streaming
        client = LLMClient()
        response = client.completion(messages=[...])
        
        # Streaming
        for chunk in client.completion(messages=[...], stream=True):
            print(chunk['choices'][0]['delta']['content'])
    """
    
    def __init__(self, config_path: str | None = None):
        self._client = _RustLLMClient(config_path) if config_path else _RustLLMClient()
    
    def completion(
        self,
        messages: list[dict[str, Any]],
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        stream: bool = False,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any
    ) -> Union[dict[str, Any], Iterator[dict[str, Any]]]:
        """
        Create a chat completion.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model in format 'provider/model'
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Max tokens to generate
            stream: If True, returns iterator of chunks; if False, returns complete response
            tools: Tool definitions for function calling
            **kwargs: Additional provider-specific params
        
        Returns:
            dict if stream=False, Iterator[dict] if stream=True
        """
        if not stream:
            # Non-streaming: use existing Rust method
            return self._client.completion(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
        
        # Streaming: convert callback to iterator
        chunk_queue = queue.Queue()
        done_event = threading.Event()
        error_holder = []
        
        def on_chunk(chunk: dict):
            """Callback for each streaming chunk"""
            chunk_queue.put(chunk)
        
        def run_stream():
            """Run streaming in background thread"""
            try:
                self._client.stream_with_callback(
                    callback=on_chunk,
                    messages=messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    tools=tools,
                    **kwargs
                )
            except Exception as e:
                error_holder.append(e)
            finally:
                done_event.set()
        
        # Start streaming thread
        thread = threading.Thread(target=run_stream, daemon=True)
        thread.start()
        
        # Yield chunks as iterator
        while not done_event.is_set() or not chunk_queue.empty():
            try:
                chunk = chunk_queue.get(timeout=0.1)
                
                # Convert to OpenAI-style streaming format
                yield {
                    'id': chunk.get('id', ''),
                    'object': 'chat.completion.chunk',
                    'created': chunk.get('created', 0),
                    'model': chunk.get('model', ''),
                    'choices': [{
                        'index': chunk.get('index', 0),
                        'delta': {
                            k: v for k, v in {
                                'role': chunk.get('role'),
                                'content': chunk.get('content'),
                                'tool_calls': chunk.get('tool_calls'),
                            }.items() if v is not None
                        },
                        'finish_reason': chunk.get('finish_reason'),
                    }]
                }
            except queue.Empty:
                if error_holder:
                    raise error_holder[0]
                continue
        
        # Check for final errors
        if error_holder:
            raise error_holder[0]
    
    def providers(self) -> list[str]:
        """List available providers"""
        return self._client.providers()
    
    def provider_info(self, name: str) -> dict | None:
        """Get provider information"""
        return self._client.provider_info(name)


def completion(
    model: str,
    messages: list[dict[str, Any]],
    temperature: float | None = None,
    max_tokens: int | None = None,
    stream: bool = False,
    **kwargs: Any
) -> Union[dict[str, Any], Iterator[dict[str, Any]]]:
    """
    Quick completion without explicit client.
    
    Example:
        from llmao import completion
        
        # Non-streaming
        response = completion(model="openai/gpt-4", messages=[...])
        
        # Streaming
        for chunk in completion(model="openai/gpt-4", messages=[...], stream=True):
            print(chunk['choices'][0]['delta'].get('content', ''), end='')
    """
    client = LLMClient()
    return client.completion(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=stream,
        **kwargs
    )


__all__ = ["LLMClient", "completion", "__version__"]
