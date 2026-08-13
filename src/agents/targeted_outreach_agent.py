"""
TargetedOutreachAgent - Main agent for initiating outbound sales efforts and LinkedIn ad campaigns.

This agent parses PersonaScript ICP details, uses Apollo.io to search and compile a qualified lead list,
drafts personalized sales messages using templates, configures and launches a LinkedIn Ads campaign,
retrieves initial performance metrics, compiles a comprehensive summary report, and submits a detailed
task summary report via a GitHub issue.
"""

import json
import logging
import csv
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from ..integrations.apollo_integration import ApolloIntegration
from ..integrations.linkedin_integration import LinkedInIntegration
from ..integrations.github_integration import GitHubIntegration

logger = logging.getLogger(__name__)


@dataclass
class LeadInfo:
    """Information for a qualified lead."""
    first_name: str
    last_name: str
    name: str
    title: str
    company_name: str
    company_size: str
    industry: str
    email: str
    linkedin_url: str
    location: str
    id: str = ""
    personalized_message: str = ""


@dataclass
class TargetedOutreachInputs:
    """Input parameters for the TargetedOutreachAgent."""
    icp_industries: List[str]
    icp_company_sizes: List[str]
    icp_job_titles: List[str]
    ad_budget: float
    ad_objective: str
    ad_copy: str
    ad_asset_url: str
    message_template: str


@dataclass
class TargetedOutreachOutputs:
    """Output parameters produced by the TargetedOutreachAgent."""
    lead_list_file_path: str
    linkedin_campaign_id: str
    linkedin_dashboard_url: str
    performance_metrics: Dict[str, Any]
    github_issue_url: str
    leads: List[LeadInfo]


class TargetedOutreachAgent:
    """
    Agent coordinates 10-step targeted outreach campaign execution:
    1. Parse and understand PersonaScript's Ideal Customer Profile (ICP) details and objectives.
    2. Search for target companies/individuals matching defined ICP via Apollo.io.
    3. Extract relevant contact info and compile into a preliminary list.
    4. Prepare personalized outbound sales message drafts using template.
    5. Configure new LinkedIn Ad campaign using LinkedIn Ads API.
    6. Upload provided ad creatives and ad copy.
    7. Launch configured LinkedIn Ad campaign live.
    8. Retrieve initial performance metrics.
    9. Compile all deliverables (lead list, message drafts, ad data) into summary.
    10. Create a detailed GitHub issue summarizing execution with all links.
    """

    def __init__(
        self,
        apollo_api_key: Optional[str] = None,
        linkedin_client_id: Optional[str] = None,
        linkedin_client_secret: Optional[str] = None,
        linkedin_account_id: Optional[str] = None,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """Initialize the TargetedOutreachAgent with required integrations."""
        self.apollo_integration = ApolloIntegration(api_key=apollo_api_key)
        self.linkedin_integration = LinkedInIntegration(
            client_id=linkedin_client_id,
            client_secret=linkedin_client_secret,
            account_id=linkedin_account_id
        )
        self.github_integration = GitHubIntegration(
            token=github_token,
            repo=github_repo
        )
        logger.info("TargetedOutreachAgent initialized successfully")

    def execute(self, inputs: TargetedOutreachInputs) -> TargetedOutreachOutputs:
        """
        Execute the complete 10-step targeted outreach campaign workflow.

        Args:
            inputs: TargetedOutreachInputs parameters.

        Returns:
            TargetedOutreachOutputs with results, file path, and URLs.
        """
        logger.info("Executing TargetedOutreachAgent workflow")

        # Step 1: Parse and understand ICP details and objectives
        icp_details = self._parse_icp_details(inputs)

        # Step 2 & 3: Search and extract contact info from Apollo.io
        raw_leads = self.apollo_integration.search_leads(
            industries=icp_details["industries"],
            company_sizes=icp_details["company_sizes"],
            job_titles=icp_details["job_titles"],
            limit=15
        )

        leads: List[LeadInfo] = []
        for lead in raw_leads:
            leads.append(LeadInfo(
                id=lead.get("id", ""),
                first_name=lead.get("first_name", ""),
                last_name=lead.get("last_name", ""),
                name=lead.get("name", ""),
                title=lead.get("title", ""),
                company_name=lead.get("company_name", ""),
                company_size=lead.get("company_size", ""),
                industry=lead.get("industry", ""),
                email=lead.get("email", ""),
                linkedin_url=lead.get("linkedin_url", ""),
                location=lead.get("location", "")
            ))

        # Step 4: Prepare personalized outbound messages using provided template
        self._personalize_messages(leads, inputs.message_template)

        # Save to file
        lead_list_file_path = "targeted_outreach_leads.json"
        self._save_leads_json(leads, lead_list_file_path)

        # Step 5: Configure new LinkedIn Ad campaign
        audience_targeting = {
            "industries": icp_details["industries"],
            "company_sizes": icp_details["company_sizes"],
            "job_titles": icp_details["job_titles"]
        }
        campaign_name = f"PersonaScript Outbound Campaign - {icp_details['industries'][0] if icp_details['industries'] else 'Target'}"
        campaign_id = self.linkedin_integration.create_campaign(
            name=campaign_name,
            objective=inputs.ad_objective,
            budget=inputs.ad_budget,
            audience_criteria=audience_targeting
        )

        # Step 6: Upload provided ad creatives and copy
        self.linkedin_integration.upload_creative(
            campaign_id=campaign_id,
            copy=inputs.ad_copy,
            asset_url=inputs.ad_asset_url
        )

        # Step 7: Launch configured campaign
        self.linkedin_integration.launch_campaign(campaign_id=campaign_id)

        # Step 8: Retrieve performance metrics
        metrics = self.linkedin_integration.get_campaign_performance(campaign_id=campaign_id)
        dashboard_url = self.linkedin_integration.get_dashboard_url(campaign_id=campaign_id)

        # Step 9: Compile all deliverables into a comprehensive summary report
        summary_report = self._compile_summary_report(leads, metrics, campaign_id, dashboard_url, inputs)

        # Step 10: Create detailed GitHub issue
        issue_title = f"PersonaScript Targeted Outreach Campaign Execution - {campaign_name}"
        github_issue_url = self.github_integration.create_issue(
            title=issue_title,
            body=summary_report,
            labels=["outreach-campaign", "completed"]
        )

        logger.info("TargetedOutreachAgent completed workflow successfully")

        return TargetedOutreachOutputs(
            lead_list_file_path=lead_list_file_path,
            linkedin_campaign_id=campaign_id,
            linkedin_dashboard_url=dashboard_url,
            performance_metrics=metrics,
            github_issue_url=github_issue_url,
            leads=leads
        )

    def _parse_icp_details(self, inputs: TargetedOutreachInputs) -> Dict[str, Any]:
        """Step 1: Parse and validate ICP and objectives."""
        logger.info("Step 1: Parsing and understanding ICP details")
        return {
            "industries": inputs.icp_industries,
            "company_sizes": inputs.icp_company_sizes,
            "job_titles": inputs.icp_job_titles,
            "budget": inputs.ad_budget,
            "objective": inputs.ad_objective
        }

    def _personalize_messages(self, leads: List[LeadInfo], template: str) -> None:
        """Step 4: Personalize templates with prospect-specific variables."""
        logger.info("Step 4: Preparing personalized outbound sales message drafts")
        for lead in leads:
            message = template
            message = message.replace("{first_name}", lead.first_name)
            message = message.replace("{last_name}", lead.last_name)
            message = message.replace("{title}", lead.title)
            message = message.replace("{company_name}", lead.company_name)
            message = message.replace("{industry}", lead.industry)
            lead.personalized_message = message

    def _save_leads_json(self, leads: List[LeadInfo], file_path: str) -> None:
        """Save prospects and message drafts to JSON file."""
        logger.info(f"Saving compiled lead list to {file_path}")
        data = []
        for lead in leads:
            data.append({
                "id": lead.id,
                "first_name": lead.first_name,
                "last_name": lead.last_name,
                "name": lead.name,
                "title": lead.title,
                "company_name": lead.company_name,
                "company_size": lead.company_size,
                "industry": lead.industry,
                "email": lead.email,
                "linkedin_url": lead.linkedin_url,
                "location": lead.location,
                "personalized_message": lead.personalized_message
            })
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def _compile_summary_report(
        self,
        leads: List[LeadInfo],
        metrics: Dict[str, Any],
        campaign_id: str,
        dashboard_url: str,
        inputs: TargetedOutreachInputs
    ) -> str:
        """Step 9: Compile execution deliverables into summary report markdown."""
        logger.info("Step 9: Compiling summary report")
        lead_rows = []
        for lead in leads[:5]:  # Limit top 5 in the issue summary for brevity
            lead_rows.append(
                f"| {lead.name} | {lead.title} | {lead.company_name} | {lead.email} | [LinkedIn]({lead.linkedin_url}) |"
            )
        top_leads_md = "\n".join(lead_rows)

        report = f"""# PersonaScript Targeted Outreach Campaign Execution Report

## Goal
To initiate targeted outbound sales efforts and launch focused LinkedIn ad campaigns, generating a qualified sales pipeline and measurable ad performance for PersonaScript.

## Campaign Inputs Used
- **ICP Target Industries:** {", ".join(inputs.icp_industries)}
- **ICP Company Sizes:** {", ".join(inputs.icp_company_sizes)}
- **ICP Target Job Titles:** {", ".join(inputs.icp_job_titles)}
- **LinkedIn Ads Budget:** ${inputs.ad_budget:,.2f}
- **LinkedIn Ads Objective:** {inputs.ad_objective}
- **Ad Creative Asset:** {inputs.ad_asset_url}

---

## Deliverables Generated

### 1. 📋 Qualified Sales Pipeline (Initial Lead List)
- **Total Leads Acquired:** {len(leads)} leads compiled from Apollo.io matching specified ICP.
- **Lead List File Path:** `targeted_outreach_leads.json` (contains contact info & message drafts)

#### Sample Qualified Leads (Top 5):
| Name | Title | Company | Email | LinkedIn |
|------|-------|---------|-------|----------|
{top_leads_md}

---

### 2. 🚀 LinkedIn Ads Campaign Dashboard
- **Campaign ID:** `{campaign_id}`
- **Report Dashboard Link:** [LinkedIn Campaign Manager Reporting]({dashboard_url})

---

### 3. 📊 Initial Campaign Performance Metrics
Early performance delivery metrics extracted from the LinkedIn Ads API:

- **Impressions:** {metrics.get("impressions", 0):,}
- **Clicks:** {metrics.get("clicks", 0):,}
- **CTR (Click-Through-Rate):** {metrics.get("ctr", 0.0):.2%}
- **Ad Spend:** ${metrics.get("spend", 0.0):,.2f}
- **CPC (Cost-Per-Click):** ${metrics.get("cpc", 0.0):,.2f}
- **Conversions:** {metrics.get("conversions", 0)}
- **Conversion Rate:** {metrics.get("conversion_rate", 0.0):.2%}

---

## Complete Execution Summary (10 Steps)
1.  **Parse Context**: Successfully mapped ICP (B2B SaaS, Marketing leaders) and campaign parameters.
2.  **Apollo Search**: Filtered Apollo.io database to locate relevant target personas.
3.  **Lead Compilation**: Extracted names, business emails, and LinkedIn URLs for {len(leads)} decision makers.
4.  **Message Personalization**: Filled outbound templates with custom parameters (e.g. customized headers, title alignment).
5.  **Campaign Configuration**: Configured settings via LinkedIn Ads API on account.
6.  **Creative Upload**: Mounted banner image/video creative with copy: *"{inputs.ad_copy[:60]}..."*
7.  **Campaign Launch**: Initialized delivery on the ad auction network.
8.  **Performance Check**: Queried analytics endpoints for active performance feedback.
9.  **Deliverables Compilation**: Compiled detailed pipeline leads JSON and structured this report.
10. **GitHub Publishing**: Created this comprehensive execution reporting issue.

---

## Next Steps
- Review `targeted_outreach_leads.json` for manual outreach verification.
- Scale outbound campaign based on initial conversion rates.
- Monitor LinkedIn Campaign dashboard as ad delivery scales across the week.
"""
        return report
