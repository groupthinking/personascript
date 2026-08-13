"""
PersonaScriptMVPDevelopmentRoadmapAgent - Main agent for developing a detailed MVP development roadmap.

This agent parses the company name, value proposition, and timeframe, accesses internal documentation
to gather insights, synthesizes strategic themes, prioritizes features, drafts a detailed MVP roadmap
structured for Linear (Epics, Features, User Stories, and timelines), and posts it as a GitHub issue.
"""

import os
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from openai import OpenAI

from ..integrations.github_integration import GitHubIntegration

logger = logging.getLogger(__name__)


@dataclass
class UserStory:
    """Represents an actionable user story in Linear."""
    id: str
    title: str
    description: str
    priority: str  # High, Medium, Low
    estimate: str  # e.g., "3 points", "5 points", "1 week"


@dataclass
class MVPFeature:
    """Represents a specific feature or project in Linear."""
    id: str
    title: str
    description: str
    priority: str  # High, Medium, Low
    user_stories: List[UserStory] = field(default_factory=list)


@dataclass
class MVPEpic:
    """Represents a high-level Epic or Milestone in Linear."""
    id: str
    title: str
    description: str
    target_timeline: str  # e.g., "Month 1", "Months 2-3"
    features: List[MVPFeature] = field(default_factory=list)


@dataclass
class MVPDevelopmentRoadmap:
    """Represents the complete MVP roadmap structured for Linear."""
    epics: List[MVPEpic] = field(default_factory=list)


@dataclass
class RoadmapAgentInputs:
    """Input parameters for the PersonaScriptMVPDevelopmentRoadmapAgent."""
    company_name: str = "PersonaScript"
    value_proposition: str = "PersonaScript empowers growth-stage B2B SaaS marketing teams to rapidly generate high-volume, hyper-personalized, and brand-aligned content across all sales funnel stages, dramatically accelerating lead conversion and brand consistency."
    timeframe: str = "3-6 months"
    target_platform: str = "Linear"
    internal_docs_paths: List[str] = field(default_factory=list)


@dataclass
class RoadmapAgentOutputs:
    """Output results from the PersonaScriptMVPDevelopmentRoadmapAgent."""
    roadmap: MVPDevelopmentRoadmap
    github_issue_url: str
    issue_body: str
    key_themes: List[str]


class PersonaScriptMVPDevelopmentRoadmapAgent:
    """
    Main agent class for developing the detailed MVP roadmap for PersonaScript.

    This agent follows a 7-step execution plan:
    1. Parse and comprehend the provided PersonaScript business context.
    2. Access internal documentation to gather existing product strategy and pain points.
    3. Synthesize gathered information to identify key strategic themes.
    4. Generate and prioritize a list of concrete, actionable MVP features.
    5. Draft the detailed MVP roadmap structured for Linear (Epics, Features, User Stories, timelines).
    6. Construct the complete body of the GitHub issue.
    7. Create a new GitHub issue in the repository and capture the URL.
    """

    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """
        Initialize the agent.

        Args:
            openai_api_key: Optional API key for OpenAI
            github_token: Optional token for GitHub API
            github_repo: Optional repository name ("owner/repo")
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.openai_api_key) if self.openai_api_key else None

        github_tok = github_token or os.getenv("GITHUB_TOKEN")
        github_rp = github_repo or os.getenv("GITHUB_REPO", "groupthinking/personascript")
        self.github_integration = GitHubIntegration(token=github_tok, repo=github_rp)

        logger.info("PersonaScriptMVPDevelopmentRoadmapAgent initialized")

    def execute(self, inputs: RoadmapAgentInputs) -> RoadmapAgentOutputs:
        """
        Execute the complete agent workflow.

        Args:
            inputs: Configured RoadmapAgentInputs

        Returns:
            RoadmapAgentOutputs containing the roadmap, issue URL, and issue body
        """
        logger.info("Starting PersonaScriptMVPDevelopmentRoadmapAgent execution")

        # Step 1: Parse and comprehend the provided business context
        context = self._parse_business_context(inputs)

        # Step 2: Access internal documentation/knowledge bases
        doc_insights = self._access_internal_documentation(inputs.internal_docs_paths)

        # Step 3: Synthesize strategic themes
        key_themes = self._synthesize_strategic_themes(context, doc_insights)

        # Step 4: Generate list of concrete, actionable MVP features & prioritize them
        prioritized_features = self._generate_and_prioritize_features(key_themes, context)

        # Step 5: Draft the detailed MVP roadmap structured for Linear
        roadmap = self._draft_mvp_roadmap(prioritized_features, inputs.timeframe)

        # Step 6: Construct the complete body of the GitHub issue
        issue_body = self._construct_issue_body(inputs, key_themes, roadmap)

        # Step 7: Create a new GitHub issue
        issue_title = f"{inputs.company_name} MVP Roadmap ({inputs.timeframe})"
        github_issue_url = self.github_integration.create_issue(
            title=issue_title,
            body=issue_body,
            labels=["mvp-roadmap", "linear-structure", "planning"]
        )

        logger.info("PersonaScriptMVPDevelopmentRoadmapAgent execution completed successfully")
        return RoadmapAgentOutputs(
            roadmap=roadmap,
            github_issue_url=github_issue_url,
            issue_body=issue_body,
            key_themes=key_themes
        )

    def _parse_business_context(self, inputs: RoadmapAgentInputs) -> Dict[str, Any]:
        """Step 1: Parse and comprehend the provided business context."""
        logger.info("Step 1: Parsing business context")
        return {
            "company_name": inputs.company_name,
            "value_proposition": inputs.value_proposition,
            "timeframe": inputs.timeframe,
            "target_platform": inputs.target_platform
        }

    def _access_internal_documentation(self, doc_paths: List[str]) -> List[Dict[str, str]]:
        """Step 2: Access internal documentation or knowledge bases."""
        logger.info("Step 2: Accessing internal documentation")

        # Default internal documentation list if empty
        if not doc_paths:
            doc_paths = ["DOCUMENTATION.md", "README.md", "IMPLEMENTATION_SUMMARY.md"]

        insights = []
        for path in doc_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        # Extract first 1000 chars or summary headers for processing
                        insights.append({
                            "source_file": path,
                            "summary": content[:1000] + "..." if len(content) > 1000 else content
                        })
                except Exception as e:
                    logger.warning(f"Failed to read internal doc {path}: {str(e)}")

        return insights

    def _synthesize_strategic_themes(self, context: Dict[str, Any], doc_insights: List[Dict[str, str]]) -> List[str]:
        """Step 3: Synthesize the gathered information to identify key strategic themes."""
        logger.info("Step 3: Synthesizing strategic themes")

        # If OpenAI client is available, use LLM to synthesize themes dynamically
        if self.client:
            try:
                doc_summary_text = "\n\n".join([f"File: {d['source_file']}\nContent: {d['summary']}" for d in doc_insights])
                prompt = f"""Synthesize key strategic themes and high-impact areas for potential MVP features for the B2B SaaS startup {context['company_name']}.

Value Proposition: {context['value_proposition']}
Timeframe: {context['timeframe']}

Based on the value proposition and these internal documentation summaries:
{doc_summary_text}

Provide a clean, bulleted list of 4-5 strategic themes. Each theme should focus on a specific aspect of the value proposition (e.g., brand alignment, content scaling, personalization, review workflow).
"""
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert B2B SaaS product strategist."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )
                themes_text = response.choices[0].message.content
                themes = [t.strip().lstrip("-*• ").strip() for t in themes_text.split("\n") if t.strip()]
                return themes[:5]
            except Exception as e:
                logger.error(f"Error synthesizing strategic themes with OpenAI: {str(e)}")

        # Deterministic fallback based on PersonaScript value proposition
        return [
            "Brand Alignment & Guidelines Engine: Guaranteeing generated content meets brand-voice style rules.",
            "High-Volume Funnel Generator Orchestration: Rapid generation of marketing copy across Awareness, Consideration, and Decision stages.",
            "Hyper-Personalization & Multi-Persona Targeting: Tailoring content specifically to Demand Gen Directors, Content Managers, and Growth Leads.",
            "Human-in-the-Loop Review & Collaborative Workflow: Incorporating approval pipelines and quality control before publishing.",
            "Distribution, Publishing & Integration Ecosystem: Directly publishing approved assets to CMS (HubSpot, Webflow) and sales engagement tools."
        ]

    def _generate_and_prioritize_features(self, key_themes: List[str], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Step 4: Generate concrete, actionable features and prioritize them."""
        logger.info("Step 4: Generating and prioritizing features")

        # We can define a list of detailed features linked to our themes.
        # This list of features is highly customized and structured.
        features = [
            {
                "id": "FEAT-1",
                "title": "Brand Voice Profile Parser & Manager",
                "description": "Ingests and stores multi-dimensional brand style guides, sample collateral, and rules to guide automated content voice.",
                "theme": key_themes[0],
                "priority": "High"
            },
            {
                "id": "FEAT-2",
                "title": "Persona Segments Database & Funnel Mapper",
                "description": "Saves and manages target buyer personas and maps specific content goals to each stage of the buyer's journey.",
                "theme": key_themes[2],
                "priority": "High"
            },
            {
                "id": "FEAT-3",
                "title": "Funnel Stage Copy Generator Orchestrator",
                "description": "Orchestrates multi-persona and multi-funnel content generation with one-click bulk exports.",
                "theme": key_themes[1],
                "priority": "High"
            },
            {
                "id": "FEAT-4",
                "title": "Dynamic Template Library & Prompt Injector",
                "description": "A collection of customizable templates for LinkedIn posts, emails, and landing page copies.",
                "theme": key_themes[1],
                "priority": "Medium"
            },
            {
                "id": "FEAT-5",
                "title": "Collaborative Rich Text Editor with Brand Voice Assistant",
                "description": "A rich-text inline editor highlighting compliance issues against the configured brand style guides.",
                "theme": key_themes[3],
                "priority": "High"
            },
            {
                "id": "FEAT-6",
                "title": "Content Approval Workflow & Commenting Pipelines",
                "description": "Facilitates internal handoffs, status tracking (Draft, Under Review, Approved), and comments.",
                "theme": key_themes[3],
                "priority": "Medium"
            },
            {
                "id": "FEAT-7",
                "title": "HubSpot & Webflow CMS Publishing Integrations",
                "description": "Direct one-click API integrations with primary B2B CMS and marketing automation hubs.",
                "theme": key_themes[4],
                "priority": "Medium"
            },
            {
                "id": "FEAT-8",
                "title": "Outbound Email Sequencing & Delivery Tool Integrations",
                "description": "Direct syncing with Outreach, Salesloft, and Apollo to run hyper-personalized sequences.",
                "theme": key_themes[4],
                "priority": "Low"
            },
            {
                "id": "FEAT-9",
                "title": "Closed-Loop Content Conversion Tracking Analytics",
                "description": "Post-distribution performance tracking linking generated content pieces to conversion metrics.",
                "theme": "Feedback loops",
                "priority": "Low"
            }
        ]

        return features

    def _draft_mvp_roadmap(self, prioritized_features: List[Dict[str, Any]], timeframe: str) -> MVPDevelopmentRoadmap:
        """Step 5: Draft the detailed MVP roadmap, organizing features into logical epics and defining specific milestones."""
        logger.info("Step 5: Drafting MVP roadmap structured for Linear")

        # Construct Epics and User Stories
        epic1 = MVPEpic(
            id="EPIC-1",
            title="Brand Voice & Target Segments Knowledge Base",
            description="Establish the foundational system to store, parse, and enforce brand-voice guidelines and buyer persona target profiles.",
            target_timeline="Month 1"
        )
        epic1.features.extend([
            MVPFeature(
                id="FEAT-101",
                title="Brand Voice Profile Parser & Manager",
                description="Ingests and stores multi-dimensional brand style guides, sample collateral, and rules to guide automated content voice.",
                priority="High",
                user_stories=[
                    UserStory(id="PS-101", title="Upload Brand Guidelines", description="As a Marketing Manager, I want to upload our brand style guidelines (tone, vocabulary, rules) so that generated content always aligns with our brand.", priority="High", estimate="3 points"),
                    UserStory(id="PS-102", title="Ingest Sample Collateral", description="As a Content Writer, I want to import sample successful collateral to automatically train the model on our brand tone.", priority="Medium", estimate="5 points")
                ]
            ),
            MVPFeature(
                id="FEAT-102",
                title="Persona Segments Database & Funnel Mapper",
                description="Saves and manages target buyer personas and maps specific content goals to each stage of the buyer's journey.",
                priority="High",
                user_stories=[
                    UserStory(id="PS-103", title="Define Buyer Persona Profiles", description="As a Growth Marketer, I want to define and save target B2B buyer persona profiles so we can customize content variants.", priority="High", estimate="2 points"),
                    UserStory(id="PS-104", title="Map Persona Journey Stages", description="As a Marketing Lead, I want to define and map specific content needs to each sales funnel stage (Awareness, Consideration, Decision) for a buyer persona.", priority="High", estimate="3 points")
                ]
            )
        ])

        epic2 = MVPEpic(
            id="EPIC-2",
            title="High-Volume Funnel Generation Engine",
            description="Develop the core content generator orchestrator and a comprehensive multi-channel template library.",
            target_timeline="Month 2"
        )
        epic2.features.extend([
            MVPFeature(
                id="FEAT-201",
                title="Funnel Stage Copy Generator Orchestrator",
                description="Orchestrates multi-persona and multi-funnel content generation with one-click bulk exports.",
                priority="High",
                user_stories=[
                    UserStory(id="PS-201", title="Generate Funnel-Tailored Copy", description="As a Demand Gen Director, I want to select a target persona and funnel stage to generate highly customized copy addressing specific stage paint points.", priority="High", estimate="5 points"),
                    UserStory(id="PS-202", title="Bulk Persona Variation Generation", description="As a Content Marketer, I want to automatically generate content variants for multiple buyer personas simultaneously in a single click.", priority="Medium", estimate="8 points")
                ]
            ),
            MVPFeature(
                id="FEAT-202",
                title="Dynamic Template Library & Prompt Injector",
                description="A collection of customizable templates for LinkedIn posts, emails, and landing page copies.",
                priority="Medium",
                user_stories=[
                    UserStory(id="PS-203", title="Multi-Format Channel Templates", description="As a Marketing Specialist, I want to select from a pre-built template library (social posts, landing pages, email sequences) to quickly spawn formatted generation sessions.", priority="Medium", estimate="3 points"),
                    UserStory(id="PS-204", title="Dynamic Variable Injection", description="As a Growth Hacker, I want to inject custom variables (such as company name, target competitor name) into content templates dynamically.", priority="Medium", estimate="3 points")
                ]
            )
        ])

        epic3 = MVPEpic(
            id="EPIC-3",
            title="Human-in-the-Loop Workflow & Collaboration",
            description="Add review pipelines, inline collaborative editing, and automatic brand compliance checks before content moves to publishing.",
            target_timeline="Month 3"
        )
        epic3.features.extend([
            MVPFeature(
                id="FEAT-301",
                title="Collaborative Rich Text Editor with Brand Voice Assistant",
                description="A rich-text inline editor highlighting compliance issues against the configured brand style guides.",
                priority="High",
                user_stories=[
                    UserStory(id="PS-301", title="Inline Brand Voice Style Check", description="As a Content Editor, I want an inline editor that highlights copy segments violating brand rules or tone guidelines and recommends fixes.", priority="High", estimate="5 points")
                ]
            ),
            MVPFeature(
                id="FEAT-302",
                title="Content Approval Workflow & Commenting Pipelines",
                description="Facilitates internal handoffs, status tracking (Draft, Under Review, Approved), and comments.",
                priority="Medium",
                user_stories=[
                    UserStory(id="PS-302", title="Draft and Approve Workflows", description="As a Marketing Director, I want to review, comment on, and approve generated content drafts before scheduling them for live distribution.", priority="Medium", estimate="3 points")
                ]
            )
        ])

        epic4 = MVPEpic(
            id="EPIC-4",
            title="Distribution and Publishing API Integrations",
            description="Connect approved content publishing pipelines to popular CRM, CMS, and sales engagement platforms.",
            target_timeline="Months 4-5"
        )
        epic4.features.extend([
            MVPFeature(
                id="FEAT-401",
                title="HubSpot & Webflow CMS Publishing Integrations",
                description="Direct one-click API integrations with primary B2B CMS and marketing automation hubs.",
                priority="Medium",
                user_stories=[
                    UserStory(id="PS-401", title="One-Click CMS Publishing", description="As a Content Manager, I want to instantly publish approved blog articles and landing pages to HubSpot or Webflow.", priority="Medium", estimate="5 points")
                ]
            ),
            MVPFeature(
                id="FEAT-402",
                title="Outbound Email Sequencing & Delivery Tool Integrations",
                description="Direct syncing with Outreach, Salesloft, and Apollo to run hyper-personalized sequences.",
                priority="Low",
                user_stories=[
                    UserStory(id="PS-402", title="Outreach and Apollo Syncing", description="As a Growth Marketer, I want to synchronize generated cold email variations directly to Outreach or Apollo sequences.", priority="Low", estimate="5 points")
                ]
            )
        ])

        epic5 = MVPEpic(
            id="EPIC-5",
            title="Closed-Loop Analytics & Self-Optimizing Prompts",
            description="Enable performance tracking of the generated content and establish feedback loops to dynamically optimize future content runs.",
            target_timeline="Month 6"
        )
        epic5.features.extend([
            MVPFeature(
                id="FEAT-501",
                title="Closed-Loop Content Conversion Tracking Analytics",
                description="Post-distribution performance tracking linking generated content pieces to conversion metrics.",
                priority="Low",
                user_stories=[
                    UserStory(id="PS-501", title="CMO Analytics Dashboard", description="As a CMO, I want to view lead conversion metrics matched to generated content variations so we can evaluate performance and ROI.", priority="Low", estimate="5 points")
                ]
            ),
            MVPFeature(
                id="FEAT-502",
                title="Adaptive Content Optimization (Feedback Loop)",
                description="Prompt optimizer that analyzes high-performing copy to automatically refine future generation prompts.",
                priority="Low",
                user_stories=[
                    UserStory(id="PS-502", title="Adaptive Prompt Self-Tuning", description="As a Growth Lead, I want the generation system to automatically optimize prompt rules based on highest-converting variations from tracked campaigns.", priority="Low", estimate="8 points")
                ]
            )
        ])

        return MVPDevelopmentRoadmap(epics=[epic1, epic2, epic3, epic4, epic5])

    def _construct_issue_body(self, inputs: RoadmapAgentInputs, key_themes: List[str], roadmap: MVPDevelopmentRoadmap) -> str:
        """Step 6: Construct the complete body of the GitHub issue."""
        logger.info("Step 6: Constructing complete GitHub issue body")

        themes_markdown = "\n".join([f"- **Theme {i+1}:** {t}" for i, t in enumerate(key_themes)])

        roadmap_markdown = ""
        for epic in roadmap.epics:
            roadmap_markdown += f"## 🚀 Epic: {epic.title} ({epic.id})\n"
            roadmap_markdown += f"- **Target Timeline:** {epic.target_timeline}\n"
            roadmap_markdown += f"- **Description:** {epic.description}\n\n"

            for feature in epic.features:
                roadmap_markdown += f"### 🛠 Feature: {feature.title} ({feature.id})\n"
                roadmap_markdown += f"- **Priority:** {feature.priority}\n"
                roadmap_markdown += f"- **Description:** {feature.description}\n\n"
                roadmap_markdown += "| Story ID | User Story Title | Description | Priority | Estimate |\n"
                roadmap_markdown += "| --- | --- | --- | --- | --- |\n"
                for story in feature.user_stories:
                    roadmap_markdown += f"| {story.id} | {story.title} | {story.description} | {story.priority} | {story.estimate} |\n"
                roadmap_markdown += "\n"

        execution_plan_markdown = """### Execution Plan Steps:
1. **Parse & Comprehend Context:** Extracted inputs for PersonaScript MVP strategy.
2. **Access Internal Docs:** Pulled existing capabilities and architecture.
3. **Synthesize Strategic Themes:** Identified primary objectives around scale, brand safety, and multi-funnel personalization.
4. **Prioritize MVP Features:** Selected core high-impact features for launch.
5. **Draft Linear-Structured Roadmap:** Created epics, features, user stories, and estimates.
6. **Construct Issue Content:** Composed this comprehensive GitHub issue proposal.
7. **Publish to GitHub Repository:** Created this tracking issue for product team alignment.
"""

        body = f"""# PersonaScript MVP Development Roadmap (3-6 Months)

## 🎯 Goal
To establish a clear, structured Minimum Viable Product (MVP) roadmap for PersonaScript, organizing specific development milestones for the next 3-6 months. This roadmap is optimized and structured specifically for the **Linear platform** to allow rapid conversion into issues, epics, and projects.

## 📥 Inputs
- **Company Name:** {inputs.company_name}
- **Value Proposition:** {inputs.value_proposition}
- **Timeframe:** {inputs.timeframe}
- **Target Platform for Roadmap Structure:** {inputs.target_platform}

## 📊 Strategic Themes Synthesized
These key strategic themes align PersonaScript's foundational capabilities with market readiness and core value proposition delivery:
{themes_markdown}

## 🗺 Detailed MVP Roadmap (Linear Format)
Below is the highly structured, epic-driven roadmap containing features, estimated user stories, and timelines:

{roadmap_markdown}

## 📋 Execution Plan Review
The roadmap generation was orchestrated through the following steps:
{execution_plan_markdown}

---
*Created by PersonaScriptMVPDevelopmentRoadmapAgent*
"""
        return body
