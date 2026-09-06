"""
Anthropic API Integration Wrapper for PersonaScript.

Handles standard Anthropic API client initialization and text generation,
as well as LangChain and LlamaIndex model wrappers.
"""

import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class AnthropicIntegration:
    """Wrapper class for Anthropic API operations."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Anthropic Integration wrapper.

        Args:
            api_key: Optional Anthropic API key. If not provided, will look for the
                     ANTHROPIC_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.client = None

        if self.api_key:
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=self.api_key)
                logger.info("Anthropic client initialized successfully.")
            except ImportError:
                logger.error("Failed to import 'anthropic' library.")
            except Exception as e:
                logger.error(f"Error initializing Anthropic client: {e}")
        else:
            logger.warning("No Anthropic API key provided. Operating in mock mode.")

    def is_configured(self) -> bool:
        """Check if the integration is configured with an API key."""
        return self.api_key is not None

    def generate_text(self, prompt: str, model: str = "claude-3-5-sonnet-latest", max_tokens: int = 150, temperature: float = 0.7, **kwargs) -> str:
        """
        Generate text using the Anthropic API.

        Args:
            prompt: Input prompt.
            model: Model name to use.
            max_tokens: Maximum number of tokens in completion.
            temperature: Sampling temperature.

        Returns:
            The generated string or mock text if not fully configured.
        """
        logger.info(f"Generating text with Anthropic model: {model}")
        if not self.is_configured() or not self.client:
            logger.warning("Using Mock Anthropic response.")
            return f"[Mock Anthropic response for model '{model}']: This is a mock response to the prompt: '{prompt}'"

        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            # Anthropic messages response has .content list of ContentBlock items
            if response.content:
                return response.content[0].text
            return ""
        except Exception as e:
            logger.error(f"Anthropic text generation error: {e}")
            raise e

    def get_langchain_llm(self, model: str = "claude-3-5-sonnet-latest", temperature: float = 0.7, **kwargs):
        """
        Get a LangChain LLM instance configured with this integration's API key.

        Returns:
            An instance of ChatAnthropic from langchain_community or langchain_anthropic.
        """
        if not self.is_configured():
            logger.warning("Returning LangChain FakeListChatModel due to missing credentials.")
            from langchain_core.language_models.fake_chat_models import FakeListChatModel
            return FakeListChatModel(responses=["[Fake LangChain Anthropic Response]"])

        try:
            # Try importing langchain_anthropic first, fallback to langchain_community
            try:
                from langchain_anthropic import ChatAnthropic
            except ImportError:
                from langchain_community.chat_models import ChatAnthropic

            return ChatAnthropic(
                anthropic_api_key=self.api_key,
                model=model,
                temperature=temperature,
                **kwargs
            )
        except ImportError:
            logger.error("LangChain Anthropic components are not installed or cannot be imported.")
            raise ImportError("Please install 'langchain-anthropic' or 'langchain-community' to use LangChain wrappers.")

    def get_llamaindex_llm(self, model: str = "claude-3-5-sonnet-latest", temperature: float = 0.7, **kwargs):
        """
        Get a LlamaIndex LLM instance configured with this integration's API key.

        Returns:
            An instance of Anthropic from llama_index.llms.anthropic.
        """
        if not self.is_configured():
            logger.warning("LlamaIndex Mock LLM returned due to missing credentials.")
            from llama_index.core.llms import MockLLM
            return MockLLM(max_tokens=100)

        try:
            from llama_index.llms.anthropic import Anthropic as LlamaAnthropic
            return LlamaAnthropic(
                api_key=self.api_key,
                model=model,
                temperature=temperature,
                **kwargs
            )
        except ImportError:
            logger.error("LlamaIndex Anthropic components are not installed or cannot be imported.")
            raise ImportError("Please install 'llama-index-llms-anthropic' to use LlamaIndex wrappers.")
