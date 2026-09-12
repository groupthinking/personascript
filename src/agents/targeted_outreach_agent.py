"""
PersonaScript TargetedOutreachAgent - Agent for initiating targeted outbound sales efforts
and launching focused LinkedIn ad campaigns.

This agent follows a 10-step execution plan:
1. Parse and understand PersonaScript's Ideal Customer Profile (ICP) details and campaign objectives.
2. Utilize Apollo.io API to search for target companies and individuals matching ICP (10-15 leads).
3. Extract relevant contact information into a structured qualified lead list.
4. Prepare personalized outbound sales message drafts using templates and lead info.
5. Configure a new LinkedIn Ad campaign using LinkedIn Ads API.
6. Upload provided ad creatives (images, videos) and associated ad copy into campaign.
7. Launch the configured LinkedIn Ad campaign.
8. Retrieve initial performance metrics for the launched LinkedIn Ad campaign.
9. Compile all generated deliverables into a comprehensive summary report.
10. Create a detailed GitHub issue summarizing task execution, inputs, outputs, and URLs.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timezone

from ..integrations.apollo_integration import ApolloIntegration
from ..integrations.linkedin_integration import LinkedInIntegration
from ..integrations.github_integration import GitHubIntegration

logger = logging.getLogger(__name__)


@dataclass
class ICPDetails:
    """Ideal Customer Profile details for targeted outreach."""
    industry: str = "B2B SaaS"
    company_size_range: str = "50-200"
    target_job_titles: List[str] = field(default_factory=lambda: [
        "VP of Demand Generation",
        "Head of Growth Marketing",
        "Director of Content Marketing",
        "Chief Marketing Officer"
    ])
    target_locations: List[str] = field(default_factory=lambda: ["United States", "Canada"])


@dataclass
class CampaignConfig:
    """LinkedIn Ad campaign parameters."""
    campaign_name: str = "PersonaScript B2B SaaS Launch Campaign"
    daily_budget: float = 250.00
    objective: str = "LEAD_GENERATION"
    ad_format: str = "SPONSORED_UPDATES"


@dataclass
class AdCreative:
    """Ad creative asset details."""
    headline: str
    ad_copy: str
    media_url: Optional[str] = None
    destination_url: Optional[str] = None


@dataclass
class Lead:
    """Qualified prospect lead details."""
    id: str
    name: str
    title: str
    company: str
    email: str
    linkedin_url: str
    industry: str
    company_size: str
    location: str


@dataclass
class PersonalizedMessage:
    """Drafted outbound sales message for a prospect."""
    lead_id: str
    lead_name: str
    lead_company: str
    lead_email: str
    subject: str
    body: str


@dataclass
class AdPerformanceMetrics:
    """Performance metrics for LinkedIn Ad campaign."""
    campaign_id: str
    impressions: int
    clicks: int
    spend: float
    currency: str
    ctr_percent: float
    cpc: float
    conversions: int
    cost_per_conversion: float
    dashboard_url: str


@dataclass
class AgentInputs:
    """Inputs for the TargetedOutreachAgent."""
    icp_details: ICPDetails
    campaign_config: CampaignConfig
    ad_creatives: List[AdCreative]
    outbound_templates: List[Dict[str, str]] = field(default_factory=lambda: [
        {
            "subject": "Scaling {{company}}'s B2B content velocity with AI",
            "body": "Hi {{first_name}},\n\nNotice you lead {{title}} at {{company}}. PersonaScript helps growth-stage B2B SaaS teams automatically generate brand-aligned, hyper-personalized marketing copy.\n\nWould you be open to a 10-min intro call next week?\n\nBest,\nPersonaScript Team"
        }
    ])
    target_lead_count: int = 12


@dataclass
class AgentOutputs:
    """Outputs from the TargetedOutreachAgent."""
    qualified_leads: List[Lead]
    personalized_messages: List[PersonalizedMessage]
    campaign_id: str
    campaign_dashboard_url: str
    ad_performance: AdPerformanceMetrics
    summary_report: str
    github_issue_url: str
    status: str = "success"
    error_message: Optional[str] = None


class TargetedOutreachAgent:
    """
    Main agent class for executing targeted outbound sales prospecting
    and managing LinkedIn Ad campaigns.
    """

    def __init__(
        self,
        apollo_api_key: Optional[str] = None,
        linkedin_access_token: Optional[str] = None,
        linkedin_account_id: Optional[str] = None,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """Initialize TargetedOutreachAgent with external integrations."""
        self.apollo = ApolloIntegration(api_key=apollo_api_key)
        self.linkedin = LinkedInIntegration(
            access_token=linkedin_access_token,
            account_id=linkedin_account_id
        )
        self.github = GitHubIntegration(token=github_token, repo=github_repo)
        self.execution_log: List[Dict[str, Any]] = []
        logger.info("TargetedOutreachAgent initialized")

    def _log_step(self, step_number: int, description: str, status: str = "started", data: Optional[Dict] = None):
        """Log workflow step execution."""
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
        Execute the 10-step outbound sales and LinkedIn ads workflow.

        Args:
            inputs: AgentInputs containing ICP, campaign config, ad creatives, and messaging templates.

        Returns:
            AgentOutputs containing qualified leads, personalized messages, ad metrics, and GitHub URL.
        """
        logger.info("Starting TargetedOutreachAgent execution")
        self.execution_log = []

        try:
            # Step 1: Parse and understand PersonaScript ICP details and campaign objectives
            self._log_step(1, "Parse ICP details and campaign objectives")
            parsed_icp = self._parse_icp(inputs.icp_details, inputs.campaign_config)
            self._log_step(1, "Parse ICP details and campaign objectives", "completed", parsed_icp)

            # Step 2: Utilize Apollo.io API to search for target companies and individuals
            self._log_step(2, "Search for target prospects using Apollo.io API")
            prospect_raw_data = self.apollo.search_people(
                titles=inputs.icp_details.target_job_titles,
                industry=inputs.icp_details.industry,
                company_size_range=inputs.icp_details.company_size_range,
                location=inputs.icp_details.target_locations[0] if inputs.icp_details.target_locations else "United States",
                count=inputs.target_lead_count
            )
            self._log_step(2, "Search for target prospects using Apollo.io API", "completed", {
                "leads_found": len(prospect_raw_data)
            })

            # Step 3: Extract contact information into structured Lead list
            self._log_step(3, "Extract contact information into qualified lead list")
            leads = self._extract_leads(prospect_raw_data)
            self._log_step(3, "Extract contact information into qualified lead list", "completed", {
                "qualified_leads_count": len(leads)
            })

            # Step 4: Prepare personalized outbound sales message drafts
            self._log_step(4, "Prepare personalized outbound sales message drafts")
            personalized_messages = self._draft_personalized_messages(leads, inputs.outbound_templates)
            self._log_step(4, "Prepare personalized outbound sales message drafts", "completed", {
                "drafts_count": len(personalized_messages)
            })

            # Step 5: Configure new LinkedIn Ad campaign using LinkedIn Ads API
            self._log_step(5, "Configure new LinkedIn Ad campaign")
            target_audience = {
                "industry": inputs.icp_details.industry,
                "company_size": inputs.icp_details.company_size_range,
                "job_titles": inputs.icp_details.target_job_titles
            }
            campaign_result = self.linkedin.create_campaign(
                name=inputs.campaign_config.campaign_name,
                objective=inputs.campaign_config.objective,
                daily_budget=inputs.campaign_config.daily_budget,
                target_audience=target_audience,
                format_type=inputs.campaign_config.ad_format
            )
            campaign_id = campaign_result["campaign_id"]
            self._log_step(5, "Configure new LinkedIn Ad campaign", "completed", {"campaign_id": campaign_id})

            # Step 6: Upload provided ad creatives into configured campaign
            self._log_step(6, "Upload ad creatives and copy into LinkedIn campaign")
            creatives_uploaded = []
            for creative in inputs.ad_creatives:
                up_res = self.linkedin.upload_ad_creative(
                    campaign_id=campaign_id,
                    headline=creative.headline,
                    ad_copy=creative.ad_copy,
                    media_url=creative.media_url,
                    destination_url=creative.destination_url
                )
                creatives_uploaded.append(up_res)
            self._log_step(6, "Upload ad creatives and copy into LinkedIn campaign", "completed", {
                "creatives_count": len(creatives_uploaded)
            })

            # Step 7: Launch the configured LinkedIn Ad campaign
            self._log_step(7, "Launch LinkedIn Ad campaign")
            launch_res = self.linkedin.launch_campaign(campaign_id)
            self._log_step(7, "Launch LinkedIn Ad campaign", "completed", launch_res)

            # Step 8: Retrieve initial performance metrics for LinkedIn Ad campaign
            self._log_step(8, "Retrieve initial campaign performance metrics")
            metrics_data = self.linkedin.get_campaign_performance(campaign_id)
            ad_metrics = AdPerformanceMetrics(
                campaign_id=metrics_data["campaign_id"],
                impressions=metrics_data["impressions"],
                clicks=metrics_data["clicks"],
                spend=metrics_data["spend"],
                currency=metrics_data.get("currency", "USD"),
                ctr_percent=metrics_data["ctr_percent"],
                cpc=metrics_data["cpc"],
                conversions=metrics_data.get("conversions", 0),
                cost_per_conversion=metrics_data.get("cost_per_conversion", 0.0),
                dashboard_url=metrics_data["dashboard_url"]
            )
            self._log_step(8, "Retrieve initial campaign performance metrics", "completed", {
                "impressions": ad_metrics.impressions,
                "clicks": ad_metrics.clicks,
                "spend": ad_metrics.spend
            })

            # Step 9: Compile comprehensive summary report
            self._log_step(9, "Compile comprehensive summary report")
            summary_report = self._compile_summary_report(
                inputs, leads, personalized_messages, campaign_result, ad_metrics
            )
            self._log_step(9, "Compile comprehensive summary report", "completed")

            # Step 10: Create detailed GitHub issue
            self._log_step(10, "Create comprehensive GitHub issue summarizing execution")
            github_issue_url = self._create_github_issue(
                inputs, leads, personalized_messages, campaign_result, ad_metrics, summary_report
            )
            self._log_step(10, "Create comprehensive GitHub issue summarizing execution", "completed", {
                "github_url": github_issue_url
            })

            logger.info("TargetedOutreachAgent execution completed successfully")
            return AgentOutputs(
                qualified_leads=leads,
                personalized_messages=personalized_messages,
                campaign_id=campaign_id,
                campaign_dashboard_url=ad_metrics.dashboard_url,
                ad_performance=ad_metrics,
                summary_report=summary_report,
                github_issue_url=github_issue_url,
                status="success"
            )

        except Exception as e:
            logger.error(f"Error executing TargetedOutreachAgent: {e}", exc_info=True)
            empty_metrics = AdPerformanceMetrics(
                campaign_id="",
                impressions=0,
                clicks=0,
                spend=0.0,
                currency="USD",
                ctr_percent=0.0,
                cpc=0.0,
                conversions=0,
                cost_per_conversion=0.0,
                dashboard_url=""
            )
            return AgentOutputs(
                qualified_leads=[],
                personalized_messages=[],
                campaign_id="",
                campaign_dashboard_url="",
                ad_performance=empty_metrics,
                summary_report="",
                github_issue_url="",
                status="error",
                error_message=str(e)
            )

    def _parse_icp(self, icp: ICPDetails, campaign: CampaignConfig) -> Dict[str, Any]:
        """Step 1 helper to format and validate ICP specs."""
        return {
            "industry": icp.industry,
            "company_size": icp.company_size_range,
            "job_titles": icp.target_job_titles,
            "locations": icp.target_locations,
            "campaign_name": campaign.campaign_name,
            "daily_budget": campaign.daily_budget,
            "objective": campaign.objective
        }

    def _extract_leads(self, raw_data: List[Dict[str, Any]]) -> List[Lead]:
        """Step 3 helper to format Apollo prospects into Lead objects."""
        leads = []
        for idx, item in enumerate(raw_data):
            lead = Lead(
                id=item.get("id", f"lead-{idx+1}"),
                name=item.get("name", "Target Prospect"),
                title=item.get("title", "Marketing Director"),
                company=item.get("company", "B2B SaaS Inc"),
                email=item.get("email", f"prospect{idx}@example.com"),
                linkedin_url=item.get("linkedin_url", "https://linkedin.com"),
                industry=item.get("industry", "B2B SaaS"),
                company_size=item.get("company_size", "50-200"),
                location=item.get("location", "United States")
            )
            leads.append(lead)
        return leads

    def _draft_personalized_messages(
        self,
        leads: List[Lead],
        templates: List[Dict[str, str]]
    ) -> List[PersonalizedMessage]:
        """Step 4 helper to draft lead-specific personalized outbound sales messages."""
        messages = []
        default_tmpl = templates[0] if templates else {
            "subject": "Personalized AI content for {{company}}",
            "body": "Hi {{first_name}},\n\nReaching out because of your work as {{title}} at {{company}}."
        }

        for lead in leads:
            first_name = lead.name.split()[0] if lead.name else "there"
            subject = default_tmpl["subject"].replace("{{company}}", lead.company).replace("{{first_name}}", first_name).replace("{{title}}", lead.title)
            body = (
                default_tmpl["body"]
                .replace("{{company}}", lead.company)
                .replace("{{first_name}}", first_name)
                .replace("{{title}}", lead.title)
                .replace("{{full_name}}", lead.name)
            )

            messages.append(
                PersonalizedMessage(
                    lead_id=lead.id,
                    lead_name=lead.name,
                    lead_company=lead.company,
                    lead_email=lead.email,
                    subject=subject,
                    body=body
                )
            )

        return messages

    def _compile_summary_report(
        self,
        inputs: AgentInputs,
        leads: List[Lead],
        messages: List[PersonalizedMessage],
        campaign: Dict[str, Any],
        metrics: AdPerformanceMetrics
    ) -> str:
        """Step 9 helper to compile complete outbound & ads summary report."""
        lines = [
            "# PersonaScript Targeted Outreach & LinkedIn Ads Execution Report",
            "",
            "## Executive Summary",
            f"Successfully initiated outbound prospecting via Apollo.io and launched a targeted LinkedIn Ad campaign. "
            f"Generated **{len(leads)} qualified leads**, drafted personalized outbound messaging, and launched campaign `{campaign['campaign_id']}`.",
            "",
            "## 🎯 Ideal Customer Profile (ICP) Criteria",
            f"- **Industry**: {inputs.icp_details.industry}",
            f"- **Company Size**: {inputs.icp_details.company_size_range} employees",
            f"- **Target Job Titles**: {', '.join(inputs.icp_details.target_job_titles)}",
            f"- **Locations**: {', '.join(inputs.icp_details.target_locations)}",
            "",
            "## 👥 Qualified Prospect Pipeline (10-15 Leads)",
            "| Name | Title | Company | Email | LinkedIn Profile |",
            "| --- | --- | --- | --- | --- |"
        ]

        for lead in leads:
            lines.append(f"| {lead.name} | {lead.title} | {lead.company} | `{lead.email}` | [View Profile]({lead.linkedin_url}) |")

        lines.extend([
            "",
            "## ✉️ Sample Personalized Outbound Messages",
            f"Drafted **{len(messages)} lead-specific outreach messages** using personalized template placeholders.",
            "",
            f"### Sample Message for {messages[0].lead_name} ({messages[0].lead_company})",
            f"**Subject**: `{messages[0].subject}`",
            "```text",
            messages[0].body,
            "```",
            "",
            "## 🚀 LinkedIn Ad Campaign Performance Report",
            f"- **Campaign ID**: `{metrics.campaign_id}`",
            f"- **Campaign Dashboard URL**: {metrics.dashboard_url}",
            f"- **Daily Budget**: ${inputs.campaign_config.daily_budget:.2f} {metrics.currency}",
            f"- **Total Spend to Date**: ${metrics.spend:.2f} {metrics.currency}",
            f"- **Impressions Delivered**: {metrics.impressions:,}",
            f"- **Clicks Generated**: {metrics.clicks:,}",
            f"- **Click-Through Rate (CTR)**: {metrics.ctr_percent:.2f}%",
            f"- **Average CPC**: ${metrics.cpc:.2f}",
            f"- **Conversions**: {metrics.conversions}",
            f"- **Cost per Conversion**: ${metrics.cost_per_conversion:.2f}",
            ""
        ])

        return "\n".join(lines)

    def _create_github_issue(
        self,
        inputs: AgentInputs,
        leads: List[Lead],
        messages: List[PersonalizedMessage],
        campaign: Dict[str, Any],
        metrics: AdPerformanceMetrics,
        summary_report: str
    ) -> str:
        """Step 10 helper to post comprehensive execution summary to GitHub."""
        title = f"Outbound Sales Pipeline & LinkedIn Ads Campaign Launch ({metrics.campaign_id})"
        body = f"""# Targeted Outreach & LinkedIn Ads Campaign Execution

## Goal
Initiate targeted outbound sales efforts and launch focused LinkedIn ad campaigns, generating a qualified sales pipeline and measurable ad performance for PersonaScript.

## Inputs
- **Target Industry**: {inputs.icp_details.industry} ({inputs.icp_details.company_size_range} size)
- **Target Job Titles**: {", ".join(inputs.icp_details.target_job_titles)}
- **Campaign Objective**: {inputs.campaign_config.objective} (${inputs.campaign_config.daily_budget}/day)
- **Creatives Uploaded**: {len(inputs.ad_creatives)} creative variations

## Generated Deliverables & Outputs
- **Qualified Lead Pipeline**: {len(leads)} prospect profiles sourced via Apollo.io
- **Personalized Outreach Drafts**: {len(messages)} messaging templates prepped
- **LinkedIn Campaign ID**: `{metrics.campaign_id}`
- **LinkedIn Campaign Dashboard**: {metrics.dashboard_url}

## Campaign Metrics Summary
- **Impressions**: {metrics.impressions:,}
- **Clicks**: {metrics.clicks:,}
- **Spend**: ${metrics.spend:.2f} {metrics.currency}
- **CTR**: {metrics.ctr_percent:.2f}%
- **CPC**: ${metrics.cpc:.2f}
- **Conversions**: {metrics.conversions} (Cost/Conv: ${metrics.cost_per_conversion:.2f})

---
{summary_report}
"""

        github_url = self.github.create_issue(
            title=title,
            body=body,
            labels=["outbound-sales", "linkedin-ads", "lead-gen"]
        )
        return github_url
