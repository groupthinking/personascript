"""
Unit tests for Anthropic API Integration Wrapper.
"""

import unittest
from unittest.mock import MagicMock, patch
from src.integrations.anthropic_integration import AnthropicIntegration


class TestAnthropicIntegration(unittest.TestCase):
    """Test cases for AnthropicIntegration."""

    def test_init_without_key(self):
        """Test wrapper initialization when key is not provided."""
        with patch.dict("os.environ", {}, clear=True):
            wrapper = AnthropicIntegration(api_key=None)
            self.assertFalse(wrapper.is_configured())
            self.assertIsNone(wrapper.client)

    def test_init_with_key(self):
        """Test wrapper initialization when key is provided."""
        wrapper = AnthropicIntegration(api_key="test-anthropic-key")
        self.assertTrue(wrapper.is_configured())
        self.assertIsNotNone(wrapper.client)

    def test_generate_text_mock_mode(self):
        """Test text generation when no API key is set."""
        with patch.dict("os.environ", {}, clear=True):
            wrapper = AnthropicIntegration(api_key=None)
            response = wrapper.generate_text("Hi", model="claude-3-5-sonnet-latest")
            self.assertIn("Mock Anthropic response", response)
            self.assertIn("Hi", response)

    @patch("anthropic.resources.messages.Messages.create")
    def test_generate_text_configured(self, mock_create):
        """Test text generation when API key is configured."""
        # Setup mock return value
        mock_content_block = MagicMock()
        mock_content_block.text = "Real Anthropic response"
        mock_response = MagicMock()
        mock_response.content = [mock_content_block]
        mock_create.return_value = mock_response

        wrapper = AnthropicIntegration(api_key="fake-key")
        response = wrapper.generate_text("Hello World")

        self.assertEqual(response, "Real Anthropic response")
        mock_create.assert_called_once()

    def test_get_langchain_llm(self):
        """Test retrieving LangChain LLM wrapper."""
        wrapper = AnthropicIntegration(api_key=None)
        llm = wrapper.get_langchain_llm()
        self.assertIsNotNone(llm)

    def test_get_llamaindex_llm(self):
        """Test retrieving LlamaIndex LLM wrapper."""
        wrapper = AnthropicIntegration(api_key=None)
        llm = wrapper.get_llamaindex_llm()
        self.assertIsNotNone(llm)


if __name__ == "__main__":
    unittest.main()
