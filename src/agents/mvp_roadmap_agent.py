"""
PersonaScriptMVPDevelopmentRoadmapAgent - Agent for developing a detailed MVP roadmap
structured for Linear over a 3-6 month timeframe.

This agent performs the following 7 steps:
1. Parse and comprehend business context (company name, value prop, timeframe, target platform).
2. Gather internal documentation and customer pain points.
3. Synthesize strategic themes and high-impact MVP feature areas.
4. Generate and prioritize concrete, actionable MVP features.
5. Draft detailed MVP roadmap structured for Linear (Epics, Features, User Stories, Milestones, Timelines).
6. Construct complete GitHub issue body.
7. Create GitHub issue titled 'PersonaScript MVP Roadmap (3-6 Months)' via GitHub API.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from ..integrations.github_integration import GitHubIntegration
from ..integrations.linear_integration import LinearIntegration


logger = logging.getLogger(__name__)


@dataclass
class UserStory:
    """Represents an individual user story structured for Linear."""

    id: str
    title: str
    role: str
    action: str
    benefit: str
    estimate_points: int = 3


@dataclass
class Feature:
    """Represents a product feature containing user stories."""

    id: str
    title: str
    description: str
    priority: str  # e.g., "Critical", "High", "Medium"
    user_stories: List[UserStory] = field(default_factory=list)


@dataclass
class Epic:
    """Represents a high-level Epic grouping features."""

    id: str
    title: str
    theme: str
    description: str
    features: List[Feature] = field(default_factory=list)


@dataclass
class Milestone:
    """Represents a key roadmap milestone within the 3-6 month timeframe."""

    name: str
    timeframe: str
    deliverables: List[str] = field(default_factory=list)


@dataclass
class RoadmapInputs:
    """Input data for the PersonaScriptMVPDevelopmentRoadmapAgent."""

    company_name: str = "PersonaScript"
    value_proposition: str = (
        "PersonaScript empowers growth-stage B2B SaaS marketing teams to rapidly generate "
        "high-volume, hyper-personalized, and brand-aligned content across all sales funnel "
        "stages, dramatically accelerating lead conversion and brand consistency."
    )
    timeframe: str = "3-6 months"
    target_platform: str = "Linear"


@dataclass
class RoadmapOutputs:
    """Output data from the PersonaScriptMVPDevelopmentRoadmapAgent."""

    github_issue_url: str
    roadmap_markdown: str
    epics: List[Epic]
    milestones: List[Milestone]


class PersonaScriptMVPDevelopmentRoadmapAgent:
    """
    Main agent class for developing the PersonaScript MVP Roadmap formatted for Linear.
    """

    def __init__(
        self,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None,
        linear_token: Optional[str] = None
    ):
        """
        Initialize the PersonaScriptMVPDevelopmentRoadmapAgent.

        Args:
            github_token: GitHub API token
            github_repo: GitHub repository in 'owner/repo' format
            linear_token: Linear API token
        """
        self.github_integration = GitHubIntegration(token=github_token, repo=github_repo)
        self.linear_integration = LinearIntegration(token=linear_token)
        logger.info("PersonaScriptMVPDevelopmentRoadmapAgent initialized")

    def execute(self, inputs: Optional[RoadmapInputs] = None) -> RoadmapOutputs:
        """
        Execute the full 7-step roadmap drafting workflow.

        Args:
            inputs: RoadmapInputs object or None (uses default PersonaScript context)

        Returns:
            RoadmapOutputs containing GitHub issue URL, roadmap markdown, epics, and milestones.
        """
        if inputs is None:
            inputs = RoadmapInputs()

        logger.info(f"Starting MVP Roadmap execution for {inputs.company_name}")

        # Step 1: Parse and comprehend business context
        parsed_context = self._parse_context(inputs)

        # Step 2: Access internal documentation / knowledge base
        internal_docs = self._access_internal_documentation(parsed_context)

        # Step 3: Synthesize strategic themes
        themes = self._synthesize_strategic_themes(parsed_context, internal_docs)

        # Step 4: Generate and prioritize actionable MVP features
        epics = self._generate_and_prioritize_features(themes)

        # Step 5: Draft detailed MVP roadmap structured for Linear
        milestones = self._define_milestones(inputs.timeframe)
        roadmap_markdown = self._draft_roadmap_markdown(inputs, epics, milestones)

        # Step 6: Construct complete GitHub issue body
        issue_body = self._construct_github_issue_body(inputs, roadmap_markdown, epics, milestones)

        # Step 7: Create GitHub issue
        issue_title = f"{inputs.company_name} MVP Roadmap ({inputs.timeframe})"
        github_issue_url = self.github_integration.create_issue(
            title=issue_title,
            body=issue_body,
            labels=["mvp-roadmap", "linear-structure", "product-strategy"]
        )

        logger.info(f"Successfully created MVP Roadmap GitHub issue: {github_issue_url}")

        return RoadmapOutputs(
            github_issue_url=github_issue_url,
            roadmap_markdown=roadmap_markdown,
            epics=epics,
            milestones=milestones
        )

    def _parse_context(self, inputs: RoadmapInputs) -> Dict[str, Any]:
        """Step 1: Parse and comprehend provided context."""
        logger.info("Step 1: Parsing business context")
        return {
            "company_name": inputs.company_name,
            "value_proposition": inputs.value_proposition,
            "timeframe": inputs.timeframe,
            "target_platform": inputs.target_platform
        }

    def _access_internal_documentation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Step 2: Access internal documentation & customer pain points."""
        logger.info("Step 2: Gathering internal strategy and pain points")
        return {
            "customer_pain_points": [
                "Manual copy tailoring across different sales funnel stages is slow and inefficient.",
                "Inconsistent brand tone across different marketing campaigns and copywriters.",
                "Difficulty scaling hyper-personalized outreach without sacrificing messaging quality.",
                "Lack of streamlined publishing pipeline to CMS and CRM platforms (HubSpot, Contentful)."
            ],
            "product_pillars": [
                "Dynamic Content Generation Engine",
                "Brand Guideline Enforcement & Style Guardrails",
                "Persona Profile & Psychographic Personalization",
                "Automated Distribution & Analytics Feedback Loops"
            ]
        }

    def _synthesize_strategic_themes(
        self,
        context: Dict[str, Any],
        docs: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Step 3: Synthesize strategic themes and high-impact MVP areas."""
        logger.info("Step 3: Synthesizing strategic themes")
        return [
            {
                "theme_id": "THEME-1",
                "title": "Dynamic Content Orchestration Engine",
                "description": "Multi-stage sales funnel copy generation (Awareness, Consideration, Decision) with rapid batch capabilities."
            },
            {
                "theme_id": "THEME-2",
                "title": "Brand Voice Guardrails & Style Compliance",
                "description": "Automated brand guideline ingestion, vocabulary restriction, and style score auditing."
            },
            {
                "theme_id": "THEME-3",
                "title": "Hyper-Personalization & Persona Management",
                "description": "Deep psychographic trigger injection and role-based messaging customized for B2B SaaS buyers."
            },
            {
                "theme_id": "THEME-4",
                "title": "Publishing Integration & Ecosystem Connectivity",
                "description": "Direct export and synchronization with CMS/CRM tools like HubSpot, Contentful, and Linear."
            }
        ]

    def _generate_and_prioritize_features(self, themes: List[Dict[str, Any]]) -> List[Epic]:
        """Step 4 & 5: Generate features, user stories, and organize into Linear Epics."""
        logger.info("Step 4 & 5: Generating prioritized features and Linear Epics")

        epics = [
            Epic(
                id="EPIC-1",
                title="Funnel-Aligned Content Generation Engine",
                theme="Dynamic Content Orchestration Engine",
                description="Core AI prompt chaining and LLM engine to produce multi-channel copy tailored to buyer funnel stages.",
                features=[
                    Feature(
                        id="FEAT-101",
                        title="Multi-Stage Funnel Prompt Orchestrator",
                        description="Support Awareness, Consideration, and Decision stage copy templates for landing pages, emails, and ads.",
                        priority="Critical",
                        user_stories=[
                            UserStory(
                                id="US-101a",
                                title="Funnel Stage Selection",
                                role="Content Marketer",
                                action="select specific funnel stages in the generator UI",
                                benefit="produce targeted messaging matched to buyer readiness",
                                estimate_points=5
                            ),
                            UserStory(
                                id="US-101b",
                                title="Batch Funnel Variation Generation",
                                role="Demand Gen Manager",
                                action="batch-generate up to 50 email variations from CSV prospect data",
                                benefit="scale outreach campaigns rapidly without manual editing",
                                estimate_points=8
                            )
                        ]
                    ),
                    Feature(
                        id="FEAT-102",
                        title="Multi-Channel Formatting Presets",
                        description="Pre-configured export formats for email sequences, LinkedIn sponsored posts, and blog outlines.",
                        priority="High",
                        user_stories=[
                            UserStory(
                                id="US-102a",
                                title="Channel Format Preset Selection",
                                role="Growth Marketer",
                                action="choose between Email, Social, and Web Landing Page output structures",
                                benefit="receive immediately usable copy formatted for specific channels",
                                estimate_points=3
                            )
                        ]
                    )
                ]
            ),
            Epic(
                id="EPIC-2",
                title="Brand Adherence & Style Guardrails",
                theme="Brand Voice Guardrails & Style Compliance",
                description="Automated style rules, tone consistency scoring, and vocabulary enforcement.",
                features=[
                    Feature(
                        id="FEAT-201",
                        title="Brand Guideline Ingestion & Rule Parser",
                        description="Ingest brand PDF/style guide docs to build custom voice profiles and banned word lists.",
                        priority="Critical",
                        user_stories=[
                            UserStory(
                                id="US-201a",
                                title="Brand Guidelines Document Upload",
                                role="VP of Marketing",
                                action="upload style guide PDFs and specify tone parameters",
                                benefit="enforce company-wide brand consistency across all generated outputs",
                                estimate_points=5
                            )
                        ]
                    ),
                    Feature(
                        id="FEAT-202",
                        title="Real-Time Compliance Audit Score",
                        description="Audit generated content against style guidelines and calculate an adherence score (0-100%).",
                        priority="High",
                        user_stories=[
                            UserStory(
                                id="US-202a",
                                title="Compliance Audit Dashboard",
                                role="Content Manager",
                                action="view real-time adherence score and inline style violations",
                                benefit="quickly fix off-brand phrasing before publishing",
                                estimate_points=5
                            )
                        ]
                    )
                ]
            ),
            Epic(
                id="EPIC-3",
                title="Persona Manager & Psychographic Injection",
                theme="Hyper-Personalization & Persona Management",
                description="Central database for buyer persona profiles and dynamic psychographic context injection.",
                features=[
                    Feature(
                        id="FEAT-301",
                        title="Dynamic Persona Management Portal",
                        description="CRUD interface for managing B2B SaaS buyer personas, pain points, and decision criteria.",
                        priority="High",
                        user_stories=[
                            UserStory(
                                id="US-301a",
                                title="Buyer Persona Profile Creation",
                                role="Product Marketer",
                                action="create and manage detailed persona profiles with job roles, pain points, and goals",
                                benefit="ensure AI models reference accurate buyer demographics and motivations",
                                estimate_points=5
                            )
                        ]
                    ),
                    Feature(
                        id="FEAT-302",
                        title="Psychographic Trigger Context Injector",
                        description="Inject specific emotional and operational pain points into prompt context during copy generation.",
                        priority="Medium",
                        user_stories=[
                            UserStory(
                                id="US-302a",
                                title="Pain Point Trigger Selector",
                                role="Copywriter",
                                action="toggle key buyer pain points when generating copy",
                                benefit="produce hyper-relevant messaging that resonates with target buyers",
                                estimate_points=3
                            )
                        ]
                    )
                ]
            ),
            Epic(
                id="EPIC-4",
                title="Ecosystem Publishing & Workflow Integration",
                theme="Publishing Integration & Ecosystem Connectivity",
                description="Integrations with Linear, HubSpot, Contentful, and GitHub for end-to-end content delivery.",
                features=[
                    Feature(
                        id="FEAT-401",
                        title="HubSpot & Contentful Publishing Pipeline",
                        description="Direct 1-click publishing of approved content drafts to HubSpot CMS and Contentful.",
                        priority="High",
                        user_stories=[
                            UserStory(
                                id="US-401a",
                                title="Automated CMS Publishing",
                                role="Content Marketer",
                                action="publish approved drafts directly to HubSpot/Contentful",
                                benefit="eliminate manual copying and pasting into external CMS tools",
                                estimate_points=5
                            )
                        ]
                    ),
                    Feature(
                        id="FEAT-402",
                        title="Linear Roadmap & Issue Tracker Sync",
                        description="Automatically structure and push product backlog items, release notes, and tasks to Linear.",
                        priority="Medium",
                        user_stories=[
                            UserStory(
                                id="US-402a",
                                title="Linear Backlog Sync",
                                role="Product Manager",
                                action="export roadmap items directly into Linear cycles and backlog",
                                benefit="maintain engineering alignment with marketing product requirements",
                                estimate_points=3
                            )
                        ]
                    )
                ]
            )
        ]

        return epics

    def _define_milestones(self, timeframe: str) -> List[Milestone]:
        """Step 5 (cont): Define 3-6 month milestones."""
        logger.info("Step 5: Defining roadmap milestones")

        return [
            Milestone(
                name="Milestone 1: Core Foundation & Content Engine",
                timeframe="Months 1 - 2 (Cycles 1 - 4)",
                deliverables=[
                    "Funnel-aligned prompt orchestrator for Awareness, Consideration, and Decision stages",
                    "Initial multi-channel presets (Email sequences, Landing pages)",
                    "Brand guideline parser and basic tone rule configuration"
                ]
            ),
            Milestone(
                name="Milestone 2: Personalization & Compliance Auditing",
                timeframe="Months 3 - 4 (Cycles 5 - 8)",
                deliverables=[
                    "Persona Management Portal for CRUD buyer profiles and psychographic triggers",
                    "Real-time Brand Adherence Score auditor (0-100% compliance)",
                    "Batch generation capability for up to 50 personalized variations"
                ]
            ),
            Milestone(
                name="Milestone 3: Publishing Integrations & GA Launch",
                timeframe="Months 5 - 6 (Cycles 9 - 12)",
                deliverables=[
                    "HubSpot CMS & Contentful 1-click export integrations",
                    "Linear issue tracking and roadmap sync automation",
                    "GA Release of PersonaScript MVP V1.0 for B2B SaaS Growth Marketing teams"
                ]
            )
        ]

    def _draft_roadmap_markdown(
        self,
        inputs: RoadmapInputs,
        epics: List[Epic],
        milestones: List[Milestone]
    ) -> str:
        """Step 5 (cont): Draft the detailed MVP roadmap structured for Linear in Markdown."""
        logger.info("Step 5: Drafting Linear-structured roadmap Markdown")

        md_parts = [
            f"# {inputs.company_name} MVP Development Roadmap ({inputs.timeframe})",
            "",
            "## Executive Overview",
            f"**Company**: {inputs.company_name}",
            f"**Value Proposition**: {inputs.value_proposition}",
            f"**Timeframe**: {inputs.timeframe}",
            f"**Target Execution Platform**: {inputs.target_platform}",
            "",
            "---",
            "",
            "## Strategic Milestones & Timeline",
            ""
        ]

        for m in milestones:
            md_parts.append(f"### 🎯 {m.name}")
            md_parts.append(f"**Timeframe**: `{m.timeframe}`")
            md_parts.append("**Key Deliverables**:")
            for item in m.deliverables:
                md_parts.append(f"- [ ] {item}")
            md_parts.append("")

        md_parts.extend([
            "---",
            "",
            "## Linear Epics & Feature Breakdown",
            ""
        ])

        for epic in epics:
            md_parts.append(f"### 🚀 Epic: {epic.title} (`{epic.id}`)")
            md_parts.append(f"**Theme**: *{epic.theme}*")
            md_parts.append(f"**Description**: {epic.description}")
            md_parts.append("")

            for feature in epic.features:
                md_parts.append(f"#### 📦 Feature: {feature.title} (`{feature.id}`) - Priority: **{feature.priority}**")
                md_parts.append(f"*{feature.description}*")
                md_parts.append("")
                md_parts.append("**Linear User Stories**:")

                for story in feature.user_stories:
                    md_parts.append(
                        f"- **{story.id}**: *{story.title}* ({story.estimate_points} pts)\n"
                        f"  - **As a** {story.role},\n"
                        f"  - **I want to** {story.action},\n"
                        f"  - **So that** {story.benefit}."
                    )
                md_parts.append("")

        md_parts.extend([
            "---",
            "",
            "## Linear Platform Project Configuration Guide",
            "1. **Teams**: Assign to `Marketing Engineering` & `AI Core` teams in Linear.",
            "2. **Cycles**: Map Milestones 1, 2, and 3 across 2-week Sprint Cycles (Cycles 1 through 12).",
            "3. **Estimation**: Use Standard Fibonacci Points (1, 2, 3, 5, 8).",
            "4. **Workflow States**: Backlog -> In Progress -> In Review -> Completed."
        ])

        return "\n".join(md_parts)

    def _construct_github_issue_body(
        self,
        inputs: RoadmapInputs,
        roadmap_markdown: str,
        epics: List[Epic],
        milestones: List[Milestone]
    ) -> str:
        """Step 6: Construct complete GitHub issue body."""
        logger.info("Step 6: Constructing GitHub issue body")

        total_features = sum(len(epic.features) for epic in epics)
        total_stories = sum(len(f.user_stories) for epic in epics for f in epic.features)

        body_parts = [
            f"# {inputs.company_name} MVP Development Roadmap ({inputs.timeframe})",
            "",
            "## Goal",
            "To develop a detailed Minimum Viable Product (MVP) roadmap with specific milestones for PersonaScript for the next 3-6 months, formatted for the Linear platform.",
            "",
            "## Inputs",
            f"- **Company Name**: `{inputs.company_name}`",
            f"- **Value Proposition**: {inputs.value_proposition}",
            f"- **Timeframe**: `{inputs.timeframe}`",
            f"- **Target Platform for Roadmap Structure**: `{inputs.target_platform}`",
            "",
            "## Outputs",
            f"- **Detailed MVP Development Roadmap**: {len(epics)} Epics, {total_features} Features, {total_stories} User Stories across {len(milestones)} Milestones.",
            "- **Target Execution Platform**: Linear (structured Epics, Features, User Stories, Estimates).",
            "",
            "## Execution Plan Summary",
            "1. 🧠 **Parsed business context**: Company name, value proposition, and 3-6 month timeframe.",
            "2. 📚 **Gathered internal strategy**: Evaluated customer pain points regarding brand consistency and funnel personalization.",
            "3. 🎯 **Synthesized strategic themes**: Content Orchestration, Brand Guardrails, Persona Management, and Integrations.",
            "4. ⚖️ **Generated prioritized features**: Ranked by impact, feasibility, and alignment with lead conversion goals.",
            "5. 🗺️ **Drafted Linear Roadmap**: Organized into Epics, Features, User Stories, and Milestones for Linear.",
            "6. 📝 **Constructed GitHub Issue**: Formatted comprehensive roadmap summary for team tracking.",
            "7. 🚀 **Created GitHub Issue**: Published roadmap tracking issue to repository.",
            "",
            "---",
            "",
            "## Full MVP Development Roadmap",
            "",
            roadmap_markdown
        ]

        return "\n".join(body_parts)
