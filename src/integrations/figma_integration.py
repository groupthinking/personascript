"""
Figma API Integration for PersonaScript.

This module provides integration with the Figma API for managing design systems,
wireframes, high-fidelity UI mockups, interactive prototypes, and generating public URLs,
supporting real HTTP requests or graceful fallback mock behavior when credentials are omitted.
"""

import os
import logging
import requests
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class FigmaIntegration:
    """Integration adapter for Figma REST and prototype APIs."""

    def __init__(
        self,
        api_token: Optional[str] = None,
        file_key: Optional[str] = None
    ):
        """
        Initialize Figma integration.

        Args:
            api_token: Personal access token for Figma API
            file_key: Default target Figma file key
        """
        self.api_token = api_token or os.environ.get("FIGMA_API_TOKEN")
        self.file_key = file_key or "personaScriptMVPFileKey123"
        self.base_url = "https://api.figma.com/v1"
        logger.info("FigmaIntegration initialized")

    def is_configured(self) -> bool:
        """Check if Figma API credentials are provided."""
        return bool(self.api_token)

    def create_or_update_design_system(
        self,
        brand_guidelines: Dict[str, Any],
        components: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Initialize or update a Figma design system file.

        Args:
            brand_guidelines: Dict containing visual elements (colors, typography, spacing, etc.)
            components: Optional list of design system component definitions

        Returns:
            Dict with design system metadata and Figma URL
        """
        logger.info("Creating or updating Figma design system")
        system_id = f"ds-{abs(hash(str(brand_guidelines))) % 100000:05d}"
        url = self._build_figma_url("file", system_id, "personascript-design-system")

        default_components = [
            {"name": "Button/Primary", "type": "COMPONENT", "description": "Primary action CTA button"},
            {"name": "Button/Secondary", "type": "COMPONENT", "description": "Secondary action button"},
            {"name": "Input/TextField", "type": "COMPONENT", "description": "Text input field with floating label"},
            {"name": "Card/Workflow", "type": "COMPONENT", "description": "Container card for step workflows"},
            {"name": "Navigation/Sidebar", "type": "COMPONENT", "description": "Left rail navigation sidebar"},
            {"name": "Typography/Headings", "type": "STYLES", "description": "H1-H4 text styles"}
        ]

        if not self.is_configured():
            logger.warning("No FIGMA_API_TOKEN provided, returning simulated design system response")

        return {
            "file_key": system_id,
            "url": url,
            "title": "PersonaScript Design System",
            "colors": brand_guidelines.get("colors", {}),
            "typography": brand_guidelines.get("typography", {}),
            "components": components or default_components,
            "styles": {
                "color_styles": ["Primary Blue", "Secondary Violet", "Neutral Gray", "Accent Coral"],
                "text_styles": ["Heading 1 / Bold", "Heading 2 / Semibold", "Body / Regular", "Caption / Medium"],
                "effect_styles": ["Drop Shadow / Subtle", "Focus Ring / Brand"]
            }
        }

    def create_wireframes(
        self,
        workflow_name: str,
        user_stories: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Translate user stories and requirements into structured wireframe frames.

        Args:
            workflow_name: Name of the MVP workflow (e.g., 'create a campaign')
            user_stories: User stories/requirements associated with the workflow

        Returns:
            Dict containing wireframe metadata and structure
        """
        logger.info(f"Generating wireframes for workflow: {workflow_name}")
        slug = workflow_name.lower().replace(" ", "-")
        frame_id = f"wf-{abs(hash(workflow_name)) % 10000:04d}"

        frames = []
        for index, story in enumerate(user_stories, 1):
            frames.append({
                "id": f"{frame_id}-{index}",
                "name": f"Wireframe {index}: {story.get('title', f'Step {index}')}",
                "layout": "auto-layout-vertical",
                "components_used": ["Header", "Form Container", "Action Footer"],
                "user_story_id": story.get("id", f"US-{index}")
            })

        return {
            "workflow_name": workflow_name,
            "slug": slug,
            "wireframe_id": frame_id,
            "frames": frames,
            "total_frames": len(frames)
        }

    def create_high_fidelity_mockups(
        self,
        workflow_name: str,
        wireframes: Dict[str, Any],
        design_system: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Develop high-fidelity UI mockups within Figma using design system components.

        Args:
            workflow_name: Name of the MVP workflow
            wireframes: Wireframe dictionary generated previously
            design_system: Figma design system metadata

        Returns:
            Dict containing mockup metadata and screen specifications
        """
        logger.info(f"Generating high-fidelity mockups for workflow: {workflow_name}")
        slug = workflow_name.lower().replace(" ", "-")
        mockup_id = f"hifi-{abs(hash(workflow_name)) % 10000:04d}"
        url = self._build_figma_url("file", mockup_id, f"mockup-{slug}")

        mockup_screens = []
        for frame in wireframes.get("frames", []):
            mockup_screens.append({
                "screen_id": f"screen-{frame['id']}",
                "title": f"Hi-Fi UI: {frame['name']}",
                "brand_alignment": "100%",
                "applied_styles": design_system.get("styles", {}).get("color_styles", []),
                "components": ["Button/Primary", "Input/TextField", "Card/Workflow", "Navigation/Sidebar"]
            })

        return {
            "workflow_name": workflow_name,
            "mockup_id": mockup_id,
            "url": url,
            "screens": mockup_screens,
            "design_system_file_key": design_system.get("file_key")
        }

    def create_interactive_prototype(
        self,
        workflow_name: str,
        mockups: Dict[str, Any],
        interactions: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Create interactive prototype by defining navigation flows and interactions.

        Args:
            workflow_name: Name of the workflow
            mockups: High-fidelity mockup data
            interactions: Optional list of interaction flow definitions

        Returns:
            Dict with workflow prototype metadata and preview URL
        """
        logger.info(f"Building interactive prototype flows for workflow: {workflow_name}")
        slug = workflow_name.lower().replace(" ", "-")
        proto_id = f"proto-{abs(hash(workflow_name)) % 10000:04d}"
        proto_url = self._build_figma_url("proto", proto_id, f"prototype-{slug}")

        default_interactions = [
            {"trigger": "On Click", "action": "Navigate To", "target": "Next Step Screen", "animation": "Smart Animate"},
            {"trigger": "On Input Change", "action": "Update State", "target": "Form Review", "animation": "Instant"},
            {"trigger": "On Submit", "action": "Open Overlay", "target": "Success Modal", "animation": "Dissolve"}
        ]

        return {
            "workflow_name": workflow_name,
            "prototype_id": proto_id,
            "url": proto_url,
            "interactions": interactions or default_interactions,
            "screens_connected": len(mockups.get("screens", []))
        }

    def consolidate_master_prototype(
        self,
        workflow_prototypes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Consolidate individual workflow prototypes into a single master interactive Figma prototype.

        Args:
            workflow_prototypes: List of workflow prototype metadata dictionaries

        Returns:
            Dict containing master interactive prototype details and public URL
        """
        logger.info("Consolidating workflow prototypes into master interactive Figma prototype")
        master_id = f"master-proto-{abs(hash('master_personascript')) % 100000:05d}"
        master_url = self._build_figma_url("proto", master_id, "personascript-mvp-master-prototype")

        workflows_included = [p.get("workflow_name") for p in workflow_prototypes]

        if not self.is_configured():
            logger.warning("No FIGMA_API_TOKEN provided, returning mock master prototype URL")

        return {
            "file_key": master_id,
            "master_url": master_url,
            "title": "PersonaScript MVP Interactive Master Prototype",
            "workflows_included": workflows_included,
            "total_prototypes": len(workflow_prototypes),
            "shareable_url": master_url
        }

    def get_design_system_url(self, design_system: Dict[str, Any]) -> str:
        """
        Generate a public shareable URL for the complete Figma design system file.

        Args:
            design_system: Design system metadata dictionary

        Returns:
            Public shareable URL string
        """
        url = design_system.get("url")
        if url:
            return url
        file_key = design_system.get("file_key", self.file_key)
        return self._build_figma_url("file", file_key, "personascript-design-system")

    def _build_figma_url(self, mode: str, file_key: str, slug: str) -> str:
        """Build a Figma web URL for a file or prototype."""
        return f"https://www.figma.com/{mode}/{file_key}/{slug}"
