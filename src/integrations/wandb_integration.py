"""
Weights & Biases (W&B) Integration Wrapper for PersonaScript.

Handles authentication, environment configuration, and experiment tracking/logging
via Weights & Biases API.
"""

import os
import logging
from typing import Any, Optional, Dict

logger = logging.getLogger(__name__)


class WandbIntegration:
    """Wrapper class for Weights & Biases experiment tracking."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Weights & Biases integration.

        Args:
            api_key: Weights & Biases API key. If not provided,
                     will look for WANDB_API_KEY.
        """
        self.api_key = api_key or os.environ.get("WANDB_API_KEY")
        self.authenticated = False
        self.run = None

        if self.api_key:
            self.login()
        else:
            logger.warning("No Weights & Biases API key provided. Operating in mock mode.")

    def is_configured(self) -> bool:
        """Check if integration is configured with an API key."""
        return self.api_key is not None

    def login(self) -> bool:
        """
        Authenticate with Weights & Biases using the provided API key.

        Returns:
            bool: True if authentication succeeded, False otherwise.
        """
        if not self.is_configured():
            logger.warning("No W&B API key available to login.")
            return False

        try:
            import wandb
            # Set environment variable to avoid interactive prompts
            os.environ["WANDB_API_KEY"] = self.api_key
            os.environ["WANDB_SILENT"] = "true"
            wandb.login(key=self.api_key)
            self.authenticated = True
            logger.info("Successfully authenticated with Weights & Biases.")
            return True
        except ImportError:
            logger.error("wandb library is not installed.")
            return False
        except Exception as e:
            logger.error(f"Error authenticating with Weights & Biases: {e}")
            return False

    def init_run(self, project: str, entity: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        """
        Initialize a new W&B run for experiment tracking.

        Args:
            project: Name of the W&B project.
            entity: Name of the W&B entity (team or user).
            config: Dict of hyper-parameters and config metadata to track.

        Returns:
            W&B Run object or mock placeholder.
        """
        logger.info(f"Initializing W&B Run under project: {project}")
        if not self.is_configured():
            logger.info("Returning mock W&B Run placeholder.")
            self.run = {
                "project": project,
                "entity": entity,
                "config": config or {},
                "run_id": "mock_run_12345",
                "status": "active"
            }
            return self.run

        try:
            import wandb
            self.run = wandb.init(
                project=project,
                entity=entity,
                config=config,
                reinit=True,
                **kwargs
            )
            logger.info(f"Successfully initialized active W&B run: {self.run.name}")
            return self.run
        except Exception as e:
            logger.error(f"Failed to initialize W&B run: {e}")
            self.run = {"project": project, "status": "error", "error": str(e)}
            return self.run

    def log_metrics(self, metrics: Dict[str, Any], step: Optional[int] = None) -> bool:
        """
        Log metrics to the current active W&B run.

        Args:
            metrics: Dictionary of metric name and values.
            step: Current step number.

        Returns:
            bool: True if logged successfully, False otherwise.
        """
        if not self.run:
            logger.warning("No active run found. Call init_run before logging metrics.")
            return False

        if not self.is_configured():
            logger.info(f"[Mock W&B Log Step={step}]: {metrics}")
            return True

        try:
            import wandb
            if hasattr(self.run, "log"):
                self.run.log(metrics, step=step)
            else:
                wandb.log(metrics, step=step)
            return True
        except Exception as e:
            logger.error(f"Failed to log metrics to W&B: {e}")
            return False

    def finish_run(self) -> bool:
        """
        Mark the current W&B run as completed.

        Returns:
            bool: True if run was finished successfully.
        """
        if not self.run:
            logger.info("No active W&B run to finish.")
            return False

        logger.info("Finishing active W&B run.")
        if not self.is_configured():
            self.run = None
            return True

        try:
            import wandb
            if hasattr(self.run, "finish"):
                self.run.finish()
            else:
                wandb.finish()
            self.run = None
            return True
        except Exception as e:
            logger.error(f"Error finishing W&B run: {e}")
            return False
