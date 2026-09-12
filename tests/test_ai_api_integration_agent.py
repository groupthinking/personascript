"""
Unit tests for AIApiIntegrationAgent.
"""

import os
import unittest
from unittest.mock import MagicMock, patch
from src.agents.ai_api_integration_agent import AIApiIntegrationAgent, AIAgentInputs, AIAgentOutputs


class TestAIApiIntegrationAgent(unittest.TestCase):
    """Test cases for AIApiIntegrationAgent."""

    def test_agent_initialization(self):
        """Test agent initialization."""
        agent = AIApiIntegrationAgent()
        self.assertIsNotNone(agent)

    @patch("src.integrations.github_integration.GitHubIntegration.create_issue")
    def test_agent_execution_mock_mode(self, mock_create_issue):
        """Test complete workflow execution in mock/fallback mode."""
        # Setup mock issue creation response
        mock_create_issue.return_value = "https://github.com/groupthinking/personascript/issues/42"

        with patch.dict("os.environ", {}, clear=True):
            agent = AIApiIntegrationAgent()

            inputs = AIAgentInputs(
                openai_api_key=None,
                anthropic_api_key=None,
                huggingface_token=None,
                wandb_api_key=None,
                python_env_instructions="Test env instructions"
            )

            outputs = agent.execute(inputs)

            # Verify outputs
            self.assertEqual(outputs.status, "success")
            self.assertFalse(outputs.openai_configured)
            self.assertFalse(outputs.anthropic_configured)
            self.assertFalse(outputs.huggingface_configured)
            self.assertFalse(outputs.wandb_configured)
            self.assertEqual(outputs.fine_tuning_script_path, "src/utils/fine_tune_placeholder.py")
            self.assertEqual(outputs.github_issue_url, "https://github.com/groupthinking/personascript/issues/42")

            # Assert GitHub integration was called
            mock_create_issue.assert_called_once()
            args, kwargs = mock_create_issue.call_args
            self.assertIn("AI API Integration and Fine-Tuning Framework Setup - Completed", kwargs.get("title", ""))
            self.assertIn("Test env instructions", kwargs.get("body", ""))

    @patch("src.integrations.github_integration.GitHubIntegration.create_issue")
    def test_agent_execution_with_configured_keys(self, mock_create_issue):
        """Test workflow execution when API keys are provided."""
        mock_create_issue.return_value = "https://github.com/groupthinking/personascript/issues/43"

        agent = AIApiIntegrationAgent()

        inputs = AIAgentInputs(
            openai_api_key="sk-fakeopenai",
            anthropic_api_key="sk-ant-fakeanthropic",
            huggingface_token="hf_faketoken",
            wandb_api_key="fake_wandb_api_key",
            python_env_instructions="Custom python instructions"
        )

        # Patch hf login and wandb login to prevent actual network calls during test
        with patch("huggingface_hub.login"), patch("wandb.login"):
            outputs = agent.execute(inputs)

            self.assertEqual(outputs.status, "success")
            self.assertTrue(outputs.openai_configured)
            self.assertTrue(outputs.anthropic_configured)
            self.assertTrue(outputs.huggingface_configured)
            self.assertTrue(outputs.wandb_configured)
            self.assertEqual(outputs.github_issue_url, "https://github.com/groupthinking/personascript/issues/43")


if __name__ == "__main__":
    unittest.main()
