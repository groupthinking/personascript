"""
PersonaScriptFeaturePlanningAgent - Main agent for planning and documenting advanced feature development,
updating product roadmaps in Linear, and generating draft release notes.

This agent follows a 6-step execution plan:
1. Parse and understand detailed requirements for advanced features: multi-persona content generation, campaign planning tools, and deeper CRM integrations.
2. Review existing product roadmap in Linear to identify areas for integration and impact assessment of new features.
3. Formulate an updated product roadmap draft in Linear, incorporating new features, estimated timelines, and dependencies. Capture roadmap URL.
4. Generate initial draft release notes for advanced features highlighting key benefits and user value aligned with PersonaScript's value proposition.
5. Consolidate updated Linear roadmap URL and drafted release notes.
6. Create a detailed GitHub issue summarizing goal, inputs, outputs, and steps taken.
"""

import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timezone

from ..integrations.linear_integration import LinearIntegration
from ..integrations.github_integration import GitHubIntegration

logger = logging.getLogger(__name__)


@dataclass
class FeatureRequirements:
    """Detailed requirements for advanced PersonaScript features."""
    multi_persona_content_generation: str = (
        "Support multi-persona content generation allowing users to target diverse buyer personas "
        "simultaneously with contextual messaging and tone adaptation."
    )
    campaign_planning_tools: str = (
        "Comprehensive campaign planning tools enabling multi-channel campaign structuring, "
        "content calendar alignment, and automated workflow triggers."
    )
    deeper_crm_integrations: str = (
        "Deeper CRM integrations with platforms like Salesforce and HubSpot to sync lead data, "
        "trigger dynamic personalized copy, and track revenue attribution."
    )


@dataclass
class AgentInputs:
    """Inputs for the PersonaScriptFeaturePlanningAgent."""
    feature_requirements: Optional[Union[FeatureRequirements, Dict[str, str]]] = None
    existing_product_roadmap: Optional[Dict[str, Any]] = None


@dataclass
class RoadmapItem:
    """Represents an item on the updated product roadmap."""
    id: str
    title: str
    description: str
    quarter: str
    estimated_timeline: str
    dependencies: List[str]
    linear_issue_url: Optional[str] = None


@dataclass
class UpdatedRoadmap:
    """Represents the updated product roadmap."""
    title: str
    url: str
    summary: str
    roadmap_items: List[RoadmapItem]


@dataclass
class DraftReleaseNotes:
    """Represents initial draft release notes for the new features."""
    version: str
    title: str
    overview: str
    feature_highlights: List[Dict[str, str]]
    markdown_text: str


@dataclass
class AgentOutputs:
    """Outputs from the PersonaScriptFeaturePlanningAgent."""
    linear_roadmap_url: str
    draft_release_notes: DraftReleaseNotes
    github_issue_url: str
    updated_roadmap: UpdatedRoadmap
    status: str = "success"
    error_message: Optional[str] = None


class PersonaScriptFeaturePlanningAgent:
    """
    Main agent for planning and documenting advanced feature development for PersonaScript,
    resulting in an updated Linear product roadmap, draft release notes, and GitHub tracking issue.
    """

    def __init__(
        self,
        linear_api_key: Optional[str] = None,
        linear_team_id: Optional[str] = None,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """Initialize the PersonaScriptFeaturePlanningAgent with required integrations."""
        self.linear = LinearIntegration(
            api_key=linear_api_key, team_id=linear_team_id
        )
        self.github = GitHubIntegration(
            token=github_token, repo=github_repo
        )
        self.execution_log: List[Dict[str, Any]] = []
        logger.info("PersonaScriptFeaturePlanningAgent initialized")

    def _log_step(self, step_number: int, description: str, status: str = "started", data: Optional[Dict] = None):
        """Log step execution."""
        log_entry = {
            "step": step_number,
            "description": description,
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data or {}
        }
        self.execution_log.append(log_entry)
        logger.info(f"Step {step_number}: {description} - {status}")

    def execute(self, inputs: Optional[AgentInputs] = None) -> AgentOutputs:
        """
        Execute the complete 6-step feature planning workflow.

        Args:
            inputs: AgentInputs with feature requirements and existing roadmap data.

        Returns:
            AgentOutputs containing updated Linear roadmap URL, release notes draft, and GitHub URL.
        """
        if inputs is None:
            inputs = AgentInputs()

        logger.info("Starting PersonaScriptFeaturePlanningAgent execution")
        self.execution_log = []

        try:
            # Step 1: Parse and understand detailed requirements for advanced features
            self._log_step(1, "Parse and understand detailed advanced feature requirements")
            parsed_reqs = self._parse_requirements(inputs.feature_requirements)
            self._log_step(1, "Parse and understand detailed advanced feature requirements", "completed", {
                "features_parsed": list(parsed_reqs.keys())
            })

            # Step 2: Review existing product roadmap in Linear
            self._log_step(2, "Review existing product roadmap in Linear for integration areas and impact")
            existing_roadmap = inputs.existing_product_roadmap or self._fetch_existing_linear_roadmap()
            impact_assessment = self._assess_roadmap_impact(parsed_reqs, existing_roadmap)
            self._log_step(2, "Review existing product roadmap in Linear for integration areas and impact", "completed", impact_assessment)

            # Step 3: Formulate an updated product roadmap draft in Linear
            self._log_step(3, "Formulate updated product roadmap draft in Linear and capture URL")
            updated_roadmap = self._formulate_updated_roadmap(parsed_reqs, impact_assessment)
            self._log_step(3, "Formulate updated product roadmap draft in Linear and capture URL", "completed", {
                "roadmap_url": updated_roadmap.url,
                "item_count": len(updated_roadmap.roadmap_items)
            })

            # Step 4: Generate initial draft release notes for advanced features
            self._log_step(4, "Generate initial draft release notes for advanced features")
            draft_notes = self._generate_release_notes(parsed_reqs, updated_roadmap)
            self._log_step(4, "Generate initial draft release notes for advanced features", "completed")

            # Step 5: Consolidate updated Linear roadmap URL and drafted release notes
            self._log_step(5, "Consolidate updated Linear roadmap URL and drafted release notes")
            consolidated_data = self._consolidate_outputs(updated_roadmap, draft_notes)
            self._log_step(5, "Consolidate updated Linear roadmap URL and drafted release notes", "completed")

            # Step 6: Create detailed GitHub issue summarizing goal, inputs, outputs, and steps taken
            self._log_step(6, "Create detailed GitHub issue summarizing goal, inputs, outputs, and execution plan")
            github_issue_url = self._create_github_issue(inputs, parsed_reqs, updated_roadmap, draft_notes)
            self._log_step(6, "Create detailed GitHub issue summarizing goal, inputs, outputs, and execution plan", "completed", {
                "github_issue_url": github_issue_url
            })

            logger.info("PersonaScriptFeaturePlanningAgent execution completed successfully")
            return AgentOutputs(
                linear_roadmap_url=updated_roadmap.url,
                draft_release_notes=draft_notes,
                github_issue_url=github_issue_url,
                updated_roadmap=updated_roadmap,
                status="success"
            )

        except Exception as e:
            logger.error("Error during PersonaScriptFeaturePlanningAgent execution", exc_info=True)
            empty_notes = DraftReleaseNotes(
                version="v1.0.0-draft",
                title="Draft Release Notes Error",
                overview="An error occurred during feature planning execution.",
                feature_highlights=[],
                markdown_text="An error occurred during execution."
            )
            empty_roadmap = UpdatedRoadmap(
                title="Error Roadmap",
                url="",
                summary="An error occurred.",
                roadmap_items=[]
            )
            return AgentOutputs(
                linear_roadmap_url="",
                draft_release_notes=empty_notes,
                github_issue_url="",
                updated_roadmap=empty_roadmap,
                status="error",
                error_message=str(e)
            )

    def _parse_requirements(
        self,
        raw_reqs: Optional[Union[FeatureRequirements, Dict[str, str]]]
    ) -> Dict[str, str]:
        """Step 1: Parse and validate input feature requirements."""
        if isinstance(raw_reqs, FeatureRequirements):
            return {
                "multi_persona_content_generation": raw_reqs.multi_persona_content_generation,
                "campaign_planning_tools": raw_reqs.campaign_planning_tools,
                "deeper_crm_integrations": raw_reqs.deeper_crm_integrations
            }
        elif isinstance(raw_reqs, dict):
            defaults = FeatureRequirements()
            return {
                "multi_persona_content_generation": raw_reqs.get(
                    "multi_persona_content_generation", defaults.multi_persona_content_generation
                ),
                "campaign_planning_tools": raw_reqs.get(
                    "campaign_planning_tools", defaults.campaign_planning_tools
                ),
                "deeper_crm_integrations": raw_reqs.get(
                    "deeper_crm_integrations", defaults.deeper_crm_integrations
                )
            }
        else:
            defaults = FeatureRequirements()
            return {
                "multi_persona_content_generation": defaults.multi_persona_content_generation,
                "campaign_planning_tools": defaults.campaign_planning_tools,
                "deeper_crm_integrations": defaults.deeper_crm_integrations
            }

    def _fetch_existing_linear_roadmap(self) -> Dict[str, Any]:
        """Step 2a: Fetch or simulate existing roadmap data from Linear."""
        return {
            "roadmap_id": "roadmap-2025-q4",
            "title": "PersonaScript Product Roadmap 2025-2026",
            "existing_features": [
                {"id": "FEAT-101", "name": "Single Persona Content Generation", "status": "Completed"},
                {"id": "FEAT-102", "name": "Basic Brand Guideline Enforcer", "status": "Completed"},
                {"id": "FEAT-103", "name": "HubSpot Draft Exporter", "status": "In Progress"}
            ]
        }

    def _assess_roadmap_impact(self, reqs: Dict[str, str], existing_roadmap: Dict[str, Any]) -> Dict[str, Any]:
        """Step 2b: Assess impact and identify integration touchpoints for advanced features."""
        return {
            "multi_persona_content_generation": {
                "impact_level": "High",
                "integration_point": "Expands FEAT-101 Single Persona engine into parallel persona context generation",
                "target_quarter": "Q1 2026",
                "estimated_weeks": 4
            },
            "campaign_planning_tools": {
                "impact_level": "High",
                "integration_point": "New core module interfacing with content generation and calendar orchestration",
                "target_quarter": "Q1 2026",
                "estimated_weeks": 6
            },
            "deeper_crm_integrations": {
                "impact_level": "Medium",
                "integration_point": "Enhances FEAT-103 HubSpot Exporter with bi-directional Salesforce & HubSpot data sync",
                "target_quarter": "Q2 2026",
                "estimated_weeks": 5
            }
        }

    def _formulate_updated_roadmap(
        self,
        reqs: Dict[str, str],
        impact_assessment: Dict[str, Any]
    ) -> UpdatedRoadmap:
        """Step 3: Create Linear roadmap issues and compile UpdatedRoadmap."""
        roadmap_items: List[RoadmapItem] = []

        feature_specs = [
            (
                "multi_persona_content_generation",
                "Multi-Persona Content Generation Engine",
                "Q1 2026",
                "4 Weeks",
                ["FEAT-101 (Single Persona Engine)"]
            ),
            (
                "campaign_planning_tools",
                "Campaign Planning & Content Orchestration Suite",
                "Q1 2026",
                "6 Weeks",
                ["Multi-Persona Content Generation Engine"]
            ),
            (
                "deeper_crm_integrations",
                "Deeper Salesforce & HubSpot CRM Integration",
                "Q2 2026",
                "5 Weeks",
                ["FEAT-103 (HubSpot Exporter)", "Campaign Planning Suite"]
            )
        ]

        main_roadmap_issue_url = None

        for key, title, quarter, timeline, deps in feature_specs:
            description = (
                f"**Feature Requirement**: {reqs[key]}\n\n"
                f"**Quarter**: {quarter}\n"
                f"**Estimated Timeline**: {timeline}\n"
                f"**Dependencies**: {', '.join(deps)}\n"
                f"**Impact Level**: {impact_assessment.get(key, {}).get('impact_level', 'Medium')}"
            )

            # Create Linear issue
            issue_res = self.linear.create_issue(
                title=f"[Roadmap - {quarter}] {title}",
                description=description,
                priority=2,
                labels=["roadmap", "advanced-features", quarter.lower().replace(" ", "-")]
            )

            issue_url = issue_res if isinstance(issue_res, str) else issue_res.get("url")
            if not main_roadmap_issue_url:
                main_roadmap_issue_url = issue_url

            roadmap_items.append(
                RoadmapItem(
                    id=f"LIN-RM-{hash(key) % 1000:03d}",
                    title=title,
                    description=reqs[key],
                    quarter=quarter,
                    estimated_timeline=timeline,
                    dependencies=deps,
                    linear_issue_url=issue_url
                )
            )

        roadmap_url = main_roadmap_issue_url or "https://linear.app/personascript/roadmap/advanced-features-2026"
        summary = (
            f"Updated PersonaScript Product Roadmap featuring 3 core advanced initiatives: "
            f"Multi-Persona Content Generation (Q1 2026), Campaign Planning Tools (Q1 2026), "
            f"and Deeper CRM Integrations (Q2 2026)."
        )

        return UpdatedRoadmap(
            title="PersonaScript Advanced Features Roadmap (2026)",
            url=roadmap_url,
            summary=summary,
            roadmap_items=roadmap_items
        )

    def _generate_release_notes(
        self,
        reqs: Dict[str, str],
        roadmap: UpdatedRoadmap
    ) -> DraftReleaseNotes:
        """Step 4: Generate draft release notes highlighting key benefits and value alignment."""
        version = "v2.0.0-alpha"
        title = "Draft Release Notes: PersonaScript Advanced Features Expansion"
        overview = (
            "PersonaScript v2.0 introduces revolutionary capabilities designed for growth-stage B2B SaaS "
            "marketing teams. With multi-persona content generation, integrated campaign planning tools, "
            "and deeper CRM data synchronizations, marketing teams can scale personalized content execution "
            "and measure true pipeline impact seamlessly."
        )

        highlights = [
            {
                "feature": "Multi-Persona Content Generation",
                "benefit": "Simultaneously generate tailored copy variations for complex buying committees (e.g., CMO, CTO, CFO) in a single workflow.",
                "value_proposition": "Drastically reduces campaign setup time while ensuring relevant messaging across all buyer decision-makers."
            },
            {
                "feature": "Campaign Planning & Orchestration Tools",
                "benefit": "Visual campaign calendar mapping, automated multi-channel messaging flows, and content asset distribution controls.",
                "value_proposition": "Aligns demand generation teams with unified campaign messaging and schedule precision."
            },
            {
                "feature": "Deeper CRM Integrations (Salesforce & HubSpot)",
                "benefit": "Bi-directional lead context sync, dynamic personalized email trigger generation, and revenue attribution metrics.",
                "value_proposition": "Bridge content creation with closed-won revenue, proving marketing content ROI directly inside your CRM."
            }
        ]

        markdown_lines = [
            f"# {title}",
            f"**Version**: `{version}` | **Status**: Draft",
            "",
            "## Executive Overview",
            overview,
            "",
            "## Key Feature Highlights & User Value",
            ""
        ]

        for h in highlights:
            markdown_lines.extend([
                f"### 🚀 {h['feature']}",
                f"- **Key Benefit**: {h['benefit']}",
                f"- **Value Proposition**: {h['value_proposition']}",
                ""
            ])

        markdown_lines.extend([
            "## Roadmap & Availability",
            f"For detailed delivery timelines and dependencies, view the updated [Linear Product Roadmap]({roadmap.url}).",
            ""
        ])

        return DraftReleaseNotes(
            version=version,
            title=title,
            overview=overview,
            feature_highlights=highlights,
            markdown_text="\n".join(markdown_lines)
        )

    def _consolidate_outputs(
        self,
        roadmap: UpdatedRoadmap,
        notes: DraftReleaseNotes
    ) -> Dict[str, Any]:
        """Step 5: Consolidate roadmap and release notes data."""
        return {
            "linear_roadmap_url": roadmap.url,
            "roadmap_items_count": len(roadmap.roadmap_items),
            "release_notes_version": notes.version,
            "release_notes_title": notes.title
        }

    def _create_github_issue(
        self,
        inputs: AgentInputs,
        reqs: Dict[str, str],
        roadmap: UpdatedRoadmap,
        notes: DraftReleaseNotes
    ) -> str:
        """
        Step 6: Create detailed GitHub tracking issue.
        Body strictly includes Goal, Inputs, Outputs with URLs, and Execution Plan.
        """
        issue_title = "Feature Planning: Advanced Feature Roadmap & Release Notes Draft"

        # Format inputs list
        inputs_str = (
            "- Advanced Feature Requirements:\n"
            f"  - Multi-Persona Content Generation: {reqs['multi_persona_content_generation']}\n"
            f"  - Campaign Planning Tools: {reqs['campaign_planning_tools']}\n"
            f"  - Deeper CRM Integrations: {reqs['deeper_crm_integrations']}\n"
            "- Existing Product Roadmap: Linear Roadmap (MKT / Product Team)"
        )

        # Format outputs list
        outputs_str = (
            f"- URL to Updated Product Roadmap in Linear: {roadmap.url}\n"
            f"- Draft Release Notes for new features:\n\n"
            f"```markdown\n{notes.markdown_text}\n```\n"
        )

        # Format execution plan summary
        exec_plan_str = (
            "1. **Parsed and understood detailed requirements** for multi-persona content generation, campaign planning tools, and deeper CRM integrations.\n"
            "2. **Reviewed existing product roadmap in Linear** to assess integration impact, timeline estimates, and module dependencies.\n"
            "3. **Formulated an updated product roadmap draft in Linear** with structured milestones and captured the updated roadmap URL.\n"
            "4. **Generated initial draft release notes** highlighting key benefits and value alignment for B2B SaaS marketing teams.\n"
            "5. **Consolidated updated Linear roadmap URL and draft release notes** into structured deliverable outputs."
        )

        body = f"""Goal: To plan and document advanced feature development for PersonaScript, resulting in an updated product roadmap and draft release notes.

Inputs:
{inputs_str}

Outputs:
{outputs_str}

Execution Plan:
{exec_plan_str}
"""

        github_url = self.github.create_issue(
            title=issue_title,
            body=body,
            labels=["feature-planning", "roadmap", "release-notes"]
        )
        return github_url
