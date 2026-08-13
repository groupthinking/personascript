"""
Hugging Face Integration Wrapper for PersonaScript.

Handles authentication, environment configuration, and loading models/datasets
via Hugging Face API and libraries.
"""

import os
import logging
from typing import Any, Optional, Dict

logger = logging.getLogger(__name__)


class HuggingFaceIntegration:
    """Wrapper class for Hugging Face platform integration."""

    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize Hugging Face integration.

        Args:
            access_token: Hugging Face personal access token. If not provided,
                         will look for HF_TOKEN or HUGGINGFACE_CO_API_KEY.
        """
        self.access_token = access_token or os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_CO_API_KEY")
        self.authenticated = False

        if self.access_token:
            self.login()
        else:
            logger.warning("No Hugging Face token provided. Operating in mock mode.")

    def is_configured(self) -> bool:
        """Check if integration is configured with an access token."""
        return self.access_token is not None

    def login(self) -> bool:
        """
        Authenticate with Hugging Face using the provided access token.

        Returns:
            bool: True if authentication succeeded, False otherwise.
        """
        if not self.is_configured():
            logger.warning("No Hugging Face token available to login.")
            return False

        try:
            from huggingface_hub import login
            login(token=self.access_token)
            self.authenticated = True
            logger.info("Successfully authenticated with Hugging Face Hub.")
            return True
        except ImportError:
            logger.error("huggingface_hub is not installed.")
            return False
        except Exception as e:
            logger.error(f"Error authenticating with Hugging Face Hub: {e}")
            return False

    def get_environment_info(self) -> Dict[str, Any]:
        """
        Get the current Hugging Face configuration environment details.

        Returns:
            Dict containing configuration state.
        """
        return {
            "has_token": self.is_configured(),
            "authenticated": self.authenticated,
            "cache_dir": os.environ.get("HF_HOME") or os.path.expanduser("~/.cache/huggingface"),
            "token_masked": f"{self.access_token[:4]}...{self.access_token[-4:]}" if self.access_token else None
        }

    def load_model(self, model_id: str, **kwargs) -> Any:
        """
        Loads a pre-trained model metadata or object.
        Supports loading actual transformers model or returns mock placeholder.

        Args:
            model_id: Hugging Face model repository ID.

        Returns:
            A model object or model configuration dictionary.
        """
        logger.info(f"Loading Hugging Face model: {model_id}")
        if not self.is_configured():
            logger.info("Returning mock Hugging Face model placeholder.")
            return {
                "model_id": model_id,
                "status": "mock_loaded",
                "device": "cpu",
                "config": kwargs
            }

        try:
            # We can use AutoConfig or AutoModel from transformers if installed,
            # or use huggingface_hub to get model details
            from huggingface_hub import model_info
            info = model_info(model_id, token=self.access_token)
            logger.info(f"Successfully retrieved info for model: {model_id}")
            return {
                "model_id": model_id,
                "status": "active",
                "info": {
                    "author": info.author,
                    "downloads": info.downloads,
                    "likes": info.likes,
                    "tags": info.tags
                }
            }
        except ImportError:
            logger.warning("huggingface_hub is not imported correctly. Returning placeholder.")
            return {"model_id": model_id, "status": "partial_load"}
        except Exception as e:
            logger.error(f"Failed to load model {model_id} from Hugging Face Hub: {e}")
            # Fallback to local configuration metadata
            return {"model_id": model_id, "status": "error", "error": str(e)}

    def load_dataset(self, dataset_id: str, **kwargs) -> Any:
        """
        Loads a dataset or dataset metadata.

        Args:
            dataset_id: Hugging Face dataset ID.

        Returns:
            The loaded dataset object or metadata dict.
        """
        logger.info(f"Loading Hugging Face dataset: {dataset_id}")
        if not self.is_configured():
            logger.info("Returning mock Hugging Face dataset placeholder.")
            return {
                "dataset_id": dataset_id,
                "status": "mock_loaded",
                "num_rows": 100,
                "features": ["text", "label"],
                "config": kwargs
            }

        try:
            from huggingface_hub import dataset_info
            info = dataset_info(dataset_id, token=self.access_token)
            logger.info(f"Successfully retrieved info for dataset: {dataset_id}")
            return {
                "dataset_id": dataset_id,
                "status": "active",
                "info": {
                    "author": info.author,
                    "downloads": info.downloads,
                    "likes": info.likes,
                    "tags": info.tags
                }
            }
        except ImportError:
            logger.warning("huggingface_hub is not imported correctly. Returning placeholder.")
            return {"dataset_id": dataset_id, "status": "partial_load"}
        except Exception as e:
            logger.error(f"Failed to load dataset {dataset_id} from Hugging Face Hub: {e}")
            return {"dataset_id": dataset_id, "status": "error", "error": str(e)}
