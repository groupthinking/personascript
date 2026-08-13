"""
PersonaScriptFeaturePlanningAgent - Main agent for planning and documenting advanced features.

This agent parses detailed product requirements, reviews and updates product roadmaps
on Linear, drafts release notes, and logs everything in a detailed GitHub issue.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from ..integrations.linear_integration import LinearIntegration
from ..integrations.github_integration import GitHubIntegration

logger = logging.getLogger(__name__)


@dataclass
class FeatureRequirement:
    """Represents a detailed product feature requirement."""

    name: str
    description: str
    key_details: List[str] = field(default_factory=list)


@dataclass
class FeaturePlanningInputs:
    """Input data for the FeaturePlanningAgent."""

    advanced_features: List[FeatureRequirement]
    existing_roadmap_id: Optional[str] = None
    linear_api_key: Optional[str] = None
    github_token: Optional[str] = None
    github_repo: Optional[str] = None


@dataclass
class FeaturePlanningOutputs:
    """Output data from the FeaturePlanningAgent."""

    roadmap_url: str
    draft_release_notes: str
    github_issue_url: str


class PersonaScriptFeaturePlanningAgent:
    """
    Main agent class for advanced feature planning and documentation.

    This agent follows a 6-step execution plan:
    1. Parse and understand detailed requirements for advanced features.
    2. Review the existing product roadmap in Linear.
    3. Formulate an updated product roadmap draft in Linear.
    4. Generate initial draft release notes for the advanced features.
    5. Consolidate roadmap URL and draft release notes.
    6. Create a detailed GitHub issue tracking the plan and deliverables.
    """

    def __init__(
        self,
        linear_api_key: Optional[str] = None,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """
        Initialize the FeaturePlanningAgent.

        Args:
            linear_api_key: API key for Linear integration
            github_token: Token for GitHub API
            github_repo: Repository name (format: "owner/repo")
        """
        self.linear_integration = LinearIntegration(api_key=linear_api_key)
        self.github_integration = GitHubIntegration(token=github_token, repo=github_repo)
        logger.info("PersonaScriptFeaturePlanningAgent initialized")

    def execute(self, inputs: FeaturePlanningInputs) -> FeaturePlanningOutputs:
        """
        Execute the complete agent feature planning workflow.

        Args:
            inputs: FeaturePlanningInputs including advanced features and options.

        Returns:
            FeaturePlanningOutputs containing roadmap URL, release notes, and GitHub issue URL.
        """
        logger.info("Starting FeaturePlanningAgent execution")

        # Step 1: Parse and understand detailed requirements
        parsed_requirements = self._parse_requirements(inputs.advanced_features)

        # Step 2: Review existing product roadmap in Linear
        existing_roadmap = self._review_existing_roadmap(inputs.existing_roadmap_id)

        # Step 3: Formulate updated product roadmap draft in Linear
        roadmap_url = self._update_linear_roadmap(existing_roadmap, parsed_requirements, inputs.existing_roadmap_id)

        # Step 4: Generate initial draft release notes
        draft_release_notes = self._generate_release_notes(parsed_requirements)

        # Step 5: Consolidate outputs
        consolidated = {
            "roadmap_url": roadmap_url,
            "draft_release_notes": draft_release_notes
        }

        # Step 6: Create detailed GitHub issue
        github_issue_url = self._create_github_issue(consolidated, inputs)

        outputs = FeaturePlanningOutputs(
            roadmap_url=roadmap_url,
            draft_release_notes=draft_release_notes,
            github_issue_url=github_issue_url
        )

        logger.info("FeaturePlanningAgent execution completed successfully")
        return outputs

    def _parse_requirements(self, features: List[FeatureRequirement]) -> List[Dict[str, Any]]:
        """
        Step 1: Parse and understand requirements for advanced features.

        Args:
            features: List of raw features requirements.

        Returns:
            List of parsed, structured feature metadata.
        """
        logger.info("Step 1: Parsing advanced feature requirements")
        parsed = []
        for feature in features:
            parsed.append({
                "name": feature.name,
                "description": feature.description,
                "key_details": feature.key_details,
                "complexity": self._estimate_complexity(feature),
                "dependencies": self._determine_dependencies(feature.name)
            })
        return parsed

    def _estimate_complexity(self, feature: FeatureRequirement) -> str:
        """Estimate feature development complexity based on details."""
        if "crm" in feature.name.lower() or "integration" in feature.name.lower():
            return "High"
        elif "campaign" in feature.name.lower():
            return "Medium-High"
        return "Medium"

    def _determine_dependencies(self, feature_name: str) -> List[str]:
        """Determine what other features/components this feature depends on."""
        name = feature_name.lower()
        if "campaign" in name:
            return ["User Persona Profiles", "Content Journey Maps"]
        if "crm" in name:
            return ["Campaign Planning Tools", "Multi-Persona Content Generation"]
        return ["User Persona Profiles"]

    def _review_existing_roadmap(self, roadmap_id: Optional[str]) -> Dict[str, Any]:
        """
        Step 2: Review existing product roadmap in Linear to assess impact.

        Args:
            roadmap_id: The ID of the roadmap in Linear.

        Returns:
            Dictionary containing the existing roadmap projects and metadata.
        """
        logger.info("Step 2: Reviewing existing roadmap from Linear")
        if not roadmap_id:
            logger.info("No existing roadmap ID provided, using base MVP roadmap")
            roadmap_id = "default-mvp-roadmap"

        return self.linear_integration.get_roadmap(roadmap_id)

    def _update_linear_roadmap(
        self,
        existing_roadmap: Dict[str, Any],
        parsed_requirements: List[Dict[str, Any]],
        roadmap_id: Optional[str]
    ) -> str:
        """
        Step 3: Formulate an updated product roadmap draft in Linear.

        Args:
            existing_roadmap: Existing roadmap metadata.
            parsed_requirements: Parsed new features to add.
            roadmap_id: The roadmap ID to update.

        Returns:
            URL to the updated product roadmap in Linear.
        """
        logger.info("Step 3: Formulating updated product roadmap draft in Linear")

        new_projects = []
        for index, req in enumerate(parsed_requirements):
            # Estimate quarterly timelines sequentially following Q2
            quarter = f"2024-Q{3 + (index // 2)}"
            new_projects.append({
                "name": req["name"],
                "description": req["description"],
                "status": "planned",
                "target_date": quarter,
                "dependencies": req["dependencies"],
                "complexity": req["complexity"]
            })

        updates = {
            "title": "PersonaScript Advanced Features Product Roadmap",
            "description": "Updated roadmap including Multi-Persona Content Generation, Campaign Planning, and CRM Integrations",
            "projects": existing_roadmap.get("projects", []) + new_projects
        }

        if roadmap_id:
            return self.linear_integration.update_roadmap(roadmap_id, updates)
        else:
            return self.linear_integration.create_roadmap(
                title=updates["title"],
                description=updates["description"],
                projects=updates["projects"]
            )

    def _generate_release_notes(self, parsed_requirements: List[Dict[str, Any]]) -> str:
        """
        Step 4: Generate initial draft release notes highlighting key benefits and user value.

        Args:
            parsed_requirements: Parsed features.

        Returns:
            Draft release notes as a Markdown string.
        """
        logger.info("Step 4: Generating draft release notes")

        notes = [
            "# PersonaScript Draft Release Notes - Advanced Features",
            "",
            "We are thrilled to introduce a suite of advanced features designed to help growth-stage B2B SaaS marketing teams supercharge their content operations, coordinate seamless campaigns, and track real-time business impact.",
            "",
            "## What's New",
            ""
        ]

        for req in parsed_requirements:
            notes.extend([
                f"### 🚀 {req['name']}",
                "",
                f"**Overview:** {req['description']}",
                "",
                "**Key Capabilities & Benefits:**"
            ])
            for detail in req["key_details"]:
                notes.append(f"- {detail}")
            notes.extend([
                "",
                f"**Dependencies:** {', '.join(req['dependencies'])}",
                f"**Target Timeline:** Q3/Q4 2024",
                ""
            ])

        notes.extend([
            "## Value Realization",
            "By tying these three pillars together—simultaneous multi-persona targeting, automated multi-stage campaign execution, and closed-loop CRM tracking—PersonaScript empowers growth marketing leaders to dramatically accelerate lead conversion while maintaining uncompromised brand alignment.",
            ""
        ])

        return "\n".join(notes)

    def _create_github_issue(
        self,
        consolidated: Dict[str, str],
        inputs: FeaturePlanningInputs
    ) -> str:
        """
        Step 6: Create detailed GitHub issue with standard required structure.

        Args:
            consolidated: Dictionary containing roadmap_url and draft_release_notes.
            inputs: Original inputs for contextual logs.

        Returns:
            URL of the newly created GitHub issue.
        """
        logger.info("Step 6: Constructing and creating GitHub issue")

        goal_text = "To plan and document advanced feature development for PersonaScript, resulting in an updated product roadmap and draft release notes."

        inputs_list = [
            "Advanced Feature Requirements (multi-persona content generation, campaign planning tools, deeper CRM integrations)",
            f"Existing Product Roadmap ID: {inputs.existing_roadmap_id or 'None provided (simulated MVP base)'}"
        ]

        outputs_list = [
            f"URL to Updated Product Roadmap in Linear: {consolidated['roadmap_url']}",
            "Draft Release Notes for new features (included in the issue body)",
            "URL to new GitHub issue tracking the plan and deliverables"
        ]

        # Summary of Steps 1-5
        execution_plan_summary = (
            "1. **Parse & Understand Requirements**: Analyzed the advanced feature definitions including Multi-Persona Content Generation, Campaign Planning Tools, and Deeper CRM Integrations, mapping key capabilities, dependencies, and development complexities.\n"
            "2. **Review Existing Roadmap**: Retrieved the baseline core roadmap from Linear (MVP tracking) to assess integration options and dependencies.\n"
            "3. **Formulate Updated Roadmap**: Constructed an updated product roadmap draft in Linear, organizing the new features with chronological targets (Q3/Q4 2024), estimating development complexity, and capturing the live roadmap URL.\n"
            "4. **Generate Release Notes**: Crafted high-value draft release notes highlighting user benefits, functionality, and aligned value propositions for growth-stage marketing teams.\n"
            "5. **Consolidate Deliverables**: Aggregated the resulting Linear roadmap URL and draft release notes for structured hand-off."
        )

        # Construct exact issue body format
        issue_body = f"""Goal: {goal_text}

Inputs:
{chr(10).join([f'- {item}' for item in inputs_list])}

Outputs:
{chr(10).join([f'- {item}' for item in outputs_list])}

Execution Plan:
{execution_plan_summary}

---

## 📄 Generated Draft Release Notes

{consolidated['draft_release_notes']}
"""

        issue_url = self.github_integration.create_issue(
            title="PersonaScript Advanced Feature Planning & Product Roadmap",
            body=issue_body,
            labels=["feature-planning", "roadmap", "release-notes"]
        )

        return issue_url
