"""
PersonaScriptPRDDrafterAgent - Main agent for drafting MVP PRDs focusing on brand alignment and personalization.

This agent analyzes value propositions and feature concepts to:
1. Comprehend and parse inputs
2. Define core functionalities for the MVP
3. Generate detailed user stories
4. Develop comprehensive acceptance criteria
5. Compile everything into a cohesive Product Requirements Document (PRD) V0.9
6. Create and publish the PRD in Notion
7. Create a review issue in Linear
8. Summarize and link everything in a GitHub issue
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from ..integrations.notion_integration import NotionIntegration
from ..integrations.linear_integration import LinearIntegration
from ..integrations.github_integration import GitHubIntegration


logger = logging.getLogger(__name__)


@dataclass
class UserStory:
    """Represents a detailed user story with acceptance criteria."""

    id: str
    title: str
    role: str
    action: str
    benefit: str
    acceptance_criteria: List[str]


@dataclass
class CoreFunctionality:
    """Represents a core functionality defined for the MVP."""

    name: str
    description: str
    user_stories: List[UserStory]


@dataclass
class AgentInputs:
    """Input data for the PersonaScriptPRDDrafterAgent."""

    value_proposition: str
    feature_concepts: List[str]


@dataclass
class AgentOutputs:
    """Output data from the PersonaScriptPRDDrafterAgent."""

    notion_prd_url: str
    linear_issue_url: str
    github_issue_url: str
    prd_content: str
    core_functionalities: List[CoreFunctionality]


class PersonaScriptPRDDrafterAgent:
    """
    Main agent class for drafting MVP Product Requirements Documents.

    This agent follows an 8-step execution plan:
    1. Parse and comprehend context and value proposition.
    2. Define core functionalities for the MVP emphasizing brand alignment and personalization.
    3. Generate detailed user stories for each core functionality.
    4. Develop comprehensive acceptance criteria for each user story.
    5. Compile everything into a cohesive PRD draft titled 'PersonaScript MVP Features PRD - V0.9'.
    6. Create a Notion page and publish the drafted PRD.
    7. Create a Linear issue to initiate the PRD review process.
    8. Create a GitHub issue summarizing the task, inputs, outputs, and steps taken.
    """

    def __init__(
        self,
        notion_token: Optional[str] = None,
        notion_database_id: Optional[str] = None,
        linear_token: Optional[str] = None,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """
        Initialize the PersonaScriptPRDDrafterAgent.

        Args:
            notion_token: Token for Notion integration
            notion_database_id: Database ID for Notion integration (optional)
            linear_token: Token for Linear integration
            github_token: Token for GitHub API
            github_repo: Repository name (format: "owner/repo")
        """
        self.notion_integration = NotionIntegration(token=notion_token, database_id=notion_database_id)
        self.linear_integration = LinearIntegration(token=linear_token)
        self.github_integration = GitHubIntegration(token=github_token, repo=github_repo)

        self.core_functionalities: List[CoreFunctionality] = []
        self.prd_content: str = ""

        logger.info("PersonaScriptPRDDrafterAgent initialized")

    def execute(self, inputs: AgentInputs) -> AgentOutputs:
        """
        Execute the complete 8-step PRD drafting workflow.

        Args:
            inputs: Input data containing value proposition and high-level feature concepts

        Returns:
            AgentOutputs containing published URLs and drafted PRD data
        """
        logger.info("Starting PersonaScriptPRDDrafterAgent execution")

        # Step 1: Parse and comprehend the inputs
        parsed_context = self._parse_context(inputs)

        # Step 2: Define core functionalities emphasizing brand alignment and personalization
        self.core_functionalities = self._define_core_functionalities(parsed_context)

        # Step 3 & 4: Generate detailed user stories and acceptance criteria
        # Already handled during the construction of CoreFunctionality objects

        # Step 5: Compile into a cohesive PRD draft
        self.prd_content = self._compile_prd(inputs.value_proposition, self.core_functionalities)

        # Step 6: Create and publish Notion page
        notion_prd_url = self._publish_to_notion(self.prd_content)

        # Step 7: Create Linear review issue
        linear_issue_url = self._create_linear_issue(notion_prd_url)

        # Step 8: Create GitHub issue summarizing the task and linking outputs
        github_issue_url = self._create_github_issue(notion_prd_url, linear_issue_url, inputs)

        outputs = AgentOutputs(
            notion_prd_url=notion_prd_url,
            linear_issue_url=linear_issue_url,
            github_issue_url=github_issue_url,
            prd_content=self.prd_content,
            core_functionalities=self.core_functionalities
        )

        logger.info("PersonaScriptPRDDrafterAgent execution completed successfully")
        return outputs

    def _parse_context(self, inputs: AgentInputs) -> Dict[str, Any]:
        """
        Step 1: Parse and comprehend the value proposition and high-level feature concepts.

        Args:
            inputs: AgentInputs containing value prop and feature concepts

        Returns:
            Parsed context dictionary
        """
        logger.info("Step 1: Parsing and comprehending context")

        return {
            "value_proposition": inputs.value_proposition,
            "feature_concepts": [fc.strip() for fc in inputs.feature_concepts if fc.strip()]
        }

    def _define_core_functionalities(self, parsed_context: Dict[str, Any]) -> List[CoreFunctionality]:
        """
        Step 2, 3, 4: Define core functionalities, generate detailed user stories, and develop acceptance criteria.

        Args:
            parsed_context: Parsed context dictionary

        Returns:
            List of CoreFunctionality objects
        """
        logger.info("Step 2-4: Defining core functionalities, user stories, and acceptance criteria")

        feature_concepts = parsed_context["feature_concepts"]
        functionalities = []

        for concept in feature_concepts:
            if "Dynamic Content Generation" in concept:
                # Dynamic Content Generation core functionality
                stories = [
                    UserStory(
                        id="US-001",
                        title="Multi-stage Funnel Generation",
                        role="B2B SaaS Content Marketer",
                        action="generate variations of content tailored to specific sales funnel stages (Awareness, Consideration, Decision)",
                        benefit="rapidly produce targeted copy that moves prospects through the funnel and improves lead conversion",
                        acceptance_criteria=[
                            "User can select between Awareness, Consideration, and Decision funnel stages in the content generation panel.",
                            "The system prompts the user to select the preferred format (e.g., email sequence, landing page, social copy).",
                            "The generation engine dynamically alters CTA aggressiveness, depth of technical details, and focus topics according to the selected funnel stage.",
                            "The system delivers the output within 15 seconds of request submission.",
                            "Generated content features clear placeholders for personalization tags such as {{company_name}} and {{industry}}."
                        ]
                    ),
                    UserStory(
                        id="US-002",
                        title="High-Volume Batch Production",
                        role="Demand Generation Director",
                        action="batch-generate up to 50 content variations simultaneously for a targeted advertising/email segment",
                        benefit="rapidly scale multi-channel personalization without manual copy pasting or individual prompt creation",
                        acceptance_criteria=[
                            "User can upload a CSV list of prospect details (e.g., role, company name, industry, current tool).",
                            "The system generates unique personalized copy for each row in the uploaded CSV.",
                            "The user can preview at least 3 sample outputs prior to initiating full batch generation.",
                            "The final batch output can be exported as a single structured ZIP file containing individual markdown files, or a unified CSV format."
                        ]
                    )
                ]
                functionalities.append(
                    CoreFunctionality(
                        name="Dynamic Content Generation",
                        description=(
                            "The central content creation engine of PersonaScript. It utilizes advanced LLM prompts "
                            "and context injection to rapidly generate highly relevant, high-volume B2B marketing collateral "
                            "customized for multiple channels, buyer personas, and sales funnel stages."
                        ),
                        user_stories=stories
                    )
                )

            elif "Brand Guideline Adherence Engine" in concept:
                # Brand Guideline Adherence Engine core functionality
                stories = [
                    UserStory(
                        id="US-003",
                        title="Brand Voice and Tone Configuration",
                        role="VP of Marketing",
                        action="upload, configure, and save custom brand guidelines including style manuals, voice definitions, and specific tone presets",
                        benefit="ensure all machine-generated content maintains consistent brand voice and style alignment without manual proofreading",
                        acceptance_criteria=[
                            "User can upload brand guidelines as a PDF or text document up to 10MB.",
                            "The system parses and highlights critical stylistic rules, tone adjectives, and formatting guidelines.",
                            "The system allows the configuration of explicit 'banned words', 'restricted phrases', and 'preferred synonyms' lists.",
                            "The system provides a visual tone-slider configuration (e.g., professional vs. casual, technical vs. simple) to fine-tune the output profile."
                        ]
                    ),
                    UserStory(
                        id="US-004",
                        title="Real-time Style & Adherence Auditing",
                        role="Content Manager",
                        action="run an automated adherence audit on any generated draft to analyze compliance with saved brand parameters",
                        benefit="identify and resolve stylistic inconsistencies, terminology violations, or tone drifts prior to content publishing",
                        acceptance_criteria=[
                            "The system runs a stylistic and vocabulary analysis comparing the generated draft to saved brand guidelines.",
                            "The system displays an overall 'Brand Adherence Score' from 0% to 100%.",
                            "All instances of banned words or critical tone drifts are highlighted inline with contextual hover explanations.",
                            "The user is presented with one-click automated correction suggestions to align the flagged content with brand parameters."
                        ]
                    )
                ]
                functionalities.append(
                    CoreFunctionality(
                        name="Brand Guideline Adherence Engine",
                        description=(
                            "An automated style enforcement and compliance auditing system that ingests corporate brand guidelines, "
                            "extracts voice and rulesets, and guarantees generated collateral consistently aligns with brand tone "
                            "and vocabulary constraints."
                        ),
                        user_stories=stories
                    )
                )

            elif "User Profile Personalization" in concept:
                # User Profile Personalization core functionality
                stories = [
                    UserStory(
                        id="US-005",
                        title="Persona Database Management",
                        role="Growth Marketing Lead",
                        action="create, view, and organize custom buyer persona profiles containing rich demographic, firmographic, and psychographic attributes",
                        benefit="easily inject structured prospect context into the content generation engine for hyper-focused personalization",
                        acceptance_criteria=[
                            "User can create, read, update, and delete (CRUD) buyer persona profiles within a dedicated Persona Manager panel.",
                            "Each persona profile must capture demographic attributes (e.g., seniority, job title), firmographic attributes (e.g., industry, company size, growth stage), and psychographic details (e.g., primary pain points, personal goals, key motivations).",
                            "The system offers out-of-the-box preloaded templates for standard B2B SaaS buyer roles (e.g., CMO, VP of Sales, CTO).",
                            "User can tag personas for easy filtering and multi-persona batch generation campaigns."
                        ]
                    ),
                    UserStory(
                        id="US-006",
                        title="Psychographic Trigger Injection",
                        role="Growth Marketer",
                        action="specify a primary psychographic pain point or motivation from a persona profile during generation",
                        benefit="ensure generated messaging directly addresses the core psychological drivers and bottlenecks of the recipient",
                        acceptance_criteria=[
                            "The content generation interface lists saved pain points and motivations associated with the selected persona.",
                            "The user can toggle which pain points/motivations to prioritize for the generation prompt.",
                            "The system references specific psychological pain points in the generated headline and introduction copy.",
                            "The system provides a rationale summary alongside the draft, explaining how the copy targets the selected psychographic triggers."
                        ]
                    )
                ]
                functionalities.append(
                    CoreFunctionality(
                        name="User Profile Personalization",
                        description=(
                            "A central repository of buyer segment attributes and dynamic injection system. It stores "
                            "detailed buyer roles, goals, motivations, and pain points, passing these parameters into the generation "
                            "pipeline to produce hyper-personalized copy targeting the exact buyer mindset."
                        ),
                        user_stories=stories
                    )
                )

            else:
                # Fallback for generic feature concepts
                stories = [
                    UserStory(
                        id=f"US-{abs(hash(concept)) % 1000:03d}",
                        title=f"{concept} Management",
                        role="B2B SaaS Marketer",
                        action=f"utilize {concept} features to configure and scale marketing campaign copy",
                        benefit="accelerate conversion rates and content velocity",
                        acceptance_criteria=[
                            f"The user can configure inputs for {concept} within the user interface.",
                            f"The system processes the configuration of {concept} in under 10 seconds.",
                            f"Output demonstrates clear alignment with B2B SaaS best practices."
                        ]
                    )
                ]
                functionalities.append(
                    CoreFunctionality(
                        name=concept,
                        description=f"Core MVP capability delivering {concept} to streamline B2B SaaS marketing workflows.",
                        user_stories=stories
                    )
                )

        return functionalities

    def _compile_prd(self, value_proposition: str, functionalities: List[CoreFunctionality]) -> str:
        """
        Step 5: Compile core functionalities, user stories, and acceptance criteria into a cohesive PRD draft.

        Args:
            value_proposition: Value proposition string
            functionalities: List of CoreFunctionality objects

        Returns:
            Cohesive Markdown formatted PRD
        """
        logger.info("Step 5: Compiling cohesive PRD V0.9")

        parts = [
            "# PersonaScript MVP Features PRD - V0.9",
            "",
            "## 1. Executive Summary",
            "",
            "### 1.1 Product Purpose & Value Proposition",
            f"**PersonaScript** is an AI-powered content orchestration and generation platform. {value_proposition}",
            "",
            "### 1.2 Document Scope",
            "This Product Requirements Document (PRD) outlines the essential MVP feature set required to deliver "
            "on the core promise of brand-aligned and highly-personalized B2B SaaS content generation. "
            "It establishes the baseline functionalities, detailed user stories, and acceptance criteria "
            "necessary for the initial engineering cycle.",
            "",
            "---",
            "",
            "## 2. Core Functional Requirements",
            "",
            "The PersonaScript MVP is focused on three high-impact technical pillars: **Dynamic Content Generation**, "
            "**Brand Guideline Adherence Engine**, and **User Profile Personalization**.",
            ""
        ]

        for index, func in enumerate(functionalities, 1):
            parts.extend([
                f"### 2.{index} {func.name}",
                f"{func.description}",
                ""
            ])

            for story in func.user_stories:
                parts.extend([
                    f"#### {story.id}: {story.title}",
                    f"**As a** {story.role},",
                    f"**I want to** {story.action},",
                    f"**So that** {story.benefit}.",
                    "",
                    "**Acceptance Criteria:**",
                    *[f"- [ ] {ac}" for ac in story.acceptance_criteria],
                    ""
                ])

        parts.extend([
            "---",
            "",
            "## 3. System Integrations & External Interfaces",
            "",
            "- **Notion Integration**: Central wiki for collaboration, requirements drafting, and feature specification.",
            "- **Linear Integration**: Automated issue tracking, story assignment, and development cycle management.",
            "- **GitHub Integration**: Repository-level task assignment, developer summaries, and release tracking.",
            "",
            "## 4. Key Performance Benchmarks & Success Metrics",
            "",
            "1. **Generation Latency**: Single-page content generation must complete in less than 15 seconds.",
            "2. **Adherence Auditing Accuracy**: Stylistic audits must identify guideline infractions with >90% precision.",
            "3. **Export Completeness**: Batch export artifacts must maintain structured file hierarchies without data loss.",
            "4. **Brand Consistency**: Generated variations must score at least 85% on the automated Brand Adherence Scale."
        ])

        return "\n".join(parts)

    def _publish_to_notion(self, prd_content: str) -> str:
        """
        Step 6: Create and publish the drafted PRD in Notion.

        Args:
            prd_content: Cohesive PRD markdown content

        Returns:
            URL of the created Notion page
        """
        logger.info("Step 6: Publishing PRD to Notion")
        notion_url = self.notion_integration.create_page(
            title="PersonaScript MVP Features PRD - V0.9",
            content=prd_content
        )
        logger.info(f"Published Notion page: {notion_url}")
        return notion_url

    def _create_linear_issue(self, notion_url: str) -> str:
        """
        Step 7: Create a new issue in Linear to initiate the PRD review process.

        Args:
            notion_url: Notion page URL

        Returns:
            URL of the created Linear issue
        """
        logger.info("Step 7: Creating Linear review issue")

        title = "PRD Review: PersonaScript MVP Features PRD - V0.9"
        description = (
            f"An initial draft of the PersonaScript MVP Features PRD (Version 0.9) has been successfully generated.\n\n"
            f"Please review the core functionalities, user stories, and acceptance criteria in Notion:\n"
            f"👉 [Notion PRD Draft (V0.9)]({notion_url})\n\n"
            f"**Review Objectives:**\n"
            f"1. Validate alignment with B2B SaaS target personas.\n"
            f"2. Confirm technical feasibility of the Brand Guideline Adherence Engine.\n"
            f"3. Sign off on acceptance criteria for Dynamic Content Generation."
        )

        linear_url = self.linear_integration.create_issue(
            title=title,
            description=description,
            assignees=["Product Team"]
        )
        logger.info(f"Created Linear issue: {linear_url}")
        return linear_url

    def _create_github_issue(self, notion_url: str, linear_url: str, inputs: AgentInputs) -> str:
        """
        Step 8: Create a GitHub issue summarizing the task, inputs, outputs, and steps taken.

        Args:
            notion_url: Notion page URL
            linear_url: Linear issue URL
            inputs: Original inputs for context

        Returns:
            URL of the created GitHub issue
        """
        logger.info("Step 8: Creating GitHub summary issue")

        title = "PersonaScript MVP Features PRD V0.9 Drafted for Review"
        body = f"""# PersonaScript MVP Features PRD V0.9 Drafted for Review

## Goal
Draft an initial Product Requirements Document (PRD) for MVP features focusing on brand alignment and personalization for PersonaScript.

## Inputs
- **Value Proposition**: "{inputs.value_proposition}"
- **High-level MVP Feature Concepts**: {", ".join([f"`{fc}`" for fc in inputs.feature_concepts])}

## Outputs Generated

- **Notion PRD URL**: {notion_url}
- **Linear Review Issue URL**: {linear_url}

## Execution Steps Taken
1. 🧠 **Parsed and comprehended** the PersonaScript value proposition and MVP feature concepts.
2. 🛠️ **Defined core functionalities** for the MVP emphasizing Brand Guideline Adherence and User Personalization.
3. 📝 **Generated detailed user stories** specifying B2B SaaS buyer roles, actions, and benefits.
4. 🔍 **Developed comprehensive acceptance criteria** with strict performance latency limits and functional constraints.
5. 📄 **Compiled everything** into a professional Product Requirements Document titled `PersonaScript MVP Features PRD - V0.9`.
6. 🌐 **Published the drafted PRD** to Notion for persistent, cross-team access.
7. 🚦 **Initiated the review process** in Linear by creating a tracking issue linking the Notion PRD.
8. 🚀 **Created this GitHub issue** to summarize the completed automated workflow and establish traceability.

## Next Steps
- Product and engineering stakeholders to review the PRD draft in [Notion]({notion_url}).
- Tracks progress and log feedback comments in the [Linear Issue]({linear_url}).
"""

        github_url = self.github_integration.create_issue(
            title=title,
            body=body,
            labels=["prd-review", "mvp-scoping", "completed"]
        )
        logger.info(f"Created GitHub issue: {github_url}")
        return github_url
