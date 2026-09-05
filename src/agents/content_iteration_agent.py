"""
PersonaScriptContentIterationAgent - Main agent for monitoring engagement, analyzing performance,
and proposing prioritized feature backlog items.

This agent follows a 9-step execution plan:
1. Retrieve content performance metrics from Mixpanel & Google Analytics
2. Collect user engagement data from Mixpanel & Google Analytics
3. Fetch active A/B test results from Optimizely
4. Consolidate and analyze all collected data
5. Generate 'Weekly Analytics Report'
6. Synthesize 'A/B Test Results Summary' document
7. Identify and prioritize content iteration opportunities and new features
8. Create Linear issues for high-priority items
9. Create a comprehensive GitHub issue as the primary deliverable
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timezone

from ..integrations.mixpanel_integration import MixpanelIntegration
from ..integrations.google_analytics_integration import GoogleAnalyticsIntegration
from ..integrations.optimizely_integration import OptimizelyIntegration
from ..integrations.linear_integration import LinearIntegration
from ..integrations.github_integration import GitHubIntegration

logger = logging.getLogger(__name__)


@dataclass
class ContentAsset:
    """Represents an existing content asset and its metadata."""
    id: str
    title: str
    url: str
    type: str  # e.g., "blog", "landing_page", "pricing"
    current_cta: str
    audience_target: str


@dataclass
class AgentInputs:
    """Inputs for the PersonaScriptContentIterationAgent."""
    start_date: str
    end_date: str
    existing_content_assets: List[ContentAsset]


@dataclass
class WeeklyAnalyticsReport:
    """Represents the generated Weekly Analytics Report."""
    summary: str
    content_performance: List[Dict[str, Any]]
    engagement_insights: List[Dict[str, Any]]
    underperforming_urls: List[str]
    high_performing_urls: List[str]


@dataclass
class ABTestResultsSummary:
    """Represents the generated A/B Test Results Summary."""
    summary: str
    experiments: List[Dict[str, Any]]
    winning_variations: List[Dict[str, Any]]
    actionable_recommendations: List[str]


@dataclass
class BacklogItem:
    """Represents a prioritized backlog item."""
    id: str
    title: str
    description: str
    priority_level: str  # "Critical", "High", "Medium", "Low"
    priority_score: int  # 0 to 100
    category: str  # e.g., "Headline optimization", "CTA optimization", "New Feature"
    target_url: Optional[str] = None
    linear_issue_url: Optional[str] = None


@dataclass
class AgentOutputs:
    """Outputs from the PersonaScriptContentIterationAgent."""
    weekly_analytics_report: WeeklyAnalyticsReport
    ab_test_results_summary: ABTestResultsSummary
    prioritized_feature_backlog: List[BacklogItem]
    github_issue_url: str
    status: str = "success"
    error_message: Optional[str] = None


class PersonaScriptContentIterationAgent:
    """
    Main agent class for monitoring engagement, analyzing performance,
    and proposing prioritized feature backlog items.
    """

    def __init__(
        self,
        mixpanel_api_key: Optional[str] = None,
        mixpanel_project_id: Optional[str] = None,
        google_analytics_property_id: Optional[str] = None,
        google_analytics_credentials_path: Optional[str] = None,
        optimizely_api_key: Optional[str] = None,
        optimizely_project_id: Optional[str] = None,
        linear_api_key: Optional[str] = None,
        linear_team_id: Optional[str] = None,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """Initialize the ContentIterationAgent with necessary integrations."""
        self.mixpanel = MixpanelIntegration(
            api_key=mixpanel_api_key, project_id=mixpanel_project_id
        )
        self.google_analytics = GoogleAnalyticsIntegration(
            property_id=google_analytics_property_id,
            credentials_path=google_analytics_credentials_path
        )
        self.optimizely = OptimizelyIntegration(
            api_key=optimizely_api_key, project_id=optimizely_project_id
        )
        self.linear = LinearIntegration(
            api_key=linear_api_key, team_id=linear_team_id
        )
        self.github = GitHubIntegration(
            token=github_token, repo=github_repo
        )

        self.execution_log: List[Dict[str, Any]] = []
        logger.info("PersonaScriptContentIterationAgent initialized")

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
        Execute the complete agent workflow.

        Args:
            inputs: AgentInputs including dates and content assets to analyze.

        Returns:
            AgentOutputs containing reports, backlog items, and GitHub URL.
        """
        logger.info("Starting ContentIterationAgent execution")
        self.execution_log = []

        try:
            # Step 1: Retrieve content performance metrics from Mixpanel and Google Analytics
            self._log_step(1, "Retrieve content performance metrics")
            mixpanel_perf = self.mixpanel.get_content_performance(inputs.start_date, inputs.end_date)
            ga_perf = self.google_analytics.get_content_performance(inputs.start_date, inputs.end_date)
            self._log_step(1, "Retrieve content performance metrics", "completed", {
                "mixpanel_records": len(mixpanel_perf), "ga_records": len(ga_perf)
            })

            # Step 2: Collect user engagement data from Mixpanel and Google Analytics
            self._log_step(2, "Collect user engagement data")
            mixpanel_eng = self.mixpanel.get_user_engagement(inputs.start_date, inputs.end_date)
            ga_eng = self.google_analytics.get_user_engagement(inputs.start_date, inputs.end_date)
            self._log_step(2, "Collect user engagement data", "completed", {
                "mixpanel_records": len(mixpanel_eng), "ga_records": len(ga_eng)
            })

            # Step 3: Fetch active A/B test results and relevant experiment data from Optimizely
            self._log_step(3, "Fetch active A/B test results")
            experiments = self.optimizely.get_experiments()
            self._log_step(3, "Fetch active A/B test results", "completed", {
                "experiments_count": len(experiments)
            })

            # Step 4: Consolidate and analyze all collected data
            self._log_step(4, "Consolidate and analyze collected data")
            analysis_data = self._analyze_data(
                inputs, mixpanel_perf, ga_perf, mixpanel_eng, ga_eng, experiments
            )
            self._log_step(4, "Consolidate and analyze collected data", "completed")

            # Step 5: Generate a comprehensive 'Weekly Analytics Report'
            self._log_step(5, "Generate Weekly Analytics Report")
            weekly_report = self._generate_weekly_report(analysis_data, inputs)
            self._log_step(5, "Generate Weekly Analytics Report", "completed")

            # Step 6: Synthesize A/B test results into a 'A/B Test Results Summary' document
            self._log_step(6, "Synthesize A/B Test Results Summary")
            ab_summary = self._synthesize_ab_results(experiments)
            self._log_step(6, "Synthesize A/B Test Results Summary", "completed")

            # Step 7: Identify and prioritize specific content iteration opportunities and potential new features
            self._log_step(7, "Identify and prioritize specific content iteration opportunities")
            backlog_items = self._prioritize_backlog(weekly_report, ab_summary, inputs)
            self._log_step(7, "Identify and prioritize specific content iteration opportunities", "completed", {
                "backlog_count": len(backlog_items)
            })

            # Step 8: Create a new issue in Linear for high-priority items
            self._log_step(8, "Create new issues in Linear for high-priority items")
            updated_backlog = self._create_linear_issues(backlog_items)
            self._log_step(8, "Create new issues in Linear for high-priority items", "completed")

            # Step 9: Compile a detailed GitHub issue
            self._log_step(9, "Compile and create comprehensive GitHub issue")
            github_issue_url = self._create_github_issue(
                weekly_report, ab_summary, updated_backlog, inputs
            )
            self._log_step(9, "Compile and create comprehensive GitHub issue", "completed", {
                "issue_url": github_issue_url
            })

            logger.info("ContentIterationAgent execution completed successfully")
            return AgentOutputs(
                weekly_analytics_report=weekly_report,
                ab_test_results_summary=ab_summary,
                prioritized_feature_backlog=updated_backlog,
                github_issue_url=github_issue_url,
                status="success"
            )
        except Exception as e:
            logger.error("Error during ContentIterationAgent execution", exc_info=True)
            empty_report = WeeklyAnalyticsReport(
                summary="An error occurred during execution. No analytics available.",
                content_performance=[],
                engagement_insights=[],
                underperforming_urls=[],
                high_performing_urls=[]
            )
            empty_ab = ABTestResultsSummary(
                summary="An error occurred during execution. No A/B test data available.",
                experiments=[],
                winning_variations=[],
                actionable_recommendations=[]
            )
            return AgentOutputs(
                weekly_analytics_report=empty_report,
                ab_test_results_summary=empty_ab,
                prioritized_feature_backlog=[],
                github_issue_url="",
                status="error",
                error_message=str(e)
            )

    def _analyze_data(
        self,
        inputs: AgentInputs,
        mp_perf: List[Dict[str, Any]],
        ga_perf: List[Dict[str, Any]],
        mp_eng: List[Dict[str, Any]],
        ga_eng: List[Dict[str, Any]],
        experiments: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Consolidate page performance and engagement metrics with robust aggregation."""
        consolidated_pages = {}

        # Helper to get or create page profile
        def get_page(url: str):
            clean_url = url.split("?")[0]
            if clean_url not in consolidated_pages:
                consolidated_pages[clean_url] = {
                    "url": clean_url,
                    "views": 0,
                    "sessions": 0,
                    "conversion_rates": [],
                    "bounce_rates": [],
                    "times_on_page": [],
                    "engagement_rates": [],
                    "clicks_by_element": {},
                    "scroll_depths": []
                }
            return consolidated_pages[clean_url]

        # Process Mixpanel Perf
        for record in mp_perf:
            p = get_page(record["page_url"])
            p["views"] += record.get("page_views", 0)
            if "conversion_rate" in record:
                p["conversion_rates"].append(record["conversion_rate"])
            if "bounce_rate" in record:
                p["bounce_rates"].append(record["bounce_rate"])
            if "average_time_on_page_seconds" in record:
                p["times_on_page"].append(record["average_time_on_page_seconds"])

        # Process GA Perf
        for record in ga_perf:
            p = get_page(record["page_url"])
            p["sessions"] += record.get("sessions", 0)
            if "bounce_rate" in record:
                p["bounce_rates"].append(record["bounce_rate"])
            if "average_session_duration_seconds" in record:
                p["times_on_page"].append(record["average_session_duration_seconds"])

        # Process Mixpanel Engagement
        for record in mp_eng:
            p = get_page(record["page_url"])
            p["scroll_depths"].append(record.get("average_scroll_depth_percent", 0.0))
            for k, v in record.get("clicks_by_element", {}).items():
                p["clicks_by_element"][k] = p["clicks_by_element"].get(k, 0) + v

        # Process GA Engagement
        for record in ga_eng:
            p = get_page(record["page_url"])
            if "engagement_rate" in record:
                p["engagement_rates"].append(record["engagement_rate"])

        # Compute averages for rates and times
        final_pages = []
        for url, p in consolidated_pages.items():
            avg_conversion_rate = sum(p["conversion_rates"]) / len(p["conversion_rates"]) if p["conversion_rates"] else 0.0
            avg_bounce_rate = sum(p["bounce_rates"]) / len(p["bounce_rates"]) if p["bounce_rates"] else 0.0
            avg_time_on_page = sum(p["times_on_page"]) / len(p["times_on_page"]) if p["times_on_page"] else 0.0
            avg_engagement_rate = sum(p["engagement_rates"]) / len(p["engagement_rates"]) if p["engagement_rates"] else 0.0
            avg_scroll_depth = sum(p["scroll_depths"]) / len(p["scroll_depths"]) if p["scroll_depths"] else 0.0

            final_pages.append({
                "url": url,
                "views": p["views"],
                "sessions": p["sessions"],
                "conversion_rate": avg_conversion_rate,
                "bounce_rate": avg_bounce_rate,
                "average_time_on_page": avg_time_on_page,
                "engagement_rate": avg_engagement_rate,
                "clicks_by_element": p["clicks_by_element"],
                "scroll_depth": avg_scroll_depth
            })

        return {
            "pages": final_pages,
            "experiments": experiments
        }

    def _generate_weekly_report(self, analysis_data: Dict[str, Any], inputs: AgentInputs) -> WeeklyAnalyticsReport:
        """Step 5: Generate the Weekly Analytics Report."""
        pages = analysis_data["pages"]

        # Classify high vs underperforming based on conversion rate / bounce rate threshold
        high_performing = []
        underperforming = []

        for p in pages:
            # Benchmark thresholds: conversion rate > 4% is high, bounce rate > 60% or conversion < 2% is underperforming
            cv_rate = p.get("conversion_rate", 0.0)
            bounce_rate = p.get("bounce_rate", 0.0)

            if cv_rate >= 0.04:
                high_performing.append(p["url"])
            elif cv_rate < 0.02 or bounce_rate > 0.60:
                underperforming.append(p["url"])

        summary = (
            f"Weekly content performance summary from {inputs.start_date} to {inputs.end_date}.\n"
            f"Monitored {len(pages)} content assets. Identified {len(high_performing)} high-performing "
            f"pages and {len(underperforming)} underperforming pages that present iteration opportunities."
        )

        return WeeklyAnalyticsReport(
            summary=summary,
            content_performance=pages,
            engagement_insights=[
                {
                    "page_url": p["url"],
                    "clicks_summary": p["clicks_by_element"],
                    "scroll_depth_percent": p["scroll_depth"],
                    "engagement_rate": p["engagement_rate"]
                }
                for p in pages
            ],
            underperforming_urls=underperforming,
            high_performing_urls=high_performing
        )

    def _synthesize_ab_results(self, experiments: List[Dict[str, Any]]) -> ABTestResultsSummary:
        """Step 6: Synthesize A/B test results into a summary document."""
        winning_variations = []
        recommendations = []

        for exp in experiments:
            for var in exp.get("variations", []):
                if var.get("status") == "winning":
                    winning_variations.append({
                        "experiment_id": exp["experiment_id"],
                        "experiment_name": exp["name"],
                        "winning_variation": var["name"],
                        "improvement_percent": var.get("improvement_percent", 0.0),
                        "statistical_significance": var.get("statistical_significance", 0.0)
                    })

                    recommendations.append(
                        f"Deploy winning variation '{var['name']}' permanently for experiment '{exp['name']}'. "
                        f"This delivered a {var.get('improvement_percent', 0.0)}% improvement with "
                        f"{var.get('statistical_significance', 0.0)*100:.1f}% confidence."
                    )

        summary = (
            f"Analyzed {len(experiments)} active experiments on Optimizely. "
            f"Found {len(winning_variations)} winning variations with statistically significant improvements."
        )

        return ABTestResultsSummary(
            summary=summary,
            experiments=experiments,
            winning_variations=winning_variations,
            actionable_recommendations=recommendations
        )

    def _prioritize_backlog(
        self,
        weekly_report: WeeklyAnalyticsReport,
        ab_summary: ABTestResultsSummary,
        inputs: AgentInputs
    ) -> List[BacklogItem]:
        """
        Step 7: Identify specific content iteration opportunities and potential new features.

        Prioritizes items based on custom heuristics:
        - Target conversion uplift potential (bounce rate, low conversion rate)
        - Strategic alignment with lead conversion & brand consistency (scoring formula)
        """
        backlog_items = []

        # 1. Opportunities from underperforming pages (headline, CTA optimization)
        # Find match in existing assets to get rich metadata
        asset_map = {asset.url: asset for asset in inputs.existing_content_assets}

        for url in weekly_report.underperforming_urls:
            asset = asset_map.get(url)
            # Default title and type if not matched
            title = asset.title if asset else "Page Content"
            asset_type = asset.type if asset else "page"
            current_cta = asset.current_cta if asset else "Learn More"

            # Analyze page specific metrics to build a rich item
            page_perf = next((p for p in weekly_report.content_performance if p["url"] == url), {})
            bounce_rate = page_perf.get("bounce_rate", 0.0)
            conversion_rate = page_perf.get("conversion_rate", 0.0)

            if bounce_rate > 0.60:
                # Issue is likely headline/engagement alignment (brand consistency, target fit)
                desc = (
                    f"The page '{title}' at {url} has a high bounce rate of {bounce_rate*100:.1f}%. "
                    f"Optimize headlines to better align with target B2B buyer persona expectations."
                )
                # Calculate priority score out of 100
                score = int(bounce_rate * 100)
                priority_level = self._get_priority_level(score)
                backlog_items.append(BacklogItem(
                    id=f"backlog-headline-{hash(url) % 1000}",
                    title=f"Optimize Headlines on '{title}'",
                    description=desc,
                    priority_level=priority_level,
                    priority_score=score,
                    category="Headline optimization",
                    target_url=url
                ))

            if conversion_rate < 0.02:
                # Issue is likely CTA related
                desc = (
                    f"The page '{title}' at {url} has a very low conversion rate of {conversion_rate*100:.1f}%. "
                    f"Current CTA is '{current_cta}'. Propose CTA design optimization, layout shifts, or more high-intent CTA offers."
                )
                score = int((1.0 - conversion_rate) * 80)
                priority_level = self._get_priority_level(score)
                backlog_items.append(BacklogItem(
                    id=f"backlog-cta-{hash(url) % 1000}",
                    title=f"CTA Placement & Design Optimization on '{title}'",
                    description=desc,
                    priority_level=priority_level,
                    priority_score=score,
                    category="CTA optimization",
                    target_url=url
                ))

        # 2. Opportunities from A/B winning recommendations (Feature expansion/automation)
        for win in ab_summary.winning_variations:
            desc = (
                f"Based on Optimizely experiment results, winning variation '{win['winning_variation']}' "
                f"improved conversions by {win['improvement_percent']}%. Build automated, "
                f"data-driven features around this personalization logic."
            )
            score = int(min(win["improvement_percent"], 100))
            priority_level = self._get_priority_level(score)
            backlog_items.append(BacklogItem(
                id=f"backlog-feature-{hash(win['experiment_id']) % 1000}",
                title=f"Automate personalization logic for '{win['experiment_name']}'",
                description=desc,
                priority_level=priority_level,
                priority_score=score,
                category="New Feature"
            ))

        # Ensure we always return at least some default backlog items if metrics are healthy
        if not backlog_items:
            backlog_items.append(BacklogItem(
                id="backlog-default-1",
                title="Continuous Content Quality Audit",
                description="Conduct bi-weekly reviews of high-performing assets to reverse engineer winning elements.",
                priority_level="Medium",
                priority_score=45,
                category="Content Audit"
            ))

        # Sort by priority score descending
        backlog_items.sort(key=lambda x: x.priority_score, reverse=True)
        return backlog_items

    def _get_priority_level(self, score: int) -> str:
        if score >= 80:
            return "Critical"
        elif score >= 60:
            return "High"
        elif score >= 40:
            return "Medium"
        else:
            return "Low"

    def _create_linear_issues(self, backlog_items: List[BacklogItem]) -> List[BacklogItem]:
        """Step 8: Create Linear issues for high-priority items."""
        updated_items = []
        for item in backlog_items:
            # Map priority level to Linear priority integer (1=Urgent, 2=High, 3=Medium, 4=Low)
            priority_map = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4}
            lin_priority = priority_map.get(item.priority_level, 0)

            # Create the issue in Linear
            linear_issue = self.linear.create_issue(
                title=f"[{item.category}] {item.title}",
                description=item.description,
                priority=lin_priority,
                labels=["growth", "content-iteration"]
            )

            # Record the Linear issue URL back into the backlog item
            item.linear_issue_url = linear_issue.get("url")
            updated_items.append(item)

        return updated_items

    def _create_github_issue(
        self,
        weekly_report: WeeklyAnalyticsReport,
        ab_summary: ABTestResultsSummary,
        backlog_items: List[BacklogItem],
        inputs: AgentInputs
    ) -> str:
        """Step 9: Compile a detailed GitHub issue detailing all findings and recommendations."""
        title = "Weekly Content Performance Analytics & Prioritized Backlog"

        # Format the backlog list with priority labels and Linear links
        backlog_markdown = []
        for item in backlog_items:
            lin_link = f"([Linear Issue]({item.linear_issue_url}))" if item.linear_issue_url else ""
            backlog_markdown.append(
                f"- **{item.title}** {lin_link}\n"
                f"  - **Category**: {item.category} | **Priority**: {item.priority_level} (Score: {item.priority_score}/100)\n"
                f"  - **Description**: {item.description}\n"
                f"  - **Target Page**: {item.target_url or 'N/A'}"
            )
        backlog_list_str = "\n".join(backlog_markdown)

        # Format high-performing and underperforming URLs
        high_perf_str = "\n".join([f"- {url}" for url in weekly_report.high_performing_urls]) or "- None"
        under_perf_str = "\n".join([f"- {url}" for url in weekly_report.underperforming_urls]) or "- None"

        # Format experiment recommendations
        rec_str = "\n".join([f"- {rec}" for rec in ab_summary.actionable_recommendations]) or "- No recommendations"

        body = f"""# PersonaScript Content Performance Iteration Report

## Goal
Continuously monitor user engagement and content performance metrics, analyze data to identify content iteration opportunities, and propose data-driven feature backlog items to enhance lead conversion and brand consistency.

## Analysis Period
- **Start Date**: {inputs.start_date}
- **End Date**: {inputs.end_date}

## 📊 Weekly Analytics Report
{weekly_report.summary}

### High-Performing Content Assets
{high_perf_str}

### Underperforming Content Assets (Iteration Opportunities)
{under_perf_str}

## 🧪 A/B Test Results Summary
{ab_summary.summary}

### Actionable Experiment Recommendations
{rec_str}

## 📋 Prioritized Feature & Content Backlog
These items have been automatically created and tracked in Linear:

{backlog_list_str}

---
*Report compiled automatically by PersonaScriptContentIterationAgent on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC.*
"""
        issue_url = self.github.create_issue(
            title=title,
            body=body,
            labels=["content-performance", "backlog", "analytics"]
        )
        return issue_url
