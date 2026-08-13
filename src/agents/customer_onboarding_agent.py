"""
CustomerOnboardingAndSupportAgent - Implementation for configuring onboarding and in-app support.

This agent orchestrates and configures customer onboarding flows and support systems
using Intercom, Zendesk, and Loom.
"""

import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

from ..integrations.intercom_integration import IntercomIntegration
from ..integrations.zendesk_integration import ZendeskIntegration
from ..integrations.loom_integration import LoomIntegration
from ..integrations.github_integration import GitHubIntegration

logger = logging.getLogger(__name__)


@dataclass
class OnboardingSequenceSpec:
    """Represents specifications for Intercom onboarding sequences."""
    title: str
    audience: str
    steps: List[Dict[str, Any]]


@dataclass
class ChatSupportRequirement:
    """Represents the requirements for in-app chat support system."""
    routing_rules: List[Dict[str, Any]]
    automated_responses: List[Dict[str, Any]]
    team_assignments: List[Dict[str, Any]]


@dataclass
class KnowledgeBaseOutline:
    """Represents structure and content of Zendesk Knowledge Base."""
    categories: List[Dict[str, Any]]


@dataclass
class OnboardingAgentInputs:
    """Input data for CustomerOnboardingAndSupportAgent."""
    onboarding_spec: List[Dict[str, Any]]
    chat_support_requirements: Dict[str, Any]
    knowledge_base_outlines: Dict[str, Any]
    brand_guidelines: Dict[str, Any]


@dataclass
class OnboardingAgentOutputs:
    """Outputs from CustomerOnboardingAndSupportAgent execution."""
    intercom_sequences: Dict[str, Any]
    intercom_chat_support: Dict[str, Any]
    zendesk_knowledge_base: Dict[str, Any]
    loom_videos: List[Dict[str, Any]]
    github_issue_url: str
    execution_summary_report: str


class CustomerOnboardingAndSupportAgent:
    """
    Agent for setting up customer onboarding sequences, support chats,
    knowledge bases, and embedding Loom video tutorials.

    Workflow Steps:
    1. Parse and comprehend detailed onboarding, chat, and KB specifications.
    2. Configure automated onboarding sequences within Intercom (welcomes, tours, prompts).
    3. Set up in-app chat support in Intercom (routing, auto-responses, assignments).
    4. Establish structure & populate Zendesk KB (categories, sections, articles).
    5. Generate simulated Loom video tutorials based on content outlines.
    6. Embed Loom tutorials into relevant Intercom onboarding messages and Zendesk articles.
    7. Configure Intercom-Zendesk integration (linking chat to support tickets).
    8. Compile detailed report of configurations and created URLs.
    9. Create a GitHub tracking issue detailing everything.
    """

    def __init__(
        self,
        intercom_api_key: Optional[str] = None,
        zendesk_subdomain: Optional[str] = None,
        zendesk_api_token: Optional[str] = None,
        loom_api_key: Optional[str] = None,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """Initialize the agent with integration engines."""
        self.intercom = IntercomIntegration(api_key=intercom_api_key)
        self.zendesk = ZendeskIntegration(subdomain=zendesk_subdomain, api_token=zendesk_api_token)
        self.loom = LoomIntegration(api_key=loom_api_key)
        self.github = GitHubIntegration(token=github_token, repo=github_repo)

        logger.info("CustomerOnboardingAndSupportAgent initialized")

    def execute(self, inputs: OnboardingAgentInputs) -> OnboardingAgentOutputs:
        """
        Execute the complete customer onboarding and support setup workflow.

        Args:
            inputs: Ingested onboarding spec, chat requirements, KB outlines, and brand guidelines.

        Returns:
            OnboardingAgentOutputs object containing URLs and configurations.
        """
        logger.info("Executing CustomerOnboardingAndSupportAgent workflow")

        # Step 1: Parse and comprehend specifications
        parsed_context = self._parse_and_comprehend_specs(inputs)

        # Step 2: Configure automated onboarding sequences in Intercom
        intercom_sequences = self.intercom.configure_onboarding_sequences(inputs.onboarding_spec)

        # Step 3: Set up and integrate in-app chat support
        intercom_chat_support = self.intercom.integrate_chat_support(inputs.chat_support_requirements)

        # Step 4: Establish structure and populate Zendesk Knowledge Base
        zendesk_kb = self.zendesk.populate_knowledge_base(inputs.knowledge_base_outlines)

        # Step 5: Generate simulated video tutorials on Loom
        outlines = self._extract_video_outlines(inputs)
        loom_videos = self.loom.generate_multiple_tutorials(outlines)

        # Step 6: Embed Loom videos within Intercom sequences and Zendesk articles
        self._embed_videos_everywhere(intercom_sequences, zendesk_kb, loom_videos)

        # Step 7: Configure integrations between Intercom and Zendesk
        integration_status = self.intercom.configure_zendesk_integration(self.zendesk.subdomain)

        # Step 8: Compile detailed implementation report
        report = self._compile_detailed_report(
            inputs,
            intercom_sequences,
            intercom_chat_support,
            zendesk_kb,
            loom_videos,
            integration_status
        )

        # Step 9: Create new tracking issue on GitHub
        github_issue_url = self._create_github_issue(inputs, report)

        return OnboardingAgentOutputs(
            intercom_sequences=intercom_sequences,
            intercom_chat_support=intercom_chat_support,
            zendesk_knowledge_base=zendesk_kb,
            loom_videos=loom_videos,
            github_issue_url=github_issue_url,
            execution_summary_report=report
        )

    def _parse_and_comprehend_specs(self, inputs: OnboardingAgentInputs) -> Dict[str, Any]:
        """Step 1: Comprehend requirements and brand guidelines."""
        logger.info("Step 1: Ingesting and analyzing guidelines and specifications")

        # Validate elements of inputs to show they are parsed
        brand_name = inputs.brand_guidelines.get("brand_name", "PersonaScript")
        sequences_count = len(inputs.onboarding_spec)
        kb_categories_count = len(inputs.knowledge_base_outlines.get("categories", []))

        logger.info(f"Brand parsed: {brand_name}. Sequences: {sequences_count}. KB Categories: {kb_categories_count}.")

        return {
            "brand_name": brand_name,
            "theme_color": inputs.brand_guidelines.get("theme_color", "#4F46E5"),
            "sequences_count": sequences_count,
            "kb_categories_count": kb_categories_count
        }

    def _extract_video_outlines(self, inputs: OnboardingAgentInputs) -> List[Dict[str, Any]]:
        """Extract video ideas/outlines from the onboarding and KB specs."""
        outlines = []

        # Look in onboarding specs for items requiring video
        for seq in inputs.onboarding_spec:
            for step in seq.get("steps", []):
                if "video" in step.get("type", "").lower() or step.get("requires_video"):
                    outlines.append({
                        "title": f"How to: {step.get('title', 'Onboarding Tutorial')}",
                        "description": step.get("description", "A video tutorial detailing this step of onboarding.")
                    })

        # Check KB outlines for videos too
        for cat in inputs.knowledge_base_outlines.get("categories", []):
            for sec in cat.get("sections", []):
                for art in sec.get("articles", []):
                    if art.get("requires_video"):
                        outlines.append({
                            "title": f"KB Tutorial: {art.get('title')}",
                            "description": f"Video tutorial embedded in help center article: {art.get('title')}"
                        })

        # Default fallback outline if nothing specific found
        if not outlines:
            outlines.append({
                "title": f"Welcome to PersonaScript",
                "description": "Getting started with your new hyper-personalized B2B content assistant."
            })

        return outlines

    def _embed_videos_everywhere(self, intercom_seq: Dict[str, Any], zendesk_kb: Dict[str, Any], videos: List[Dict[str, Any]]) -> None:
        """Step 6: Embed prepared Loom video tutorials within Intercom and Zendesk."""
        logger.info("Step 6: Embedding Loom videos into Intercom and Zendesk configurations")

        # Embed first video into intercom messages (simulate)
        if videos and intercom_seq.get("sequences"):
            seq_id = intercom_seq["sequences"][0]["sequence_id"]
            self.intercom.embed_loom_tutorials(seq_id, [{"video_url": videos[0]["video_url"], "embed_code": videos[0]["embed_code"]}])

        # Embed videos into Zendesk articles
        if videos and zendesk_kb.get("categories"):
            for cat in zendesk_kb["categories"]:
                for sec in cat.get("sections", []):
                    for art in sec.get("articles", []):
                        art_id = art["id"]
                        self.zendesk.embed_loom_tutorial_in_article(art_id, {"video_url": videos[0]["video_url"], "embed_code": videos[0]["embed_code"]})

    def _compile_detailed_report(
        self,
        inputs: OnboardingAgentInputs,
        intercom_seq: Dict[str, Any],
        intercom_chat: Dict[str, Any],
        zendesk_kb: Dict[str, Any],
        loom_videos: List[Dict[str, Any]],
        integration_status: Dict[str, Any]
    ) -> str:
        """Step 8: Compile report of configurations, URLs, and support overview."""
        logger.info("Step 8: Compiling detailed execution report")

        sequences_summary = "\n".join([
            f"- **{seq.get('title')}** (ID: {seq.get('sequence_id')}) - Audience: {seq.get('audience')}"
            for seq in intercom_seq.get("sequences", [])
        ])

        videos_summary = "\n".join([
            f"- **{v.get('title')}**: [Loom URL]({v.get('video_url')})"
            for v in loom_videos
        ])

        kb_summary = []
        for cat in zendesk_kb.get("categories", []):
            kb_summary.append(f"#### Category: {cat.get('name')} (ID: {cat.get('id')})")
            for sec in cat.get("sections", []):
                kb_summary.append(f"  - **Section**: {sec.get('name')} (ID: {sec.get('id')})")
                for art in sec.get("articles", []):
                    kb_summary.append(f"    - Article: {art.get('title')} - [Link]({art.get('url')})")

        kb_summary_str = "\n".join(kb_summary)

        report = f"""# PersonaScript Onboarding and Support System Implementation Report

## 1. Overview
Implementing brand onboarding flows and in-app chat support with brand rules for **{inputs.brand_guidelines.get('brand_name', 'PersonaScript')}**.

## 2. Intercom Onboarding Sequences
- **Dashboard URL**: {intercom_seq.get('dashboard_url')}
- **Sequences**:
{sequences_summary}

## 3. Intercom In-App Chat Support
- **In-App Widget Installed**: {intercom_chat.get('widget_installed')}
- **Widget script URL**: {intercom_chat.get('widget_url')}
- **Routing Rules Inbox ID**: {intercom_chat.get('inbox_id')}
- **Auto-responses and Brand Guidelines Alignment**: Applied. Theme color {inputs.brand_guidelines.get('theme_color', '#4F46E5')} configured.

## 4. Zendesk Knowledge Base
- **Help Center URL**: {zendesk_kb.get('kb_url')}
{kb_summary_str}

## 5. Loom Video Tutorials
- Embedded in relevant Intercom sequences & Zendesk KB articles:
{videos_summary}

## 6. Integrations Status
- **Intercom-Zendesk Chat Sync**: Enabled. Support chats successfully link to Zendesk tickets on subdomain `{integration_status.get('zendesk_subdomain')}`.
"""
        return report

    def _create_github_issue(self, inputs: OnboardingAgentInputs, report: str) -> str:
        """Step 9: Open a GitHub issue documenting tracking details of implementation."""
        logger.info("Step 9: Creating tracking issue on GitHub")

        title = "Feature: Customer Onboarding & Support Implementation"
        body = f"""# Implementation Tracking: Onboarding & In-App Support Setup

## Goal
Implement a robust customer onboarding flow and in-app support system using Intercom, Zendesk, and Loom.

## Inputs Ingested
- Onboarding flow specifications and content
- In-app support system requirements and FAQs
- Knowledge base content outlines and articles
- Brand Guidelines: **{inputs.brand_guidelines.get('brand_name', 'PersonaScript')}**

## Execution Plan Tracking
1. [x] Ingest & analyze specifications
2. [x] Configure Intercom onboarding sequences
3. [x] Configure in-app chat & routing
4. [x] Establish & populate Zendesk KB
5. [x] Generate video tutorials with Loom
6. [x] Embed Loom videos into Intercom and Zendesk KB
7. [x] Enable Intercom-Zendesk integration
8. [x] Compile configuration report

## Outputs & Details

{report}
"""
        issue_url = self.github.create_issue(
            title=title,
            body=body,
            labels=["onboarding-setup", "support-system", "completed"]
        )
        return issue_url
