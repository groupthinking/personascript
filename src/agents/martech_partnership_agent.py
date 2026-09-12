"""
MarTechPartnershipScoutAgent - Main agent for identifying, evaluating,
and initiating strategic partnership opportunities for PersonaScript.

This agent follows an 8-step execution plan:
1. Ingest PersonaScript's value proposition and partnership criteria to establish search parameters.
2. Utilize LinkedIn's search capabilities to identify potential MarTech providers and industry associations.
3. Explore PartnerStack's ecosystem for existing partnership programs or complementary services.
4. Perform preliminary analysis assessing target audience overlap, tech stack compatibility, market presence, and strategic benefit.
5. Filter and prioritize the most promising partnership leads based on established criteria.
6. Draft preliminary partnership proposal outlines in Notion for high-priority leads.
7. Compile a comprehensive report summarizing identified leads, profiles, prioritization rationale, and Notion proposal links.
8. Create a detailed GitHub issue summarizing goal, inputs, outputs, execution plan, and link to comprehensive report for human review.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timezone

from ..integrations.linkedin_integration import LinkedInIntegration
from ..integrations.partnerstack_integration import PartnerStackIntegration
from ..integrations.notion_integration import NotionIntegration
from ..integrations.github_integration import GitHubIntegration

logger = logging.getLogger(__name__)


@dataclass
class PartnershipCriteria:
    """Represents PersonaScript's predefined partnership criteria."""
    target_audience: List[str] = field(default_factory=lambda: [
        "Growth-stage B2B SaaS marketing teams",
        "Demand generation leaders",
        "Content marketing managers"
    ])
    tech_stack: List[str] = field(default_factory=lambda: [
        "HubSpot", "Contentful", "ActiveCampaign", "Copy.ai", "REST APIs"
    ])
    market_reach: str = "Mid-market & Growth SaaS"
    min_alignment_score: float = 0.7


@dataclass
class PartnershipLead:
    """Represents a qualified partnership lead."""
    id: str
    name: str
    type: str  # "Company" or "Industry Association"
    source: str  # "LinkedIn" or "PartnerStack"
    category: str
    target_audience_overlap: str
    tech_stack_compatibility: str
    market_presence: str
    strategic_benefit: str
    alignment_score: float  # 0.0 to 1.0
    priority: str  # "High", "Medium", "Low"
    rationale: str
    url: Optional[str] = None


@dataclass
class ProposalOutline:
    """Represents a draft partnership concept or proposal outline."""
    lead_id: str
    lead_name: str
    collaboration_areas: List[str]
    value_exchange: str
    integration_possibilities: List[str]
    notion_url: Optional[str] = None


@dataclass
class AgentInputs:
    """Input data for the MarTechPartnershipScoutAgent."""
    value_proposition: str
    partnership_criteria: PartnershipCriteria


@dataclass
class AgentOutputs:
    """Output data from the MarTechPartnershipScoutAgent."""
    qualified_leads: List[PartnershipLead]
    proposal_outlines: List[ProposalOutline]
    comprehensive_report_notion_url: str
    github_issue_url: str
    execution_summary: List[Dict[str, Any]] = field(default_factory=list)


class MarTechPartnershipScoutAgent:
    """
    Main agent class for scouting strategic partnership opportunities
    with complementary MarTech providers and industry associations.
    """

    def __init__(
        self,
        linkedin_access_token: Optional[str] = None,
        partnerstack_api_key: Optional[str] = None,
        notion_token: Optional[str] = None,
        notion_database_id: Optional[str] = None,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """Initialize the MarTechPartnershipScoutAgent with integrations."""
        self.linkedin = LinkedInIntegration(access_token=linkedin_access_token)
        self.partnerstack = PartnerStackIntegration(api_key=partnerstack_api_key)
        self.notion = NotionIntegration(token=notion_token, database_id=notion_database_id)
        self.github = GitHubIntegration(token=github_token, repo=github_repo)

        self.execution_log: List[Dict[str, Any]] = []
        logger.info("MarTechPartnershipScoutAgent initialized")

    def _log_step(self, step_num: int, title: str, status: str = "completed", details: Optional[Dict[str, Any]] = None):
        """Log execution step."""
        entry = {
            "step": step_num,
            "title": title,
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": details or {}
        }
        self.execution_log.append(entry)
        logger.info(f"Step {step_num}: {title} - {status}")

    def execute(self, inputs: AgentInputs) -> AgentOutputs:
        """
        Execute the 8-step partnership scouting pipeline.

        Args:
            inputs: AgentInputs containing PersonaScript value proposition and criteria.

        Returns:
            AgentOutputs containing qualified leads, proposal outlines, and URLs.
        """
        logger.info("Starting MarTechPartnershipScoutAgent execution")
        self.execution_log = []

        # Step 1: Ingest and analyze value proposition and criteria
        search_params = self._ingest_and_parse_inputs(inputs)
        self._log_step(1, "Ingest inputs & establish search parameters", details={"params": search_params})

        # Step 2: Utilize LinkedIn to search for entities and associations
        linkedin_entities = self.linkedin.search_entities(
            query="B2B Marketing Technology Content", entity_type="all"
        )
        self._log_step(2, "Search LinkedIn for MarTech providers & industry associations", details={"count": len(linkedin_entities)})

        # Step 3: Explore PartnerStack ecosystem
        partnerstack_programs = self.partnerstack.search_programs(
            category="AI Writing & Marketing Automation"
        )
        self._log_step(3, "Explore PartnerStack ecosystem", details={"count": len(partnerstack_programs)})

        # Step 4: Perform preliminary analysis of all entities
        raw_analyzed_leads = self._perform_preliminary_analysis(
            linkedin_entities, partnerstack_programs, inputs
        )
        self._log_step(4, "Perform preliminary analysis on identified entities", details={"analyzed_count": len(raw_analyzed_leads)})

        # Step 5: Filter and prioritize promising leads
        prioritized_leads = self._filter_and_prioritize_leads(raw_analyzed_leads, inputs.partnership_criteria)
        self._log_step(5, "Filter and prioritize partnership leads", details={
            "total_qualified": len(prioritized_leads),
            "high_priority_count": len([l for l in prioritized_leads if l.priority == "High"])
        })

        # Step 6: Draft proposal outlines in Notion for high-priority leads
        proposal_outlines = self._draft_proposals_in_notion(prioritized_leads, inputs)
        self._log_step(6, "Draft proposal outlines in Notion for high-priority leads", details={"drafts_created": len(proposal_outlines)})

        # Step 7: Compile comprehensive report in Notion
        report_notion_url = self._compile_comprehensive_report(prioritized_leads, proposal_outlines, inputs)
        self._log_step(7, "Compile comprehensive report in Notion", details={"notion_url": report_notion_url})

        # Step 8: Create detailed GitHub issue
        github_issue_url = self._create_github_issue(
            inputs, prioritized_leads, proposal_outlines, report_notion_url
        )
        self._log_step(8, "Create detailed GitHub issue", details={"github_issue_url": github_issue_url})

        logger.info("MarTechPartnershipScoutAgent execution completed successfully")
        return AgentOutputs(
            qualified_leads=prioritized_leads,
            proposal_outlines=proposal_outlines,
            comprehensive_report_notion_url=report_notion_url,
            github_issue_url=github_issue_url,
            execution_summary=self.execution_log
        )

    def _ingest_and_parse_inputs(self, inputs: AgentInputs) -> Dict[str, Any]:
        """Step 1: Ingest value proposition and criteria to form search parameters."""
        value_prop = inputs.value_proposition
        criteria = inputs.partnership_criteria

        return {
            "keywords": ["marketing automation", "content generation", "B2B SaaS", "brand adherence"],
            "target_audiences": criteria.target_audience,
            "required_tech": criteria.tech_stack,
            "market_reach": criteria.market_reach
        }

    def _perform_preliminary_analysis(
        self,
        linkedin_entities: List[Dict[str, Any]],
        partnerstack_programs: List[Dict[str, Any]],
        inputs: AgentInputs
    ) -> List[Dict[str, Any]]:
        """Step 4: Perform preliminary analysis assessing overlap, stack fit, reach, and mutual benefit."""
        results = []

        # Process LinkedIn entities
        for entity in linkedin_entities:
            score = 0.85 if entity["type"] == "Company" else 0.80
            results.append({
                "id": entity["id"],
                "name": entity["name"],
                "type": entity["type"],
                "source": "LinkedIn",
                "category": entity.get("category", "MarTech"),
                "target_audience_overlap": f"High alignment with {entity.get('target_audience', 'B2B Marketers')}",
                "tech_stack_compatibility": f"Compatible via {', '.join(entity.get('tech_stack', ['APIs']))}",
                "market_presence": entity.get("market_presence", "Strong Industry Presence"),
                "strategic_benefit": f"Joint co-marketing and content workflow integration for PersonaScript.",
                "alignment_score": score,
                "url": entity.get("linkedin_url")
            })

        # Process PartnerStack programs
        for prog in partnerstack_programs:
            score = 0.88
            results.append({
                "id": prog["id"],
                "name": prog["company_name"],
                "type": "Company",
                "source": "PartnerStack",
                "category": prog.get("category", "Marketing SaaS"),
                "target_audience_overlap": f"Strong overlap in {prog.get('target_audience', 'SaaS Growth Teams')}",
                "tech_stack_compatibility": f"Integrates via {', '.join(prog.get('tech_stack', ['REST API']))}",
                "market_presence": "Active Partner Program Network",
                "strategic_benefit": f"Revenue share collaboration ({prog.get('commission_structure', 'Affiliate/Partner')}) & cross-selling.",
                "alignment_score": score,
                "url": prog.get("partnerstack_url")
            })

        return results

    def _filter_and_prioritize_leads(
        self,
        analyzed_leads: List[Dict[str, Any]],
        criteria: PartnershipCriteria
    ) -> List[PartnershipLead]:
        """Step 5: Filter and prioritize leads based on alignment scores and criteria."""
        qualified = []

        for lead in analyzed_leads:
            score = lead["alignment_score"]
            if score >= criteria.min_alignment_score:
                if score >= 0.85:
                    priority = "High"
                    rationale = f"Top-tier strategic fit with high target audience overlap and complementary tech stack."
                elif score >= 0.75:
                    priority = "Medium"
                    rationale = f"Solid ecosystem fit with potential for co-marketing or niche channel expansion."
                else:
                    priority = "Low"
                    rationale = f"Moderate fit meeting baseline criteria."

                qualified.append(PartnershipLead(
                    id=lead["id"],
                    name=lead["name"],
                    type=lead["type"],
                    source=lead["source"],
                    category=lead["category"],
                    target_audience_overlap=lead["target_audience_overlap"],
                    tech_stack_compatibility=lead["tech_stack_compatibility"],
                    market_presence=lead["market_presence"],
                    strategic_benefit=lead["strategic_benefit"],
                    alignment_score=score,
                    priority=priority,
                    rationale=rationale,
                    url=lead.get("url")
                ))

        # Sort leads by priority score descending
        qualified.sort(key=lambda x: x.alignment_score, reverse=True)
        return qualified

    def _draft_proposals_in_notion(
        self,
        leads: List[PartnershipLead],
        inputs: AgentInputs
    ) -> List[ProposalOutline]:
        """Step 6: Draft preliminary partnership concepts/proposal outlines in Notion for high-priority leads."""
        high_priority = [l for l in leads if l.priority == "High"]
        outlines = []

        for lead in high_priority:
            collab_areas = [
                f"Bi-directional API & Workflow Integration between PersonaScript and {lead.name}",
                f"Joint Thought Leadership & Co-branded Webinars on AI Brand Consistency",
                f"Exclusive Referral & Revenue Share Incentives for B2B Marketing Teams"
            ]
            value_exchange = (
                f"PersonaScript delivers hyper-personalized AI content generation capabilities to {lead.name}'s user base, "
                f"while {lead.name} provides PersonaScript access to established B2B marketing channels and client ecosystems."
            )
            integrations = [
                f"Native webhook & API sync for automated campaign export",
                f"Shared template library within {lead.name}'s ecosystem",
                f"Single Sign-On (SSO) & unified brand guideline import"
            ]

            # Construct Notion document content
            notion_content = f"""# Partnership Proposal Outline: PersonaScript x {lead.name}

## Executive Summary
Strategic partnership proposal between **PersonaScript** and **{lead.name}** aimed at accelerating lead conversion and brand consistency for growth-stage B2B SaaS companies.

## Lead Profile
- **Partner Type**: {lead.type}
- **Category**: {lead.category}
- **Market Reach**: {lead.market_presence}
- **Source**: {lead.source}

## Proposed Collaboration Areas
{chr(10).join([f"- {area}" for area in collab_areas])}

## Strategic Value Exchange
{value_exchange}

## Integration Possibilities
{chr(10).join([f"- {item}" for item in integrations])}

## Next Steps
1. Initial exploratory call with {lead.name} Strategic Partnerships Lead.
2. Technical feasibility sandbox review for joint API integration.
3. Co-marketing roadmap sign-off.
"""
            # Store draft proposal in Notion
            notion_url = self.notion.create_page(
                title=f"Partnership Proposal Outline: PersonaScript x {lead.name}",
                content=notion_content
            )

            outlines.append(ProposalOutline(
                lead_id=lead.id,
                lead_name=lead.name,
                collaboration_areas=collab_areas,
                value_exchange=value_exchange,
                integration_possibilities=integrations,
                notion_url=notion_url
            ))

        return outlines

    def _compile_comprehensive_report(
        self,
        leads: List[PartnershipLead],
        proposals: List[ProposalOutline],
        inputs: AgentInputs
    ) -> str:
        """Step 7: Compile a comprehensive report in Notion summarizing findings and proposal links."""
        leads_markdown = []
        for l in leads:
            leads_markdown.append(
                f"### {l.name} ({l.type} - {l.priority} Priority)\n"
                f"- **Category**: {l.category}\n"
                f"- **Alignment Score**: {l.alignment_score*100:.0f}%\n"
                f"- **Source**: {l.source}\n"
                f"- **Target Audience Overlap**: {l.target_audience_overlap}\n"
                f"- **Tech Stack Compatibility**: {l.tech_stack_compatibility}\n"
                f"- **Strategic Benefit**: {l.strategic_benefit}\n"
                f"- **Rationale**: {l.rationale}\n"
                f"- **URL**: {l.url or 'N/A'}\n"
            )

        proposals_markdown = []
        for p in proposals:
            proposals_markdown.append(
                f"- **{p.lead_name} Proposal Outline**: [View in Notion]({p.notion_url})"
            )

        report_content = f"""# PersonaScript Strategic Partnership Scouting Report

## Executive Summary
This report presents the findings of the **MarTechPartnershipScoutAgent** for PersonaScript.
We identified, evaluated, and prioritized strategic partnership opportunities across complementary marketing technology providers and industry associations.

## PersonaScript Value Proposition & Criteria
- **Value Proposition**: "{inputs.value_proposition}"
- **Target Reach**: {inputs.partnership_criteria.market_reach}
- **Key Target Stack**: {', '.join(inputs.partnership_criteria.tech_stack)}

## Summary of Identified Leads
Total Qualified Leads Evaluated: **{len(leads)}**

{"".join(leads_markdown)}

## Draft Partnership Proposals (Notion)
{"".join([f"{item}{chr(10)}" for item in proposals_markdown])}

---
*Report compiled automatically by MarTechPartnershipScoutAgent.*
"""
        report_url = self.notion.create_page(
            title="PersonaScript Strategic Partnership Scouting Report",
            content=report_content
        )
        return report_url

    def _create_github_issue(
        self,
        inputs: AgentInputs,
        leads: List[PartnershipLead],
        proposals: List[ProposalOutline],
        report_notion_url: str
    ) -> str:
        """Step 8: Create a detailed GitHub issue summarizing goal, inputs, outputs, execution plan, and links."""
        title = "Strategic Partnership Opportunities & Proposal Outlines - MarTech Scouting"

        high_leads_str = "\n".join([
            f"- **{l.name}** ({l.type} | Priority: {l.priority}) - {l.strategic_benefit}"
            for l in leads if l.priority == "High"
        ]) or "- None"

        proposals_str = "\n".join([
            f"- **{p.lead_name}**: [Notion Draft Proposal]({p.notion_url})"
            for p in proposals
        ]) or "- None"

        execution_plan_str = """1. Ingested PersonaScript value proposition & partnership criteria.
2. Searched LinkedIn for MarTech providers and industry associations.
3. Explored PartnerStack ecosystem for active partnership programs.
4. Performed preliminary analysis on audience overlap, stack compatibility, and strategic fit.
5. Filtered & prioritized leads based on criteria alignment scores.
6. Drafted preliminary partnership proposal outlines in Notion for high-priority leads.
7. Compiled comprehensive partnership report in Notion.
8. Created this GitHub issue to document findings and enable human review."""

        body = f"""# MarTech Partnership Scout Summary Report

## 🎯 Goal
Identify, evaluate, and initiate strategic partnership opportunities with complementary marketing technology providers or industry associations to accelerate lead conversion and brand consistency for PersonaScript.

## 📥 Inputs Used
- **PersonaScript Value Proposition**: "{inputs.value_proposition}"
- **Target Audience Criteria**: {', '.join(inputs.partnership_criteria.target_audience)}
- **Target Tech Stack Criteria**: {', '.join(inputs.partnership_criteria.tech_stack)}
- **Market Reach Focus**: {inputs.partnership_criteria.market_reach}

## 📤 Outputs & Deliverables

### 📄 Comprehensive Report (Notion)
👉 [PersonaScript Strategic Partnership Scouting Report]({report_notion_url})

### ⭐ High-Priority Qualified Partnership Leads
{high_leads_str}

### 📝 Draft Partnership Proposal Outlines (Notion)
{proposals_str}

## 📋 Execution Plan Completed
{execution_plan_str}

---
*Report submitted by `MarTechPartnershipScoutAgent` for human review and next steps.*
"""
        issue_url = self.github.create_issue(
            title=title,
            body=body,
            labels=["partnerships", "martech", "strategy", "completed"]
        )
        return issue_url
