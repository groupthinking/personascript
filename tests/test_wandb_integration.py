"""
Unit tests for Weights & Biases Integration Wrapper.
"""

import unittest
from unittest.mock import MagicMock, patch
from src.integrations.wandb_integration import WandbIntegration


class TestWandbIntegration(unittest.TestCase):
    """Test cases for WandbIntegration."""

    def test_init_without_key(self):
        """Test W&B initialization when API key is not provided."""
        with patch.dict("os.environ", {}, clear=True):
            wrapper = WandbIntegration(api_key=None)
            self.assertFalse(wrapper.is_configured())
            self.assertFalse(wrapper.authenticated)

    def test_init_with_key(self):
        """Test W&B initialization when API key is provided."""
        with patch("wandb.login") as mock_login:
            wrapper = WandbIntegration(api_key="fake-wandb-key")
            self.assertTrue(wrapper.is_configured())
            self.assertTrue(wrapper.authenticated)
            mock_login.assert_called_once_with(key="fake-wandb-key")

    def test_run_lifecycle_mock_mode(self):
        """Test full W&B run lifecycle in mock mode (no key)."""
        with patch.dict("os.environ", {}, clear=True):
            wrapper = WandbIntegration(api_key=None)

            # Test init run
            run = wrapper.init_run(project="test-project", config={"lr": 0.01})
            self.assertEqual(run["project"], "test-project")
            self.assertEqual(run["run_id"], "mock_run_12345")

            # Test log metrics
            success_log = wrapper.log_metrics({"loss": 0.5}, step=1)
            self.assertTrue(success_log)

            # Test finish run
            success_finish = wrapper.finish_run()
            self.assertTrue(success_finish)
            self.assertIsNone(wrapper.run)

    @patch("wandb.init")
    def test_init_run_configured(self, mock_init):
        """Test W&B run initialization when configured."""
        mock_run = MagicMock()
        mock_run.name = "vocal-durian-3"
        mock_init.return_value = mock_run

        wrapper = WandbIntegration(api_key="fake-key")
        run = wrapper.init_run(project="my-project", config={"batch_size": 32})

        self.assertEqual(run.name, "vocal-durian-3")
        mock_init.assert_called_once_with(
            project="my-project",
            entity=None,
            config={"batch_size": 32},
            reinit=True
        )

    @patch("wandb.log")
    def test_log_metrics_configured(self, mock_log):
        """Test W&B logging when configured."""
        wrapper = WandbIntegration(api_key="fake-key")
        wrapper.run = MagicMock() # Simulate active run

        success = wrapper.log_metrics({"accuracy": 0.95}, step=10)
        self.assertTrue(success)
        wrapper.run.log.assert_called_once_with({"accuracy": 0.95}, step=10)

    @patch("wandb.finish")
    def test_finish_run_configured(self, mock_finish):
        """Test finishing run when configured."""
        wrapper = WandbIntegration(api_key="fake-key")
        mock_run = MagicMock()
        wrapper.run = mock_run

        success = wrapper.finish_run()
        self.assertTrue(success)
        mock_run.finish.assert_called_once()
        self.assertIsNone(wrapper.run)


if __name__ == "__main__":
    unittest.main()
