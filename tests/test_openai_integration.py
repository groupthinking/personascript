"""
Unit tests for OpenAI API Integration Wrapper.
"""

import unittest
from unittest.mock import MagicMock, patch
from src.integrations.openai_integration import OpenAIIntegration


class TestOpenAIIntegration(unittest.TestCase):
    """Test cases for OpenAIIntegration."""

    def test_init_without_key(self):
        """Test wrapper initialization when key is not provided."""
        with patch.dict("os.environ", {}, clear=True):
            wrapper = OpenAIIntegration(api_key=None)
            self.assertFalse(wrapper.is_configured())
            self.assertIsNone(wrapper.client)

    def test_init_with_key(self):
        """Test wrapper initialization when key is provided."""
        wrapper = OpenAIIntegration(api_key="test-openai-key")
        self.assertTrue(wrapper.is_configured())
        self.assertIsNotNone(wrapper.client)

    def test_generate_text_mock_mode(self):
        """Test text generation when no API key is set."""
        with patch.dict("os.environ", {}, clear=True):
            wrapper = OpenAIIntegration(api_key=None)
            response = wrapper.generate_text("Hi", model="gpt-4o-mini")
            self.assertIn("Mock OpenAI response", response)
            self.assertIn("Hi", response)

    @patch("openai.resources.chat.Completions.create")
    def test_generate_text_configured(self, mock_create):
        """Test text generation when API key is configured."""
        # Setup mock return value
        mock_choice = MagicMock()
        mock_choice.message.content = "Real OpenAI response"
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_create.return_value = mock_response

        wrapper = OpenAIIntegration(api_key="fake-key")
        response = wrapper.generate_text("Hello World")

        self.assertEqual(response, "Real OpenAI response")
        mock_create.assert_called_once()

    def test_get_langchain_llm(self):
        """Test retrieving LangChain LLM wrapper."""
        wrapper = OpenAIIntegration(api_key=None)
        llm = wrapper.get_langchain_llm()
        self.assertIsNotNone(llm)

    def test_get_llamaindex_llm(self):
        """Test retrieving LlamaIndex LLM wrapper."""
        wrapper = OpenAIIntegration(api_key=None)
        llm = wrapper.get_llamaindex_llm()
        self.assertIsNotNone(llm)


if __name__ == "__main__":
    unittest.main()
