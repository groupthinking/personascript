"""
OpenAI API Integration Wrapper for PersonaScript.

Handles standard OpenAI API client initialization and text generation,
as well as LangChain and LlamaIndex model wrappers.
"""

import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class OpenAIIntegration:
    """Wrapper class for OpenAI API operations."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OpenAI Integration wrapper.

        Args:
            api_key: Optional OpenAI API key. If not provided, will look for the
                     OPENAI_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.client = None

        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                logger.info("OpenAI client initialized successfully.")
            except ImportError:
                logger.error("Failed to import 'openai' library.")
            except Exception as e:
                logger.error(f"Error initializing OpenAI client: {e}")
        else:
            logger.warning("No OpenAI API key provided. Operating in mock mode.")

    def is_configured(self) -> bool:
        """Check if the integration is configured with an API key."""
        return self.api_key is not None

    def generate_text(self, prompt: str, model: str = "gpt-4o-mini", max_tokens: int = 150, temperature: float = 0.7, **kwargs) -> str:
        """
        Generate text using the OpenAI Chat Completion API.

        Args:
            prompt: Input prompt.
            model: Model name to use.
            max_tokens: Maximum number of tokens in completion.
            temperature: Sampling temperature.

        Returns:
            The generated string or mock text if not fully configured.
        """
        logger.info(f"Generating text with OpenAI model: {model}")
        if not self.is_configured() or not self.client:
            logger.warning("Using Mock OpenAI response.")
            return f"[Mock OpenAI response for model '{model}']: This is a mock response to the prompt: '{prompt}'"

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"OpenAI text generation error: {e}")
            raise e

    def get_langchain_llm(self, model: str = "gpt-4o-mini", temperature: float = 0.7, **kwargs):
        """
        Get a LangChain LLM instance configured with this integration's API key.

        Returns:
            An instance of ChatOpenAI from langchain_community or langchain_openai.
        """
        if not self.is_configured():
            logger.warning("Returning LangChain FakeListChatModel due to missing credentials.")
            from langchain_core.language_models.fake_chat_models import FakeListChatModel
            return FakeListChatModel(responses=["[Fake LangChain OpenAI Response]"])

        try:
            # Try importing langchain_openai first, fallback to langchain_community
            try:
                from langchain_openai import ChatOpenAI
            except ImportError:
                from langchain_community.chat_models import ChatOpenAI

            return ChatOpenAI(
                openai_api_key=self.api_key,
                model=model,
                temperature=temperature,
                **kwargs
            )
        except ImportError:
            logger.error("LangChain components are not installed or cannot be imported.")
            raise ImportError("Please install 'langchain-openai' or 'langchain-community' to use LangChain wrappers.")

    def get_llamaindex_llm(self, model: str = "gpt-4o-mini", temperature: float = 0.7, **kwargs):
        """
        Get a LlamaIndex LLM instance configured with this integration's API key.

        Returns:
            An instance of OpenAI from llama_index.llms.openai.
        """
        if not self.is_configured():
            logger.warning("LlamaIndex Mock LLM returned due to missing credentials.")
            from llama_index.core.llms import MockLLM
            return MockLLM(max_tokens=100)

        try:
            from llama_index.llms.openai import OpenAI as LlamaOpenAI
            return LlamaOpenAI(
                api_key=self.api_key,
                model=model,
                temperature=temperature,
                **kwargs
            )
        except ImportError:
            logger.error("LlamaIndex components are not installed or cannot be imported.")
            raise ImportError("Please install 'llama-index-llms-openai' to use LlamaIndex wrappers.")
