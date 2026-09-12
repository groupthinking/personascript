"""
PersonaScriptFrontendUIAgent - Agent for generating technical blueprints for the PersonaScript frontend UI.

This agent analyzes frontend UI specifications and technical stack requirements to:
1. Parse task specifications for content generation, brief creation, and content management interfaces.
2. Extract the technology stack requirements (Next.js, TypeScript, Tailwind CSS / Chakra UI).
3. Draft a concise and descriptive issue title.
4. Formulate a detailed technical blueprint and GitHub issue body covering core UI components and setup considerations.
5. Create and publish a GitHub issue containing the technical blueprint and execution summary.
"""

import os
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from ..integrations.github_integration import GitHubIntegration

logger = logging.getLogger(__name__)


@dataclass
class ComponentBlueprint:
    """Represents a component in the frontend UI blueprint."""

    name: str
    description: str
    key_features: List[str]
    tech_details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UIBlueprint:
    """Represents the complete frontend UI technical blueprint."""

    title: str
    tech_stack: Dict[str, str]
    content_generation_components: List[ComponentBlueprint]
    brief_creation_components: List[ComponentBlueprint]
    content_management_components: List[ComponentBlueprint]
    setup_considerations: List[str]


@dataclass
class AgentInputs:
    """Input data for the PersonaScriptFrontendUIAgent."""

    task_specifications: List[str] = field(
        default_factory=lambda: [
            "content generation interface",
            "brief creation interface",
            "content management dashboard"
        ]
    )
    tech_stack: Dict[str, str] = field(
        default_factory=lambda: {
            "framework": "Next.js",
            "language": "TypeScript",
            "styling": "Tailwind CSS / Chakra UI"
        }
    )


@dataclass
class AgentOutputs:
    """Output data from the PersonaScriptFrontendUIAgent."""

    github_issue_url: str
    blueprint: UIBlueprint
    issue_title: str
    issue_body: str
    status: str = "success"
    error_message: Optional[str] = None


class PersonaScriptFrontendUIAgent:
    """
    Agent responsible for generating a technical blueprint for the PersonaScript frontend UI.

    Execution Plan:
    1. Parse input task specifications (content generation, brief creation, content management).
    2. Extract target technology stack (Next.js, TypeScript, Tailwind CSS / Chakra UI).
    3. Draft a concise and descriptive issue title.
    4. Formulate a detailed technical UI blueprint and issue body.
    5. Create a GitHub issue documenting the full blueprint and architecture.
    """

    def __init__(
        self,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """
        Initialize the PersonaScriptFrontendUIAgent.

        Args:
            github_token: GitHub Personal Access Token
            github_repo: Target repository (format: "owner/repo")
        """
        self.github_token = github_token or os.environ.get("GITHUB_TOKEN")
        self.github_repo = github_repo or os.environ.get("GITHUB_REPO", "groupthinking/personascript")
        self.github_integration = GitHubIntegration(token=self.github_token, repo=self.github_repo)

        logger.info("PersonaScriptFrontendUIAgent initialized.")

    def execute(self, inputs: Optional[AgentInputs] = None) -> AgentOutputs:
        """
        Execute the frontend UI blueprint generation workflow.

        Args:
            inputs: Optional AgentInputs containing task specifications and tech stack.

        Returns:
            AgentOutputs containing the GitHub issue URL, structured blueprint, and issue details.
        """
        logger.info("Starting PersonaScriptFrontendUIAgent workflow execution")

        if inputs is None:
            inputs = AgentInputs()

        try:
            # Step 1: Parse the input task specifications
            parsed_specs = self._parse_task_specifications(inputs.task_specifications)

            # Step 2: Extract the specified technology stack
            tech_stack = self._extract_tech_stack(inputs.tech_stack)

            # Step 3: Draft a concise and descriptive title
            issue_title = self._draft_issue_title()

            # Step 4: Formulate the detailed UI blueprint and issue body
            blueprint = self._formulate_ui_blueprint(parsed_specs, tech_stack)
            issue_body = self._formulate_issue_body(
                goal="Generate a detailed technical blueprint for the frontend user interface of the PersonaScript content application, covering content generation, brief creation, and content management, to be documented as a GitHub issue.",
                inputs=inputs,
                blueprint=blueprint
            )

            # Step 5: Create a new GitHub issue
            github_issue_url = self._create_github_issue(issue_title, issue_body)

            logger.info(f"Frontend UI blueprint generated successfully. GitHub Issue URL: {github_issue_url}")

            return AgentOutputs(
                github_issue_url=github_issue_url,
                blueprint=blueprint,
                issue_title=issue_title,
                issue_body=issue_body,
                status="success"
            )

        except Exception as e:
            logger.error(f"Error in PersonaScriptFrontendUIAgent execution: {e}", exc_info=True)
            empty_blueprint = UIBlueprint(
                title="Error Blueprint",
                tech_stack={},
                content_generation_components=[],
                brief_creation_components=[],
                content_management_components=[],
                setup_considerations=[]
            )
            return AgentOutputs(
                github_issue_url="",
                blueprint=empty_blueprint,
                issue_title="Frontend UI Blueprint Generation Failed",
                issue_body="",
                status="error",
                error_message=str(e)
            )

    def _parse_task_specifications(self, specifications: List[str]) -> Dict[str, Any]:
        """
        Step 1: Parse input task specifications to identify required core UI modules.

        Args:
            specifications: Raw list of task specifications.

        Returns:
            Structured dictionary of parsed UI feature modules.
        """
        logger.info("Step 1: Parsing task specifications")

        modules = {
            "content_generation": False,
            "brief_creation": False,
            "content_management": False,
            "raw_specs": specifications
        }

        for spec in specifications:
            spec_lower = spec.lower()
            if "generation" in spec_lower:
                modules["content_generation"] = True
            if "brief" in spec_lower:
                modules["brief_creation"] = True
            if "management" in spec_lower or "dashboard" in spec_lower or "repository" in spec_lower:
                modules["content_management"] = True

        # Ensure default coverage if empty or ambiguous specs provided
        if not any([modules["content_generation"], modules["brief_creation"], modules["content_management"]]):
            modules["content_generation"] = True
            modules["brief_creation"] = True
            modules["content_management"] = True

        return modules

    def _extract_tech_stack(self, tech_stack_input: Dict[str, str]) -> Dict[str, str]:
        """
        Step 2: Extract and normalize the target technology stack.

        Args:
            tech_stack_input: Dictionary of target tech stack.

        Returns:
            Normalized technology stack configuration.
        """
        logger.info("Step 2: Extracting technology stack specifications")

        return {
            "framework": tech_stack_input.get("framework", "Next.js (App Router v14+)"),
            "language": tech_stack_input.get("language", "TypeScript (v5+)"),
            "styling": tech_stack_input.get("styling", "Tailwind CSS / Chakra UI"),
            "state_management": tech_stack_input.get("state_management", "Zustand / React Query (TanStack Query v5)"),
            "component_library": tech_stack_input.get("component_library", "Radix UI Primitives / Chakra UI / Shadcn UI")
        }

    def _draft_issue_title(self) -> str:
        """
        Step 3: Draft a concise and descriptive title for the GitHub issue.

        Returns:
            Issue title string.
        """
        logger.info("Step 3: Drafting issue title")
        return "Frontend UI Blueprint: PersonaScript Next.js Application Specifications"

    def _formulate_ui_blueprint(
        self,
        parsed_specs: Dict[str, Any],
        tech_stack: Dict[str, str]
    ) -> UIBlueprint:
        """
        Step 4a: Formulate detailed component blueprints for content generation, brief creation, and content management.

        Args:
            parsed_specs: Parsed task specifications.
            tech_stack: Normalized tech stack.

        Returns:
            Populated UIBlueprint object.
        """
        logger.info("Step 4a: Formulating structured UI component blueprint")

        # 1. Content Generation Components
        gen_components = [
            ComponentBlueprint(
                name="FunnelStageSelector & AudienceConfigurator",
                description="Interactive control panel enabling marketers to select target sales funnel stages and inject persona parameters into the AI generation pipeline.",
                key_features=[
                    "Radio group / Segmented control for Awareness, Consideration, and Decision funnel stages",
                    "Dropdown selector for saved buyer persona profiles (e.g., Demand Gen Director, Content Manager)",
                    "Toggle controls for psychographic pain point injection and dynamic CTA aggressiveness",
                    "Tone and voice slider adjustments (e.g., Formal <-> Conversational)"
                ],
                tech_details={"component_type": "Client Component ('use client')", "state": "Local Zustand store"}
            ),
            ComponentBlueprint(
                name="DynamicPromptEditor & VariantGenerator",
                description="Rich text prompt input area with dynamic variable tag pill injection and multi-stage generation controls.",
                key_features=[
                    "Tag auto-complete pill system for inserting dynamic merge fields like {{company_name}} and {{industry}}",
                    "Real-time token counter and estimated generation latency indicator",
                    "One-click single & batch variation generation trigger buttons",
                    "Prompt preset dropdown to load pre-configured high-converting B2B templates"
                ],
                tech_details={"component_type": "Client Component", "input_parsing": "Regex token parser"}
            ),
            ComponentBlueprint(
                name="StreamingContentPreview & VariantEditor",
                description="Live streaming output viewer showing generated copy variations with real-time editing and side-by-side comparison.",
                key_features=[
                    "Server-sent events (SSE) streaming viewer using Vercel AI SDK / Fetch API ReadableStream",
                    "Side-by-side multi-variant comparison view tab system",
                    "Inline WYSIWYG markdown editor with history undo/redo support",
                    "One-click copy to clipboard and export to brief/draft options"
                ],
                tech_details={"component_type": "Client Component", "streaming_protocol": "SSE / Fetch Stream"}
            ),
            ComponentBlueprint(
                name="BatchGenerationMatrixPanel",
                description="Bulk content generation hub for scaling multi-prospect personalized campaign copy from CSV uploads.",
                key_features=[
                    "Drag-and-drop CSV file uploader for prospect details",
                    "Column mapping modal interface to bind CSV headers to prompt placeholders",
                    "Batch generation progress bar with error isolation and pause/resume triggers",
                    "Bulk export trigger in structured CSV or ZIP formats"
                ],
                tech_details={"component_type": "Client Component", "worker": "Web Worker for CSV parsing"}
            )
        ]

        # 2. Brief Creation Components
        brief_components = [
            ComponentBlueprint(
                name="BriefBuilderForm",
                description="Multi-step wizard for configuring high-converting content briefs with target parameters.",
                key_features=[
                    "Step 1: Campaign details (Title, Content Type, Funnel Stage, Target Audience)",
                    "Step 2: Brand voice & tone selection using visual slider controls",
                    "Step 3: Core messaging objectives, key value propositions, and CTA requirements",
                    "Step 4: Supporting research links, competitor references, and asset uploads"
                ],
                tech_details={"component_type": "Client Component", "form_library": "React Hook Form + Zod"}
            ),
            ComponentBlueprint(
                name="PersonaPsychographicSelector",
                description="Target buyer segment configuration widget for linking custom buyer attributes into the brief.",
                key_features=[
                    "Interactive persona card grid showing demographic, firmographic, and psychographic cards",
                    "Checkbox selector for key pain points and primary motivations to emphasize in the brief",
                    "Custom trigger tag builder for emerging buyer objections",
                    "Quick-preview drawer for full persona profile details"
                ],
                tech_details={"component_type": "Client Component", "ui_pattern": "Modal / Slide-over Drawer"}
            ),
            ComponentBlueprint(
                name="SEOKeywordConfigurator",
                description="Search engine optimization and content parameters configuration panel.",
                key_features=[
                    "Primary and secondary keyword input with difficulty/volume badge indicators",
                    "Target word count range slider (e.g., 800 - 1,500 words)",
                    "Search intent classification selector (Informational, Commercial, Transactional)",
                    "Automated internal linking recommendations list"
                ],
                tech_details={"component_type": "Client Component", "badges": "Tailwind / Chakra Badge Components"}
            ),
            ComponentBlueprint(
                name="BriefPreviewAndApprovalPanel",
                description="Comprehensive brief summary view with stakeholder review, approval workflow, and export options.",
                key_features=[
                    "Formatted document-style preview of the compiled brief",
                    "Comment and feedback annotation sidebar",
                    "One-click 'Approve & Send to Generation Engine' action button",
                    "Export to PDF, Google Docs, or Notion page"
                ],
                tech_details={"component_type": "Server & Client Component", "rendering": "Next.js Server Component"}
            )
        ]

        # 3. Content Management Components
        mgmt_components = [
            ComponentBlueprint(
                name="ContentRepositoryTable",
                description="Central searchable, filterable repository of generated content assets and briefs.",
                key_features=[
                    "Paginated data table listing title, channel, persona, created date, and status",
                    "Multi-select bulk actions (Export, Delete, Re-generate, Change Status)",
                    "Quick-view drawer for inspecting full content text without navigating away",
                    "Sorting controls by score, date, title, and engagement metrics"
                ],
                tech_details={"component_type": "Client Component", "table_library": "TanStack Table v8"}
            ),
            ComponentBlueprint(
                name="WorkflowPipelineBoard",
                description="Kanban-style visual workflow board tracking content asset progression.",
                key_features=[
                    "Kanban columns for Draft, Under Review, Approved, Scheduled, and Published",
                    "Drag-and-drop card movement across pipeline stages",
                    "Assignee avatar chips and due date status indicators",
                    "Quick filters by funnel stage, channel, and assignee"
                ],
                tech_details={"component_type": "Client Component", "drag_and_drop": "@hello-pangea/dnd or dnd-kit"}
            ),
            ComponentBlueprint(
                name="BrandAdherenceWidget",
                description="Analytics widget showing real-time brand voice score and style compliance metrics.",
                key_features=[
                    "Radial score meter displaying overall Brand Adherence Score (0-100%)",
                    "Banned words and terminology infraction alert list with inline highlighting",
                    "One-click 'Auto-Fix Brand Style' optimization trigger",
                    "Historical brand adherence trend graph across recent content batches"
                ],
                tech_details={"component_type": "Client Component", "charts": "Recharts / Chart.js"}
            ),
            ComponentBlueprint(
                name="ContentFilterAndSearchPanel",
                description="Global search bar and faceted filter drawer for finding marketing collateral.",
                key_features=[
                    "Instant fuzzy search across title, body, keywords, and persona tags",
                    "Faceted filters for Content Type (Email, Blog, Social, Ad), Funnel Stage, and Persona",
                    "Date range picker for campaign period selection",
                    "Saved search filters preset bar"
                ],
                tech_details={"component_type": "Client Component", "search_debounce": "useDebounce hook (300ms)"}
            )
        ]

        # Setup considerations
        setup_considerations = [
            "Next.js App Router Architecture: Organize code under `/app/(dashboard)` layout with nested route handlers for `/generation`, `/briefs`, and `/content`.",
            "TypeScript Strict Mode: Define strict interfaces in `src/types/content.ts`, `src/types/brief.ts`, and `src/types/persona.ts`.",
            "Styling & UI Components: Configure Tailwind CSS v3 with dynamic color tokens, dark mode support, and Radix UI primitives / Chakra UI component tokens.",
            "State Management & Data Fetching: Utilize Zustand for UI state management (e.g., active filters, drawer toggles) and TanStack React Query v5 for API caching, optimistic updates, and background refetching.",
            "Streaming UI Updates: Implement Server-Sent Events (SSE) / Vercel AI SDK integration for low-latency streaming of AI-generated content variations.",
            "Form Management: Use React Hook Form with Zod schemas for robust client-side validation across brief and generation forms."
        ]

        return UIBlueprint(
            title="PersonaScript Next.js Frontend Application Blueprint",
            tech_stack=tech_stack,
            content_generation_components=gen_components,
            brief_creation_components=brief_components,
            content_management_components=mgmt_components,
            setup_considerations=setup_considerations
        )

    def _formulate_issue_body(
        self,
        goal: str,
        inputs: AgentInputs,
        blueprint: UIBlueprint
    ) -> str:
        """
        Step 4b: Formulate the detailed Markdown body for the GitHub issue.

        Args:
            goal: Summary of the agent's goal.
            inputs: AgentInputs object.
            blueprint: UIBlueprint object.

        Returns:
            Formatted issue body string.
        """
        logger.info("Step 4b: Formulating GitHub issue body markdown")

        # Format component lists
        gen_md = self._format_component_section(blueprint.content_generation_components)
        brief_md = self._format_component_section(blueprint.brief_creation_components)
        mgmt_md = self._format_component_section(blueprint.content_management_components)
        setup_md = "\n".join([f"- {item}" for item in blueprint.setup_considerations])

        tech_stack_md = "\n".join([f"- **{k.replace('_', ' ').title()}**: `{v}`" for k, v in blueprint.tech_stack.items()])

        return f"""# {blueprint.title}

## 🎯 Goal
{goal}

---

## 📥 Inputs Processed
- **Task Specifications**:
  - `{inputs.task_specifications}`
- **Target Technology Stack**:
{tech_stack_md}

---

## 📤 Outputs
- Detailed frontend architecture specification and component blueprint.
- Structured breakdown covering Content Generation, Brief Creation, and Content Management.
- Initial setup considerations for Next.js, TypeScript, and Tailwind CSS / Chakra UI styling.

---

## 🛠️ Detailed Frontend UI Blueprint

### 1. Content Generation Interface Components (`/app/generation`)
{gen_md}

### 2. Brief Creation Interface Components (`/app/briefs`)
{brief_md}

### 3. Content Management Dashboard Components (`/app/content`)
{mgmt_md}

---

## 🏗️ Initial Setup Considerations & Architecture

{setup_md}

### Directory Structure Recommendation (Next.js App Router)
```text
app/
├── (auth)/
│   ├── login/page.tsx
│   └── layout.tsx
├── (dashboard)/
│   ├── layout.tsx
│   ├── page.tsx                      # Dashboard Overview
│   ├── generation/
│   │   ├── page.tsx                  # Content Generation Studio
│   │   └── batch/page.tsx            # Batch Generation Matrix
│   ├── briefs/
│   │   ├── page.tsx                  # Brief Management
│   │   ├── create/page.tsx           # Brief Creation Wizard
│   │   └── [id]/page.tsx             # Brief Preview & Approval
│   └── content/
│       ├── page.tsx                  # Content Repository Table
│       ├── pipeline/page.tsx         # Kanban Board View
│       └── [id]/page.tsx             # Content Detail & Adherence Audit
components/
├── ui/                               # Base design system primitives (Buttons, Inputs, Modals)
├── generation/                       # Content Generation components
├── briefs/                           # Brief Creation components
├── content/                          # Content Management components
└── shared/                           # Navigation, Sidebar, Header
lib/
├── api/                              # REST & GraphQL client fetchers
├── hooks/                            # Custom React hooks (useStreamingGeneration, useDebounce)
└── stores/                           # Zustand state stores
types/
├── content.ts                        # Content & Asset TypeScript interfaces
├── brief.ts                          # Brief & Campaign TypeScript interfaces
└── persona.ts                        # Persona & Psychographic trigger types
```

---

## 📋 Execution Summary & Steps Identified
1. ✅ **Parsed Input Specifications**: Identified core modules for Content Generation, Brief Creation, and Content Management.
2. ✅ **Extracted Tech Stack**: Configured Next.js, TypeScript, Tailwind CSS / Chakra UI, and state management frameworks.
3. ✅ **Drafted Issue Title**: Established descriptive title for repository tracking.
4. ✅ **Formulated Technical Blueprint**: Designed 12 detailed component specifications and directory architecture.
5. ✅ **Published GitHub Issue**: Documented frontend technical blueprint for development team execution.
"""

    def _format_component_section(self, components: List[ComponentBlueprint]) -> str:
        """Format a list of ComponentBlueprint items into Markdown."""
        lines = []
        for comp in components:
            lines.append(f"#### 🧩 `{comp.name}`")
            lines.append(f"**Description**: {comp.description}\n")
            lines.append("**Key Features**:")
            for feature in comp.key_features:
                lines.append(f"- {feature}")
            if comp.tech_details:
                tech_str = ", ".join([f"{k}: `{v}`" for k, v in comp.tech_details.items()])
                lines.append(f"\n**Tech Implementation**: {tech_str}")
            lines.append("")
        return "\n".join(lines)

    def _create_github_issue(self, title: str, body: str) -> str:
        """
        Step 5: Create a new GitHub issue in the repository.

        Args:
            title: Title of the issue.
            body: Body of the issue in markdown format.

        Returns:
            URL of the created GitHub issue.
        """
        logger.info("Step 5: Publishing GitHub issue via GitHub API integration")

        issue_url = self.github_integration.create_issue(
            title=title,
            body=body,
            labels=["frontend-ui", "blueprint", "nextjs", "typescript", "architecture"]
        )
        return issue_url
