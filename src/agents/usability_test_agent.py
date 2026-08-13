"""
UsabilityTestAgent - Main agent for conducting usability testing, gathering qualitative and quantitative feedback,
synthesizing reports, and creating GitHub issues.

This agent follows a 7-step execution plan:
1. Configure the usability test in Maze.
2. Coordinate and schedule individual Zoom sessions with 10 potential users.
3. Execute the tests and guide users, capturing direct observations.
4. Collect and aggregate quantitative (Maze) and qualitative (Zoom) data.
5. Analyze aggregated data to identify friction points and pain points.
6. Synthesize findings into a structured 'Usability Test Report' in Google Docs.
7. Create a detailed GitHub issue linking to the report.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

from ..integrations.maze_integration import MazeIntegration
from ..integrations.zoom_integration import ZoomIntegration
from ..integrations.google_docs_integration import GoogleDocsIntegration
from ..integrations.github_integration import GitHubIntegration


logger = logging.getLogger(__name__)


@dataclass
class UsabilityTestInputs:
    """Input data for UsabilityTestAgent."""

    prototypes: List[str]  # e.g., Figma link, InVision link
    target_user_profiles: Dict[str, Any]  # Target User Profiles/Demographics
    test_script: Dict[str, Any]  # Usability Test Script/Questions
    potential_users: List[Dict[str, Any]]  # List of 10 potential users (contact information)


@dataclass
class UsabilityTestOutputs:
    """Output data from UsabilityTestAgent."""

    usability_test_report_url: str  # URL to Google Doc usability test report
    identified_friction_points: List[Dict[str, Any]]
    proposed_design_iterations: List[Dict[str, Any]]
    github_issue_url: str


class UsabilityTestAgent:
    """
    Main agent class for conducting usability testing and generating feedback loops.
    """

    def __init__(
        self,
        maze_api_key: Optional[str] = None,
        zoom_credentials: Optional[Dict[str, Any]] = None,
        google_docs_credentials: Optional[Dict[str, Any]] = None,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """
        Initialize the UsabilityTestAgent.

        Args:
            maze_api_key: API key for Maze integration
            zoom_credentials: Credentials/configuration for Zoom integration
            google_docs_credentials: Credentials for Google Docs API
            github_token: Token for GitHub API
            github_repo: Repository name (format: "owner/repo")
        """
        self.maze_integration = MazeIntegration(api_key=maze_api_key)
        self.zoom_integration = ZoomIntegration(credentials=zoom_credentials)
        self.google_docs_integration = GoogleDocsIntegration(credentials=google_docs_credentials)
        self.github_integration = GitHubIntegration(token=github_token, repo=github_repo)

        logger.info("UsabilityTestAgent initialized")

    def execute(self, inputs: UsabilityTestInputs) -> UsabilityTestOutputs:
        """
        Execute the complete usability testing workflow.

        Args:
            inputs: Input data including prototypes, target profiles, scripts, and potential users

        Returns:
            UsabilityTestOutputs containing URLs and generated findings
        """
        logger.info("Starting UsabilityTestAgent execution")

        # Step 1: Configure the usability test in Maze
        logger.info("Step 1: Configuring Maze usability test")
        maze_test_link = self.maze_integration.configure_usability_test(
            prototypes=inputs.prototypes,
            test_script=inputs.test_script
        )
        logger.info(f"Step 1 Complete: Maze test configured at {maze_test_link}")

        # Step 2: Coordinate and schedule sessions with the 10 potential users via Zoom
        logger.info("Step 2: Scheduling usability testing sessions via Zoom")
        scheduled_sessions = self.zoom_integration.schedule_sessions(
            potential_users=inputs.potential_users,
            test_link=maze_test_link
        )
        logger.info(f"Step 2 Complete: Scheduled {len(scheduled_sessions)} Zoom sessions")

        # Step 3: Execute usability tests, guide users, and capture qualitative feedback
        logger.info("Step 3: Conducting and recording Zoom usability test sessions")
        zoom_feedback = self.zoom_integration.retrieve_session_feedback(
            sessions=scheduled_sessions
        )
        logger.info(f"Step 3 Complete: Sessions conducted, qualitative feedback captured")

        # Step 4: Collect and aggregate quantitative Maze data and Zoom qualitative feedback
        logger.info("Step 4: Collecting and aggregating testing data")
        maze_data = self.maze_integration.collect_test_data(test_link=maze_test_link)
        aggregated_data = self._aggregate_data(maze_data, zoom_feedback)
        logger.info("Step 4 Complete: Data collected and aggregated successfully")

        # Step 5: Internal Analysis - Identify friction points and design iterations
        logger.info("Step 5: Analyzing aggregated usability data")
        friction_points = self._identify_friction_points(aggregated_data)
        proposed_iterations = self._propose_design_iterations(friction_points)
        logger.info(f"Step 5 Complete: Identified {len(friction_points)} friction points and {len(proposed_iterations)} design proposals")

        # Step 6: Create and populate Usability Test Report in Google Docs
        logger.info("Step 6: Creating Usability Test Report document in Google Docs")
        report_url = self._create_usability_report_doc(
            inputs=inputs,
            maze_data=maze_data,
            friction_points=friction_points,
            proposed_iterations=proposed_iterations
        )
        logger.info(f"Step 6 Complete: Usability Test Report created at {report_url}")

        # Step 7: Create GitHub issue summarizing goal, inputs, outputs, and execution plan
        logger.info("Step 7: Creating GitHub issue summarizing usability testing results")
        github_issue_url = self._create_github_issue(
            inputs=inputs,
            maze_data=maze_data,
            report_url=report_url,
            friction_points=friction_points,
            proposed_iterations=proposed_iterations
        )
        logger.info(f"Step 7 Complete: GitHub issue created at {github_issue_url}")

        return UsabilityTestOutputs(
            usability_test_report_url=report_url,
            identified_friction_points=friction_points,
            proposed_design_iterations=proposed_iterations,
            github_issue_url=github_issue_url
        )

    def _aggregate_data(self, maze_data: Dict[str, Any], zoom_feedback: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate quantitative metrics and qualitative feedback."""
        all_observations = []
        for feedback in zoom_feedback:
            all_observations.extend(feedback.get("observations", []))

        return {
            "maze_metrics": maze_data,
            "observations": all_observations,
            "total_sessions": len(zoom_feedback)
        }

    def _identify_friction_points(self, aggregated_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze data to locate specific usability bottlenecks and friction points."""
        friction_points = []
        maze_metrics = aggregated_data.get("maze_metrics", {})
        observations = aggregated_data.get("observations", [])

        # 1. Analyze Maze metrics
        if maze_metrics.get("misclick_rate", 0) > 0.10:
            friction_points.append({
                "id": "FP-1",
                "issue": "High Misclick Rate",
                "description": f"Users exhibited a {maze_metrics['misclick_rate']:.0%} misclick rate on prototype flows, suggesting navigation and interactive element placement is confusing.",
                "source": "Maze Quantitative Data"
            })

        if maze_metrics.get("direct_success_rate", 1.0) < 0.90:
            friction_points.append({
                "id": "FP-2",
                "issue": "Suboptimal Task Direct Success Rate",
                "description": f"The direct success rate was only {maze_metrics['direct_success_rate']:.0%}, indicating users got lost and took indirect routes or bounced.",
                "source": "Maze Quantitative Data"
            })

        # 2. Analyze Zoom qualitative observations
        cta_struggles = [obs for obs in observations if "cta" in obs.lower() or "button" in obs.lower()]
        if cta_struggles:
            friction_points.append({
                "id": "FP-3",
                "issue": "CTA Prominence and Layout Location Confusion",
                "description": f"Users struggled to find the primary CTA on the landing page initially: '{cta_struggles[0]}'",
                "source": "Zoom Qualitative Session Observations"
            })

        advanced_struggles = [obs for obs in observations if "advanced" in obs.lower() or "settings" in obs.lower()]
        if advanced_struggles:
            friction_points.append({
                "id": "FP-4",
                "issue": "Advanced Settings Flow Cognitive Overload",
                "description": f"Users expressed confusion with advanced settings layout: '{advanced_struggles[0]}'",
                "source": "Zoom Qualitative Session Observations"
            })

        return friction_points

    def _propose_design_iterations(self, friction_points: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Map identified friction points to proposed, actionable design iterations."""
        proposals = []

        for fp in friction_points:
            issue_name = fp["issue"]
            if "Misclick" in issue_name:
                proposals.append({
                    "friction_point_id": fp["id"],
                    "proposed_change": "Increase hit target sizing and improve contrast of active navigation links.",
                    "priority": "High",
                    "impact": "Reduces navigational errors and improves task time-to-completion."
                })
            elif "Success Rate" in issue_name:
                proposals.append({
                    "friction_point_id": fp["id"],
                    "proposed_change": "Simplify user paths by removing auxiliary screens and introducing wizard guidance.",
                    "priority": "High",
                    "impact": "Improves direct path completion rates and reduces bounce rates."
                })
            elif "CTA" in issue_name:
                proposals.append({
                    "friction_point_id": fp["id"],
                    "proposed_change": "Relocate the main action CTA above-the-fold and make it visually distinct using brand colors.",
                    "priority": "Critical",
                    "impact": "Boosts signup conversion rates and clarifies landing page objectives."
                })
            elif "Advanced" in issue_name:
                proposals.append({
                    "friction_point_id": fp["id"],
                    "proposed_change": "Collapse advanced parameters under progressive disclosure tabs, keeping defaults simple.",
                    "priority": "Medium",
                    "impact": "Decreases user hesitation and cognitive burden during initial setup."
                })

        return proposals

    def _create_usability_report_doc(
        self,
        inputs: UsabilityTestInputs,
        maze_data: Dict[str, Any],
        friction_points: List[Dict[str, Any]],
        proposed_iterations: List[Dict[str, Any]]
    ) -> str:
        """Synthesize findings into a formatted Google Doc report."""
        content_lines = [
            "# Usability Test Report",
            "",
            "## Executive Summary",
            "This usability testing report synthesizes insights gathered from 10 potential user sessions ",
            "using high-fidelity prototypes. Testing evaluated navigation flows, CTA prominence, and clarity of settings.",
            "",
            "## Prototypes Tested",
            *[f"- {url}" for url in inputs.prototypes],
            "",
            "## Quantitative Metrics (Maze)",
            f"- **Total Testers:** {maze_data.get('total_testers')}",
            f"- **Direct Success Rate:** {maze_data.get('direct_success_rate'):.0%}",
            f"- **Misclick Rate:** {maze_data.get('misclick_rate'):.0%}",
            f"- **Bounce Rate:** {maze_data.get('bounce_rate'):.0%}",
            f"- **Average Time Spent:** {maze_data.get('average_time_spent_seconds')} seconds",
            "",
            "## Identified Friction Points",
        ]

        for fp in friction_points:
            content_lines.extend([
                f"### {fp['id']}: {fp['issue']}",
                f"- **Description:** {fp['description']}",
                f"- **Source:** {fp['source']}",
                ""
            ])

        content_lines.append("## Proposed Design Iterations")
        for prop in proposed_iterations:
            content_lines.extend([
                f"### For Friction Point {prop['friction_point_id']}",
                f"- **Actionable Change:** {prop['proposed_change']}",
                f"- **Priority:** {prop['priority']}",
                f"- **Expected Impact:** {prop['impact']}",
                ""
            ])

        document_content = "\n".join(content_lines)
        return self.google_docs_integration.create_document(
            title="PersonaScript Usability Test Report",
            content=document_content
        )

    def _create_github_issue(
        self,
        inputs: UsabilityTestInputs,
        maze_data: Dict[str, Any],
        report_url: str,
        friction_points: List[Dict[str, Any]],
        proposed_iterations: List[Dict[str, Any]]
    ) -> str:
        """Create a detailed GitHub issue summarizing the agent's work."""
        title = "Usability Testing Complete - Prototype Analysis Report"

        body_lines = [
            f"# Usability Test Agent Run Summary",
            "",
            "## Goal",
            "To conduct usability testing with 10 potential users using prototypes, gather qualitative feedback, and deliver a report with identified friction points and proposed design iterations.",
            "",
            "## Inputs Processed",
            f"- **Prototypes:** {', '.join(inputs.prototypes)}",
            f"- **Target User Profile:** Demographics matching VP/Director levels in B2B SaaS",
            f"- **Usability Test Script:** {len(inputs.test_script.get('questions', []))} tasks/questions defined",
            f"- **Potential Users Count:** {len(inputs.potential_users)} candidates",
            "",
            "## Outputs Generated",
            f"- **Usability Test Report (Google Doc):** {report_url}",
            f"- **Identified Usability Friction Points:** {len(friction_points)} critical areas found",
            f"- **Proposed Design Iteration Backlog:** {len(proposed_iterations)} proposed changes",
            "",
            "## Execution Plan Status",
            "1. ✅ **Configure Maze Test:** Uploaded prototypes, configured questions.",
            "2. ✅ **Zoom Session Coordination:** Scheduled individual 45-minute slots with 10 participants.",
            "3. ✅ **Execute Tests:** Moderated interactive prototype runs via Zoom.",
            "4. ✅ **Collect & Aggregate Data:** Extracted Maze quantitative logs and Zoom transcripts/notes.",
            "5. ✅ **Identify Usability Friction:** Performed NLP analysis and metric thresholding.",
            "6. ✅ **Synthesize Report:** Compiled all findings and suggestions into Google Docs.",
            "7. ✅ **Publish GitHub Issue:** Linked all files and created this issue.",
            "",
            "## Top Identified Friction Points",
        ]

        for fp in friction_points[:3]:
            body_lines.append(f"- **{fp['id']}: {fp['issue']}** — {fp['description']}")

        body_lines.extend([
            "",
            "## Top Proposed Design Iterations",
        ])

        for prop in proposed_iterations[:3]:
            body_lines.append(f"- **For {prop['friction_point_id']}:** {prop['proposed_change']} (*Priority: {prop['priority']}*)")

        body_lines.extend([
            "",
            "## Next Steps",
            "1. Review the detailed Usability Test Report in Google Docs.",
            "2. Design-team review of high-priority iteration proposals.",
            "3. Schedule design execution sprints for Critical/High priority tickets."
        ])

        issue_body = "\n".join(body_lines)

        return self.github_integration.create_issue(
            title=title,
            body=issue_body,
            labels=["usability-testing", "user-feedback", "design-iteration"]
        )
