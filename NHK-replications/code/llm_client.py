"""
This module provides a client for interacting with Large Language Model (LLM) APIs. It supports providers like Mistral and Google Gemini, allowing users to send prompts and receive responses with usage information such as token counts.
"""

# This import allows using type hints with forward references (e.g., class names before they're defined)
from __future__ import annotations

# Import dataclass decorator to create simple classes that mainly hold data
from dataclasses import dataclass
# Import type hints for better code documentation and error checking
from typing import Any, Dict, Optional

from mistralai import Mistral
from google import genai
from google.genai import types as genai_types


# A dataclass is a simple class that automatically generates methods like __init__ and __repr__
# This class holds the response data from an LLM API call
@dataclass
class LLMResponse:
    content: str  # The text content of the LLM's response
    usage: Dict[str, Any]  # Dictionary containing token usage information
    model: str  # The name of the model that was used


# A class is a blueprint for creating objects. This class provides methods to interact with LLM APIs
class LLMClient:
    # __init__ is the constructor method, called when creating a new instance of the class
    def __init__(self, provider: str, api_key: str):
        # self refers to the instance of the class being created
        self.provider = provider.lower()  # Convert provider name to lowercase for consistency
        # if/elif/else are conditional statements that execute different code based on conditions
        if self.provider == "mistral":
            self._client = Mistral(api_key=api_key)  # Create Mistral API client
        elif self.provider in {"google", "gemini"}:  # Check if provider is google or gemini
            self._client = genai.Client(api_key=api_key)  # Create Google Gemini API client
        else:
            # raise raises an exception to indicate an error
            raise ValueError(f"Unsupported provider: {provider}")  # Error for unknown providers

    # This method sends a prompt to the LLM and gets a response
    def complete(
        self,
        prompt: str,  # The text prompt to send to the LLM
        model: str,  # The name of the model to use
        random_seed: Optional[int] = None,  # Optional seed for reproducible results
        temperature: float = 0.7,  # Controls randomness (0.0 = deterministic, 1.0 = very random)
    ) -> LLMResponse:  # The -> indicates the return type
        """Returns {'content': str, 'usage': {...}, 'model': str}"""  # This is a docstring explaining the method
        if self.provider == "mistral":
            # Call the Mistral API to complete the chat
            response = self._client.chat.complete(  # type: ignore
                model=model,
                messages=[{"role": "user", "content": prompt}],  # List of messages in chat format
                temperature=temperature,
                random_seed=random_seed,
            )

            # Extract the content from the response
            content = response.choices[0].message.content  # type: ignore
            # Create a dictionary with usage information
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,  # Tokens used in the prompt
                "completion_tokens": response.usage.completion_tokens,  # Tokens used in the response
                "total_tokens": response.usage.total_tokens,  # Total tokens used
            }
            # Return an LLMResponse object with the extracted data
            return LLMResponse(content=content, usage=usage, model=response.model)  # type: ignore

        # This else block handles the Google Gemini provider
        # Call the Google Gemini API to generate content
        response = self._client.models.generate_content(  # type: ignore
            model=model,
            contents=prompt,  # The prompt text
            config=genai_types.GenerateContentConfig(  # Configuration object
                temperature=temperature,
                seed=random_seed,
            ),
        )

        # Get usage metadata, or empty dict if none
        usage_meta = response.usage_metadata or {}  # type: ignore
        # Create usage dictionary using getattr to safely get attributes
        usage = {
            "prompt_tokens": getattr(usage_meta, "prompt_token_count", None),
            "completion_tokens": getattr(usage_meta, "candidates_token_count", None),
            "total_tokens": getattr(usage_meta, "total_token_count", None),
        }
        # Return LLMResponse with content (or empty string if none) and other data
        return LLMResponse(content=response.text or "", usage=usage, model=model)
