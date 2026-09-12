"""
Unit tests for Hugging Face Integration Wrapper.
"""

import unittest
from unittest.mock import MagicMock, patch
from src.integrations.huggingface_integration import HuggingFaceIntegration


class TestHuggingFaceIntegration(unittest.TestCase):
    """Test cases for HuggingFaceIntegration."""

    def test_init_without_token(self):
        """Test HF initialization when token is not provided."""
        with patch.dict("os.environ", {}, clear=True):
            wrapper = HuggingFaceIntegration(access_token=None)
            self.assertFalse(wrapper.is_configured())
            self.assertFalse(wrapper.authenticated)

    def test_init_with_token(self):
        """Test HF initialization when token is provided."""
        with patch("huggingface_hub.login") as mock_login:
            wrapper = HuggingFaceIntegration(access_token="fake-hf-token")
            self.assertTrue(wrapper.is_configured())
            self.assertTrue(wrapper.authenticated)
            mock_login.assert_called_once_with(token="fake-hf-token")

    def test_load_model_mock_mode(self):
        """Test loading model when operating in mock mode."""
        wrapper = HuggingFaceIntegration(access_token=None)
        model = wrapper.load_model("gpt2")
        self.assertEqual(model["model_id"], "gpt2")
        self.assertEqual(model["status"], "mock_loaded")

    @patch("huggingface_hub.model_info")
    def test_load_model_configured(self, mock_model_info):
        """Test loading model when token is configured."""
        mock_info = MagicMock()
        mock_info.author = "openai-community"
        mock_info.downloads = 1000
        mock_info.likes = 50
        mock_info.tags = ["text-generation"]
        mock_model_info.return_value = mock_info

        wrapper = HuggingFaceIntegration(access_token="fake-token")
        model = wrapper.load_model("gpt2")

        self.assertEqual(model["model_id"], "gpt2")
        self.assertEqual(model["status"], "active")
        self.assertEqual(model["info"]["author"], "openai-community")
        mock_model_info.assert_called_once_with("gpt2", token="fake-token")

    def test_load_dataset_mock_mode(self):
        """Test loading dataset when operating in mock mode."""
        wrapper = HuggingFaceIntegration(access_token=None)
        dataset = wrapper.load_dataset("imdb")
        self.assertEqual(dataset["dataset_id"], "imdb")
        self.assertEqual(dataset["status"], "mock_loaded")

    @patch("huggingface_hub.dataset_info")
    def test_load_dataset_configured(self, mock_dataset_info):
        """Test loading dataset when token is configured."""
        mock_info = MagicMock()
        mock_info.author = "stanford"
        mock_info.downloads = 500
        mock_info.likes = 30
        mock_info.tags = ["sentiment"]
        mock_dataset_info.return_value = mock_info

        wrapper = HuggingFaceIntegration(access_token="fake-token")
        dataset = wrapper.load_dataset("imdb")

        self.assertEqual(dataset["dataset_id"], "imdb")
        self.assertEqual(dataset["status"], "active")
        self.assertEqual(dataset["info"]["author"], "stanford")
        mock_dataset_info.assert_called_once_with("imdb", token="fake-token")


if __name__ == "__main__":
    unittest.main()
