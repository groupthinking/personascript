"""
PersonaScriptFrontendUIAgent - Agent for generating detailed technical blueprints
for the frontend user interface of the PersonaScript content application.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from ..integrations.github_integration import GitHubIntegration

logger = logging.getLogger(__name__)


@dataclass
class FrontendUIInputs:
    """Input data for the PersonaScriptFrontendUIAgent."""

    specifications: List[str] = field(default_factory=lambda: ["content generation", "brief creation", "content management"])
    target_stack: Dict[str, str] = field(default_factory=lambda: {
        "framework": "Next.js (App Router)",
        "language": "TypeScript",
        "styling": "Tailwind CSS",
        "ui_library": "Chakra UI / Headless UI"
    })
    additional_notes: Optional[str] = None


@dataclass
class FrontendUIOutputs:
    """Output data from the PersonaScriptFrontendUIAgent."""

    github_issue_url: str
    blueprint_title: str
    blueprint_body: str


class PersonaScriptFrontendUIAgent:
    """
    Agent class for formulating and publishing a detailed technical blueprint
    for the PersonaScript Frontend User Interface.
    """

    def __init__(
        self,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """
        Initialize the FrontendUIAgent.

        Args:
            github_token: Token for GitHub API
            github_repo: Repository name (format: "owner/repo")
        """
        self.github_integration = GitHubIntegration(token=github_token, repo=github_repo)
        logger.info("PersonaScriptFrontendUIAgent initialized")

    def execute(self, inputs: FrontendUIInputs) -> FrontendUIOutputs:
        """
        Executes the internal analysis, generates the detailed technical blueprint,
        and posts it as a GitHub issue.

        Args:
            inputs: Configured FrontendUIInputs with specifications and tech stack.

        Returns:
            FrontendUIOutputs containing the issue URL and the blueprint content.
        """
        logger.info("Executing FrontendUIAgent analysis and blueprint generation")

        # Parse inputs internally
        specs = [s.lower() for s in inputs.specifications]
        stack = inputs.target_stack

        # Build Title
        title = "Blueprint: PersonaScript Frontend User Interface Technical Specification"

        # Build Body
        body = self._generate_blueprint_markdown(specs, stack, inputs.additional_notes)

        # Create GitHub Issue
        github_issue_url = self.github_integration.create_issue(
            title=title,
            body=body,
            labels=["frontend-ui", "technical-blueprint", "proposal"]
        )

        return FrontendUIOutputs(
            github_issue_url=github_issue_url,
            blueprint_title=title,
            blueprint_body=body
        )

    def _generate_blueprint_markdown(
        self,
        specs: List[str],
        stack: Dict[str, str],
        additional_notes: Optional[str]
    ) -> str:
        """Generates a structured markdown blueprint for the frontend UI."""

        framework = stack.get("framework", "Next.js")
        language = stack.get("language", "TypeScript")
        styling = stack.get("styling", "Tailwind CSS")
        ui_lib = stack.get("ui_library", "Chakra UI")

        markdown_parts = [
            f"# PersonaScript Frontend UI Technical Blueprint",
            "",
            "## Goal",
            "Establish a highly robust, scalable, and responsive frontend user interface technical blueprint for the PersonaScript content application. This specification acts as a foundational architecture guide for building features around high-volume, hyper-personalized, and brand-aligned content generation.",
            "",
            "## Inputs Processed",
            f"- **Core UI Capabilities Required**: {', '.join(specs)}",
            f"- **Target Technology Stack**:",
            f"  - **Framework**: {framework}",
            f"  - **Language**: {language}",
            f"  - **Styling**: {styling}",
            f"  - **UI / Component Library**: {ui_lib}",
            ""
        ]

        if additional_notes:
            markdown_parts.extend([
                "### Additional Notes",
                additional_notes,
                ""
            ])

        markdown_parts.extend([
            "## Expected Outputs",
            "1. **Modern, Responsive Frontend Layout** with multi-pane workspace panels.",
            "2. **State Management Flow** utilizing React Context/Zustand and React Query for asynchronous server state synchronization.",
            "3. **Component Hierarchy Design** categorized into Content Generation, Brief Creation, and Content Management.",
            "",
            "---",
            "",
            "## Detailed Technical Blueprint Specification",
            "",
            "### 1. Technology Stack and Architecture Configuration",
            "The architecture adopts **Next.js (App Router)** as the primary meta-framework, ensuring superior performance through Server Components (RSC) and Client Components (RCC) where interactive states are needed.",
            "",
            f"```text",
            f"Frontend Stack Details:",
            f"├── Framework: {framework}",
            f"├── Type System: {language} (strict mode enabled)",
            f"├── Styling: {styling} utilities for ultra-custom layouts",
            f"└── Component Library: {ui_lib} (accessible and fully styleable)",
            f"```",
            "",
            "#### Root Directory Structure Proposed:",
            "```text",
            "src/",
            "├── app/                   # Next.js App Router (pages & layouts)",
            "│   ├── layout.tsx         # Global Shell Layout & Providers",
            "│   ├── page.tsx           # Dashboard / Analytics home",
            "│   ├── content/           # Content Generation routes",
            "│   ├── briefs/            # Brief Creation routes",
            "│   └── management/        # Content Management dashboard",
            "├── components/            # Reusable core/ui components",
            "│   ├── ui/                # Base atoms (buttons, inputs, modals)",
            "│   └── workspace/         # Complex context-specific components",
            "├── hooks/                 # Custom React hooks (useContent, useBriefs)",
            "├── state/                 # State managers (Zustand store definitions)",
            "├── types/                 # Unified TypeScript interfaces",
            "└── utils/                 # API helpers, formatters, and theme settings",
            "```",
            "",
            "---",
            "",
            "### 2. Core UI Workspaces Specifications",
            ""
        ])

        # Spec 1: Content Generation Interface
        markdown_parts.extend([
            "#### A. Content Generation Workspace Interface",
            "**Purpose**: Empower marketers to easily prompt, trigger, view, and edit generated content in real-time.",
            "",
            "**Key UI Components & Layouts**:",
            "- **Multi-pane Layout**: A split-screen environment. Left panel for control prompts & configuration, right panel for the live editor and AI-output feedback.",
            "- **Control Sidebar**:",
            "  - **Persona Selector**: Dropdown to choose target personas (e.g., Sarah - VP of Marketing).",
            "  - **Funnel Stage Selector**: Segmented controls (Awareness, Consideration, Decision).",
            "  - **Brand Alignment Dial**: Sliders to tune creativity level vs. rigid brand guideline compliance.",
            "  - **Generation Parameters**: Text inputs for custom instructions/keywords, and output length selection.",
            "- **Interactive Canvas Editor**:",
            "  - Rich text editor area supporting markdown export, text formatting (headings, lists, quotes), and inline AI assistant tools (e.g., 'Make it punchier', 'Elaborate', 'Simplify').",
            "  - **Refinement Logs**: A collapsible history panel showing previous prompt iterations and variations.",
            "",
            "---",
            ""
        ])

        # Spec 2: Brief Creation Interface
        markdown_parts.extend([
            "#### B. Brief Creation & Formatting Workspace",
            "**Purpose**: Streamline content outline drafting and objective definition before initiating full-scale automated writing.",
            "",
            "**Key UI Components & Layouts**:",
            "- **Interactive Brief Questionnaire**: Step-by-step wizard capturing target audience parameters, primary keywords, competitor URLs, and secondary call-to-actions (CTAs).",
            "- **Structured Outline Builder**: A drag-and-drop hierarchy visualizer allowing users to structure headings (H1, H2, H3), re-order sections, and append specific instructions to individual sections.",
            "- **Template Repository Selector**: Visual card grid of pre-built briefing structures (e.g., 'Standard Case Study Brief', 'SEO-Optimized Blog Brief', 'Direct Response Email Outline').",
            "- **Real-time Scoring Widget**: Sidebar indicator evaluating SEO strength, clarity, and target audience alignment dynamically as the brief details are entered.",
            "",
            "---",
            ""
        ])

        # Spec 3: Content Management & Analytics Dashboard
        markdown_parts.extend([
            "#### C. Content Management Dashboard",
            "**Purpose**: Provide an administrative workspace to list, organize, archive, filter, and track conversion analytics of generated pieces.",
            "",
            "**Key UI Components & Layouts**:",
            "- **Content Hub Table**: Data grid with multi-column sorting and virtualized scroll support.",
            "  - **Columns**: Title, Persona, Funnel Stage, Creation Date, Word Count, Brand Alignment Score, Status Tag (Draft, AI-Generated, Reviewed, Published).",
            "  - **Filtering Panel**: Collapsible drawer offering faceted filters (by persona, content format, author, creation date range).",
            "- **Analytics Highlight Cards**: Top row displaying high-level performance indicators:",
            "  - Total Generated Words, Average Quality Rating, Projected Lead Conversion Rate, Content Pipeline Velocity.",
            "- **Bulk Action Toolbar**: Bottom sticky bar appearing upon selecting rows, enabling bulk operations like 'Export as Markdown/PDF', 'Bulk Publish to CMS', or 'Add to Brief Collection'.",
            "",
            "---",
            "",
            "### 3. State Management & API Contract Details",
            "To guarantee seamless multi-page sync and snappy user interactions, the following state and data layers are proposed:",
            "- **Global Store (Zustand)**: Controls lightweight client UI state (sidebar collapse state, dark/light theme options, currently active persona/brief profile).",
            "- **Server State Sync (React Query)**: Caches API response payloads for content generation endpoints. Supports optimistic UI updates and robust re-fetching strategies.",
            "- **TypeScript Model Definitions**:",
            "```typescript",
            "export interface Persona {",
            "  id: string;",
            "  name: string;",
            "  role: string;",
            "  goals: string[];",
            "  painPoints: string[];",
            "}",
            "",
            "export interface ContentBrief {",
            "  id: string;",
            "  title: string;",
            "  personaId: string;",
            "  funnelStage: 'awareness' | 'consideration' | 'decision';",
            "  targetKeywords: string[];",
            "  sections: string[];",
            "  status: 'draft' | 'completed';",
            "}",
            "",
            "export interface GeneratedContent {",
            "  id: string;",
            "  briefId: string;",
            "  title: string;",
            "  body: string;",
            "  personaName: string;",
            "  funnelStage: string;",
            "  brandScore: number;",
            "  createdAt: string;",
            "  status: 'draft' | 'generated' | 'reviewed' | 'published';",
            "}",
            "```",
            "",
            "---",
            "",
            "## Implementation Milestones",
            "1. **Milestone 1**: Project bootstrap with TypeScript configuration, tailwind setup, custom theme components, and initial layout routing structure.",
            "2. **Milestone 2**: Build out Brief Creation wizard UI flow and hook it up to mock schemas.",
            "3. **Milestone 3**: Develop Content Generation workspace with rich-text canvas and control sidebar interactive controls.",
            "4. **Milestone 4**: Finalize Content Management database table with full client-side searching, sorting, and pagination capabilities.",
            "",
            "## Next Steps",
            "- Approve this detailed technical specification.",
            "- Assign milestones to relevant frontend engineers.",
            "- Initiate repository scaffolding.",
            ""
        ])

        return "\n".join(markdown_parts)
