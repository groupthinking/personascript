"""
CustomerOnboardingAndSupportAgent - Main agent for orchestrating and configuring
customer onboarding flows, in-app support, and knowledge base systems using Intercom, Zendesk, and Loom.

Execution Plan:
1. Parse and comprehend detailed specifications for onboarding, support, and KB content.
2. Design & configure automated onboarding sequences within Intercom.
3. Set up and integrate in-app chat support using Intercom.
4. Establish structure and populate knowledge base within Zendesk.
5. Generate/simulate Loom video tutorials based on content outlines.
6. Embed Loom video tutorials into Intercom messages and Zendesk articles.
7. Configure integrations between Intercom and Zendesk.
8. Compile detailed implementation report.
9. Create a comprehensive GitHub issue detailing the implementation.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timezone

from ..integrations.intercom_integration import IntercomIntegration
from ..integrations.zendesk_integration import ZendeskIntegration
from ..integrations.loom_integration import LoomIntegration
from ..integrations.github_integration import GitHubIntegration

logger = logging.getLogger(__name__)


@dataclass
class OnboardingSequenceSpec:
    """Specification for an onboarding sequence."""
    title: str
    target_audience: str
    steps: List[Dict[str, Any]]


@dataclass
class InAppSupportSpec:
    """Specification for in-app chat support."""
    routing_rules: List[Dict[str, Any]]
    automated_responses: List[Dict[str, Any]]
    team_assignments: List[Dict[str, Any]]


@dataclass
class KnowledgeBaseArticleSpec:
    """Specification for a knowledge base article and associated video outline."""
    category_name: str
    section_name: str
    article_title: str
    article_body: str
    video_outline: Optional[Dict[str, Any]] = None


@dataclass
class BrandGuidelines:
    """PersonaScript brand guidelines."""
    brand_name: str = "PersonaScript"
    primary_color: str = "#4F46E5"
    tone_of_voice: str = "Professional, helpful, and empowering"
    logo_url: str = "https://personascript.com/logo.png"


@dataclass
class AgentInputs:
    """Inputs for the CustomerOnboardingAndSupportAgent."""
    onboarding_specs: List[OnboardingSequenceSpec]
    support_spec: InAppSupportSpec
    kb_article_specs: List[KnowledgeBaseArticleSpec]
    brand_guidelines: Optional[BrandGuidelines] = None


@dataclass
class OnboardingSequenceOutput:
    """Output details of configured Intercom onboarding sequence."""
    sequence_id: str
    title: str
    url: str
    target_audience: str
    steps: List[Dict[str, Any]]
    status: str = "active"


@dataclass
class SupportChatOutput:
    """Output details of configured Intercom in-app chat support."""
    config_id: str
    app_id: str
    routing_rules: List[Dict[str, Any]]
    automated_responses: List[Dict[str, Any]]
    team_assignments: List[Dict[str, Any]]
    status: str = "enabled"


@dataclass
class KnowledgeBaseArticleOutput:
    """Output details of populated Zendesk knowledge base article."""
    article_id: int
    category_name: str
    section_name: str
    title: str
    body: str
    url: str
    embedded_video_url: Optional[str] = None


@dataclass
class LoomVideoOutput:
    """Output details of generated/embedded Loom video tutorial."""
    video_id: str
    title: str
    description: str
    duration_seconds: int
    share_url: str
    embed_url: str
    embed_html: str


@dataclass
class IntegrationConfigOutput:
    """Output details of Intercom and Zendesk integration setup."""
    intercom_zendesk_link_id: str
    zendesk_intercom_link_id: str
    sync_tickets: bool
    status: str


@dataclass
class ImplementationReport:
    """Detailed summary report of the onboarding and support system setup."""
    summary: str
    onboarding_sequences_count: int
    kb_articles_count: int
    loom_videos_count: int
    integration_status: str
    detailed_overview: str


@dataclass
class AgentOutputs:
    """Outputs from the CustomerOnboardingAndSupportAgent."""
    onboarding_sequences: List[OnboardingSequenceOutput]
    support_chat_config: Optional[SupportChatOutput]
    knowledge_base_articles: List[KnowledgeBaseArticleOutput]
    loom_videos: List[LoomVideoOutput]
    integration_config: Optional[IntegrationConfigOutput]
    implementation_report: Optional[ImplementationReport]
    github_issue_url: str
    status: str = "success"
    error_message: Optional[str] = None


class CustomerOnboardingAndSupportAgent:
    """
    Main agent class for implementing onboarding flows and in-app support systems
    using Intercom, Zendesk, and Loom integrations.
    """

    def __init__(
        self,
        intercom_api_key: Optional[str] = None,
        intercom_app_id: Optional[str] = None,
        zendesk_subdomain: Optional[str] = None,
        zendesk_email: Optional[str] = None,
        zendesk_api_token: Optional[str] = None,
        loom_api_key: Optional[str] = None,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """Initialize CustomerOnboardingAndSupportAgent with integrations."""
        self.intercom = IntercomIntegration(api_key=intercom_api_key, app_id=intercom_app_id)
        self.zendesk = ZendeskIntegration(
            subdomain=zendesk_subdomain, email=zendesk_email, api_token=zendesk_api_token
        )
        self.loom = LoomIntegration(api_key=loom_api_key)
        self.github = GitHubIntegration(token=github_token, repo=github_repo)

        self.execution_log: List[Dict[str, Any]] = []
        logger.info("CustomerOnboardingAndSupportAgent initialized")

    def _log_step(self, step_number: int, description: str, status: str = "started", data: Optional[Dict] = None):
        """Log execution step."""
        log_entry = {
            "step": step_number,
            "description": description,
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data or {}
        }
        self.execution_log.append(log_entry)
        logger.info(f"Step {step_number}: {description} - {status}")

    def execute(self, inputs: AgentInputs) -> AgentOutputs:
        """
        Execute complete 9-step customer onboarding and support system setup.

        Args:
            inputs: AgentInputs containing onboarding specs, support specs, KB specs, brand guidelines.

        Returns:
            AgentOutputs containing sequence models, KB outputs, video metadata, and GitHub issue URL.
        """
        logger.info("Starting CustomerOnboardingAndSupportAgent execution")
        self.execution_log = []

        try:
            brand = inputs.brand_guidelines or BrandGuidelines()

            # Step 1: Parse and comprehend specifications
            self._log_step(1, "Parse and comprehend specifications")
            parsed_summary = self._parse_specifications(inputs, brand)
            self._log_step(1, "Parse and comprehend specifications", "completed", parsed_summary)

            # Step 2: Design and configure automated onboarding sequences in Intercom
            self._log_step(2, "Configure Intercom onboarding sequences")
            configured_sequences = self._configure_onboarding_sequences(inputs.onboarding_specs)
            self._log_step(2, "Configure Intercom onboarding sequences", "completed", {
                "sequence_count": len(configured_sequences)
            })

            # Step 3: Set up and integrate in-app chat support using Intercom
            self._log_step(3, "Set up and integrate Intercom in-app chat support")
            chat_config = self._configure_in_app_chat(inputs.support_spec)
            self._log_step(3, "Set up and integrate Intercom in-app chat support", "completed")

            # Step 4: Establish structure and populate Zendesk Knowledge Base
            self._log_step(4, "Establish structure and populate Zendesk Knowledge Base")
            kb_articles_raw, category_map, section_map = self._populate_knowledge_base(inputs.kb_article_specs)
            self._log_step(4, "Establish structure and populate Zendesk Knowledge Base", "completed", {
                "categories": len(category_map), "articles": len(kb_articles_raw)
            })

            # Step 5: Generate Loom video tutorials based on content outlines
            self._log_step(5, "Generate Loom video tutorials")
            loom_videos = self._generate_loom_videos(inputs.kb_article_specs)
            self._log_step(5, "Generate Loom video tutorials", "completed", {
                "videos_created": len(loom_videos)
            })

            # Step 6: Embed Loom video tutorials into Intercom messages and Zendesk articles
            self._log_step(6, "Embed Loom video tutorials into Intercom sequences and Zendesk KB")
            final_sequences, final_kb_articles = self._embed_loom_videos(
                configured_sequences, kb_articles_raw, loom_videos
            )
            self._log_step(6, "Embed Loom video tutorials into Intercom sequences and Zendesk KB", "completed")

            # Step 7: Configure integrations between Intercom and Zendesk
            self._log_step(7, "Configure Intercom and Zendesk integration")
            integration_config = self._configure_intercom_zendesk_integration()
            self._log_step(7, "Configure Intercom and Zendesk integration", "completed")

            # Step 8: Compile a detailed report of the implementation
            self._log_step(8, "Compile detailed implementation report")
            implementation_report = self._compile_implementation_report(
                final_sequences, chat_config, final_kb_articles, loom_videos, integration_config, brand
            )
            self._log_step(8, "Compile detailed implementation report", "completed")

            # Step 9: Create GitHub issue detailing implementation
            self._log_step(9, "Create GitHub issue detailing implementation")
            github_issue_url = self._create_github_issue(
                inputs, final_sequences, chat_config, final_kb_articles, loom_videos, integration_config, implementation_report
            )
            self._log_step(9, "Create GitHub issue detailing implementation", "completed", {
                "issue_url": github_issue_url
            })

            logger.info("CustomerOnboardingAndSupportAgent execution completed successfully")
            return AgentOutputs(
                onboarding_sequences=final_sequences,
                support_chat_config=chat_config,
                knowledge_base_articles=final_kb_articles,
                loom_videos=loom_videos,
                integration_config=integration_config,
                implementation_report=implementation_report,
                github_issue_url=github_issue_url,
                status="success"
            )

        except Exception as e:
            logger.error("Error during CustomerOnboardingAndSupportAgent execution", exc_info=True)
            return AgentOutputs(
                onboarding_sequences=[],
                support_chat_config=None,
                knowledge_base_articles=[],
                loom_videos=[],
                integration_config=None,
                implementation_report=None,
                github_issue_url="",
                status="error",
                error_message=str(e)
            )

    def _parse_specifications(self, inputs: AgentInputs, brand: BrandGuidelines) -> Dict[str, Any]:
        """Step 1: Parse and validate input specifications."""
        return {
            "onboarding_sequence_count": len(inputs.onboarding_specs),
            "kb_article_count": len(inputs.kb_article_specs),
            "routing_rules_count": len(inputs.support_spec.routing_rules),
            "automated_responses_count": len(inputs.support_spec.automated_responses),
            "brand_name": brand.brand_name
        }

    def _configure_onboarding_sequences(
        self,
        onboarding_specs: List[OnboardingSequenceSpec]
    ) -> List[OnboardingSequenceOutput]:
        """Step 2: Configure Intercom onboarding sequences."""
        outputs = []
        for spec in onboarding_specs:
            res = self.intercom.create_onboarding_sequence(
                title=spec.title,
                steps=spec.steps,
                target_audience=spec.target_audience
            )
            outputs.append(OnboardingSequenceOutput(
                sequence_id=res["sequence_id"],
                title=res["title"],
                url=res["url"],
                target_audience=res["target_audience"],
                steps=res["steps"],
                status=res["status"]
            ))
        return outputs

    def _configure_in_app_chat(self, support_spec: InAppSupportSpec) -> SupportChatOutput:
        """Step 3: Set up and integrate in-app chat support via Intercom."""
        res = self.intercom.configure_in_app_chat(
            routing_rules=support_spec.routing_rules,
            automated_responses=support_spec.automated_responses,
            team_assignments=support_spec.team_assignments
        )
        return SupportChatOutput(
            config_id=res["config_id"],
            app_id=res["app_id"],
            routing_rules=res["routing_rules"],
            automated_responses=res["automated_responses"],
            team_assignments=res["team_assignments"],
            status=res["status"]
        )

    def _populate_knowledge_base(
        self,
        kb_article_specs: List[KnowledgeBaseArticleSpec]
    ) -> tuple[List[KnowledgeBaseArticleOutput], Dict[str, int], Dict[str, int]]:
        """Step 4: Establish structure (categories/sections) and populate Zendesk KB."""
        category_map: Dict[str, int] = {}
        section_map: Dict[str, int] = {}
        articles: List[KnowledgeBaseArticleOutput] = []

        for spec in kb_article_specs:
            # Ensure category exists
            if spec.category_name not in category_map:
                cat_res = self.zendesk.create_category(
                    name=spec.category_name,
                    description=f"Knowledge base articles for {spec.category_name}"
                )
                category_map[spec.category_name] = cat_res["category_id"]

            cat_id = category_map[spec.category_name]

            # Ensure section exists
            sec_key = f"{spec.category_name}::{spec.section_name}"
            if sec_key not in section_map:
                sec_res = self.zendesk.create_section(
                    category_id=cat_id,
                    name=spec.section_name,
                    description=f"Section {spec.section_name} under {spec.category_name}"
                )
                section_map[sec_key] = sec_res["section_id"]

            sec_id = section_map[sec_key]

            # Create article
            art_res = self.zendesk.create_article(
                section_id=sec_id,
                title=spec.article_title,
                body=spec.article_body
            )

            articles.append(KnowledgeBaseArticleOutput(
                article_id=art_res["article_id"],
                category_name=spec.category_name,
                section_name=spec.section_name,
                title=art_res["title"],
                body=art_res["body"],
                url=art_res["url"]
            ))

        return articles, category_map, section_map

    def _generate_loom_videos(self, kb_article_specs: List[KnowledgeBaseArticleSpec]) -> List[LoomVideoOutput]:
        """Step 5: Generate Loom video tutorials based on content outlines."""
        videos = []
        for spec in kb_article_specs:
            if spec.video_outline:
                title = spec.video_outline.get("title", f"Tutorial: {spec.article_title}")
                desc = spec.video_outline.get("description", f"Walkthrough for {spec.article_title}")
                duration = spec.video_outline.get("duration_seconds", 120)

                res = self.loom.create_video_tutorial(
                    title=title,
                    description=desc,
                    duration_seconds=duration,
                    tags=["onboarding", spec.category_name.lower().replace(" ", "-")]
                )
                videos.append(LoomVideoOutput(
                    video_id=res["video_id"],
                    title=res["title"],
                    description=res["description"],
                    duration_seconds=res["duration_seconds"],
                    share_url=res["share_url"],
                    embed_url=res["embed_url"],
                    embed_html=res["embed_html"]
                ))
        return videos

    def _embed_loom_videos(
        self,
        sequences: List[OnboardingSequenceOutput],
        articles: List[KnowledgeBaseArticleOutput],
        videos: List[LoomVideoOutput]
    ) -> tuple[List[OnboardingSequenceOutput], List[KnowledgeBaseArticleOutput]]:
        """Step 6: Embed Loom videos into Intercom sequence steps and Zendesk KB articles."""
        video_map = {v.title.lower(): v for v in videos}

        # Embed into Zendesk Articles
        updated_articles = []
        for art in articles:
            # Match video by title similarity or index or key words
            matched_video = None
            art_words = [w for w in art.title.lower().split() if len(w) > 3]
            for v_title, v_obj in video_map.items():
                if art.title.lower() in v_title or v_title in art.title.lower() or any(w in v_title for w in art_words):
                    matched_video = v_obj
                    break

            if matched_video:
                embed_res = self.zendesk.embed_video_in_article(
                    article_id=art.article_id,
                    video_url=matched_video.embed_url,
                    video_title=matched_video.title
                )
                embed_code = f'\n\n<div class="loom-embed"><iframe src="{matched_video.embed_url}" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="width: 100%; height: 400px;"></iframe></div>'
                art.body += embed_code
                art.embedded_video_url = matched_video.embed_url

            updated_articles.append(art)

        # Embed into Intercom Sequences
        updated_sequences = []
        for seq in sequences:
            for step in seq.steps:
                step_title = step.get("title", "").lower()
                matched_video = None
                for v_title, v_obj in video_map.items():
                    if step_title and (step_title in v_title or v_title in step_title):
                        matched_video = v_obj
                        break
                if matched_video:
                    self.intercom.embed_video_in_sequence(
                        sequence_id=seq.sequence_id,
                        step_id=step.get("step_id", "step_1"),
                        video_url=matched_video.embed_url,
                        video_title=matched_video.title
                    )
                    step["embedded_video_url"] = matched_video.embed_url

            updated_sequences.append(seq)

        return updated_sequences, updated_articles

    def _configure_intercom_zendesk_integration(self) -> IntegrationConfigOutput:
        """Step 7: Configure sync and routing between Intercom and Zendesk."""
        intercom_res = self.intercom.configure_zendesk_integration(
            zendesk_subdomain=self.zendesk.subdomain,
            sync_tickets=True
        )
        zendesk_res = self.zendesk.configure_intercom_integration(
            intercom_app_id=self.intercom.app_id
        )

        return IntegrationConfigOutput(
            intercom_zendesk_link_id=intercom_res["integration_id"],
            zendesk_intercom_link_id=zendesk_res["integration_id"],
            sync_tickets=True,
            status="active"
        )

    def _compile_implementation_report(
        self,
        sequences: List[OnboardingSequenceOutput],
        chat_config: SupportChatOutput,
        articles: List[KnowledgeBaseArticleOutput],
        videos: List[LoomVideoOutput],
        integration_config: IntegrationConfigOutput,
        brand: BrandGuidelines
    ) -> ImplementationReport:
        """Step 8: Compile detailed report of implementation."""
        overview = (
            f"Successfully configured complete customer onboarding flow and support system for {brand.brand_name}.\n\n"
            f"1. **Intercom Onboarding Sequences**: Created {len(sequences)} sequence(s) targeting new user signups.\n"
            f"2. **Intercom In-App Chat**: Configured routing rules ({len(chat_config.routing_rules)} rules) "
            f"and automated response flows ({len(chat_config.automated_responses)} bots).\n"
            f"3. **Zendesk Knowledge Base**: Structure established with {len(articles)} published KB articles.\n"
            f"4. **Loom Video Tutorials**: Generated {len(videos)} video walkthrough(s) embedded into Intercom messages & Zendesk KB.\n"
            f"5. **Intercom-Zendesk Integration**: Active synchronization configured between Intercom chat and Zendesk support ticketing."
        )

        return ImplementationReport(
            summary=f"Implementation complete: {len(sequences)} Intercom sequence(s), {len(articles)} Zendesk KB article(s), {len(videos)} Loom video(s).",
            onboarding_sequences_count=len(sequences),
            kb_articles_count=len(articles),
            loom_videos_count=len(videos),
            integration_status=integration_config.status,
            detailed_overview=overview
        )

    def _create_github_issue(
        self,
        inputs: AgentInputs,
        sequences: List[OnboardingSequenceOutput],
        chat_config: SupportChatOutput,
        articles: List[KnowledgeBaseArticleOutput],
        videos: List[LoomVideoOutput],
        integration_config: IntegrationConfigOutput,
        report: ImplementationReport
    ) -> str:
        """Step 9: Create comprehensive GitHub tracking issue."""
        title = "Customer Onboarding Flow & Support System Implementation"

        # Format sequence details
        seq_md = []
        for seq in sequences:
            seq_md.append(f"- [{seq.title}]({seq.url}) - Target: {seq.target_audience} ({len(seq.steps)} steps)")
        seq_str = "\n".join(seq_md) or "- No sequences configured"

        # Format KB details
        kb_md = []
        for art in articles:
            video_note = f" (Includes Loom Video: {art.embedded_video_url})" if art.embedded_video_url else ""
            kb_md.append(f"- [{art.category_name} > {art.section_name} > {art.title}]({art.url}){video_note}")
        kb_str = "\n".join(kb_md) or "- No KB articles published"

        # Format Loom details
        loom_md = []
        for vid in videos:
            loom_md.append(f"- [{vid.title}]({vid.share_url}) ({vid.duration_seconds}s) - Embed: {vid.embed_url}")
        loom_str = "\n".join(loom_md) or "- No Loom videos generated"

        body = f"""# Customer Onboarding Flow & In-App Support System Implementation

## Goal
To implement a robust customer onboarding flow and in-app support system using Intercom, Zendesk, and Loom.

## Implementation Overview
{report.detailed_overview}

## 🚀 Configured Intercom Onboarding Sequences
{seq_str}

## 💬 Intercom In-App Support & Routing
- **Config ID**: `{chat_config.config_id}`
- **App ID**: `{chat_config.app_id}`
- **Routing Rules**: {len(chat_config.routing_rules)} configured
- **Automated Response Bots**: {len(chat_config.automated_responses)} configured
- **Team Assignments**: {len(chat_config.team_assignments)} teams assigned

## 📚 Zendesk Knowledge Base Articles
{kb_str}

## 🎥 Loom Video Tutorials Embedded
{loom_str}

## 🔗 Integration Setup
- **Intercom -> Zendesk Integration**: ID `{integration_config.intercom_zendesk_link_id}` (Status: {integration_config.status})
- **Zendesk -> Intercom Integration**: ID `{integration_config.zendesk_intercom_link_id}` (Status: {integration_config.status})
- **Ticket Sync**: Enabled

---
*Report generated automatically by CustomerOnboardingAndSupportAgent on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC.*
"""
        issue_url = self.github.create_issue(
            title=title,
            body=body,
            labels=["onboarding", "support", "intercom", "zendesk", "loom"]
        )
        return issue_url
