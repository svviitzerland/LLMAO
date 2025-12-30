"""
Type stubs for LLMAO - Lightweight LLM API Orchestrator
"""

from typing import Any, Iterator, Optional, TypedDict, Union

class Message(TypedDict, total=False):
    role: str
    content: str
    name: Optional[str]
    tool_calls: Optional[list[dict[str, Any]]]
    tool_call_id: Optional[str]

class Choice(TypedDict, total=False):
    index: int
    message: Message
    finish_reason: Optional[str]

class StreamChoice(TypedDict, total=False):
    index: int
    delta: dict[str, Any]
    finish_reason: Optional[str]

class Usage(TypedDict):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class CompletionResponse(TypedDict, total=False):
    id: str
    object: str
    created: int
    model: str
    choices: list[Choice]
    usage: Optional[Usage]

class StreamChunk(TypedDict, total=False):
    id: str
    object: str
    created: int
    model: str
    choices: list[StreamChoice]

class LLMClient:
    """
    Lightweight LLM API client with multi-provider support.
    
    Example:
        ```python
        from llmao import LLMClient
        
        # Non-streaming
        client = LLMClient()
        response = client.completion(
            model="openai/gpt-4",
            messages=[{"role": "user", "content": "Hello!"}]
        )
        print(response["choices"][0]["message"]["content"])
        
        # Streaming
        for chunk in client.completion(
            model="cerebras/llama-3.3-70b",
            messages=[{"role": "user", "content": "Hello!"}],
            stream=True
        ):
            content = chunk["choices"][0]["delta"].get("content", "")
            print(content, end="", flush=True)
        ```
    """
    
    def __init__(self, config_path: Optional[str] = None) -> None: ...
    
    def completion(
        self,
        messages: list[dict[str, Any]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        tools: Optional[list[dict[str, Any]]] = None,
        **kwargs: Any
    ) -> Union[CompletionResponse, Iterator[StreamChunk]]:
        """
        Create a chat completion.
        
        Args:
            messages: List of message dicts with 'role' and 'content' keys.
            model: Model identifier in format "provider/model".
                   Examples: "openai/gpt-4", "groq/llama-3.1-70b-versatile"
            temperature: Sampling temperature (0.0 to 2.0).
            max_tokens: Maximum tokens to generate.
            stream: If True, returns iterator; if False, returns complete response.
            tools: Tool definitions for function calling.
            **kwargs: Additional provider-specific parameters.
        
        Returns:
            CompletionResponse dict if stream=False, Iterator[StreamChunk] if stream=True.
        
        Example:
            ```python
            # Non-streaming
            response = client.completion(
                model="openai/gpt-4",
                messages=[{"role": "user", "content": "Hello!"}]
            )
            print(response["choices"][0]["message"]["content"])
            
            # Streaming
            for chunk in client.completion(
                model="openai/gpt-4",
                messages=[{"role": "user", "content": "Hello!"}],
                stream=True
            ):
                if content := chunk["choices"][0]["delta"].get("content"):
                    print(content, end="", flush=True)
            ```
        """
        ...
    
    def providers(self) -> list[str]:
        """List available provider names."""
        ...
    
    def provider_info(self, name: str) -> Optional[dict[str, Any]]:
        """Get information about a specific provider."""
        ...

def completion(
    model: str,
    messages: list[dict[str, Any]],
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    stream: bool = False,
    **kwargs: Any
) -> Union[CompletionResponse, Iterator[StreamChunk]]:
    """
    Quick completion without explicit client initialization.
    
    Example:
        ```python
        from llmao import completion
        
        # Non-streaming
        response = completion(
            model="groq/llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": "Hello!"}]
        )
        
        # Streaming  
        for chunk in completion(
            model="openai/gpt-4",
            messages=[{"role": "user", "content": "Hello!"}],
            stream=True
        ):
            print(chunk["choices"][0]["delta"].get("content", ""), end="")
        ```
    """
    ...

__version__: str
