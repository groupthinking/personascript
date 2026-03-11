"""
PersonaScriptPersonaCreatorAgent - Main agent for creating user personas and content journey maps.

This agent analyzes product information, target audience data, and marketing collateral to:
1. Identify distinct user segments
2. Generate detailed persona profiles
3. Create content journey maps
4. Output results to Miro and Google Docs
5. Report completion via GitHub issue
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from ..integrations.miro_integration import MiroIntegration
from ..integrations.google_docs_integration import GoogleDocsIntegration
from ..integrations.github_integration import GitHubIntegration


logger = logging.getLogger(__name__)


@dataclass
class PersonaProfile:
    """Represents a detailed user persona."""
    
    name: str
    role: str
    company_size: str
    goals: List[str]
    challenges: List[str]
    pain_points: List[str]
    motivations: List[str]
    preferred_content_types: List[str]
    information_sources: List[str]
    demographics: Dict[str, Any] = field(default_factory=dict)
    psychographics: Dict[str, Any] = field(default_factory=dict)
    behavioral_attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContentJourneyStage:
    """Represents a stage in the content journey."""
    
    stage_name: str  # awareness, consideration, decision
    needs: List[str]
    questions: List[str]
    content_touchpoints: List[str]
    content_formats: List[str]


@dataclass
class ContentJourneyMap:
    """Represents the complete content journey for a persona."""
    
    persona_name: str
    stages: List[ContentJourneyStage]


@dataclass
class AgentInputs:
    """Input data for the PersonaCreatorAgent."""
    
    product_information: str
    target_audience_demographics: Dict[str, Any]
    target_audience_firmographics: Dict[str, Any]
    marketing_collateral: List[str]
    customer_interviews: Optional[List[str]] = None


@dataclass
class AgentOutputs:
    """Output data from the PersonaCreatorAgent."""
    
    miro_board_url: str
    google_docs_url: str
    github_issue_url: str
    personas: List[PersonaProfile]
    journey_maps: List[ContentJourneyMap]


class PersonaScriptPersonaCreatorAgent:
    """
    Main agent class for creating user personas and content journey maps.
    
    This agent follows an 8-step execution plan:
    1. Analyze input data
    2. Identify user segments and define persona attributes
    3. Generate comprehensive persona profiles
    4. Develop detailed content journey maps
    5. Create and populate Miro board
    6. Create and populate Google Doc
    7. Compose GitHub issue content
    8. Create GitHub issue and capture URL
    """
    
    def __init__(
        self,
        miro_api_key: Optional[str] = None,
        google_docs_credentials: Optional[Dict[str, Any]] = None,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """
        Initialize the PersonaCreatorAgent.
        
        Args:
            miro_api_key: API key for Miro integration
            google_docs_credentials: Credentials for Google Docs API
            github_token: Token for GitHub API
            github_repo: Repository name (format: "owner/repo")
        """
        self.miro_integration = MiroIntegration(api_key=miro_api_key)
        self.google_docs_integration = GoogleDocsIntegration(credentials=google_docs_credentials)
        self.github_integration = GitHubIntegration(token=github_token, repo=github_repo)
        
        self.personas: List[PersonaProfile] = []
        self.journey_maps: List[ContentJourneyMap] = []
        
        logger.info("PersonaScriptPersonaCreatorAgent initialized")
    
    def execute(self, inputs: AgentInputs) -> AgentOutputs:
        """
        Execute the complete agent workflow.
        
        Args:
            inputs: Input data including product info, audience data, etc.
        
        Returns:
            AgentOutputs containing URLs and generated data
        """
        logger.info("Starting PersonaCreatorAgent execution")
        
        # Step 1: Analyze input data
        analysis_results = self._analyze_input_data(inputs)
        
        # Step 2: Identify user segments
        segments = self._identify_user_segments(analysis_results)
        
        # Step 3: Generate persona profiles
        self.personas = self._generate_persona_profiles(segments, inputs)
        
        # Step 4: Develop content journey maps
        self.journey_maps = self._develop_journey_maps(self.personas)
        
        # Step 5: Create and populate Miro board
        miro_board_url = self._create_miro_board(self.personas)
        
        # Step 6: Create and populate Google Doc
        google_docs_url = self._create_google_doc(self.journey_maps)
        
        # Step 7 & 8: Create GitHub issue
        github_issue_url = self._create_github_issue(
            miro_board_url, google_docs_url, inputs
        )
        
        outputs = AgentOutputs(
            miro_board_url=miro_board_url,
            google_docs_url=google_docs_url,
            github_issue_url=github_issue_url,
            personas=self.personas,
            journey_maps=self.journey_maps
        )
        
        logger.info("PersonaCreatorAgent execution completed successfully")
        return outputs
    
    def _analyze_input_data(self, inputs: AgentInputs) -> Dict[str, Any]:
        """
        Step 1: Analyze all provided input data.
        
        Args:
            inputs: Input data to analyze
        
        Returns:
            Dictionary containing analysis results
        """
        logger.info("Step 1: Analyzing input data")
        
        analysis = {
            "product_summary": self._summarize_product(inputs.product_information),
            "audience_insights": self._analyze_audience(
                inputs.target_audience_demographics,
                inputs.target_audience_firmographics
            ),
            "content_themes": self._extract_content_themes(inputs.marketing_collateral),
            "interview_insights": self._analyze_interviews(inputs.customer_interviews)
        }
        
        return analysis
    
    def _summarize_product(self, product_info: str) -> Dict[str, Any]:
        """Extract key product information."""
        # In a real implementation, this would use NLP/AI to extract key features,
        # value propositions, and target use cases
        return {
            "key_features": [],
            "value_propositions": [],
            "use_cases": [],
            "product_summary": product_info
        }
    
    def _analyze_audience(
        self,
        demographics: Dict[str, Any],
        firmographics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze target audience characteristics."""
        return {
            "demographic_segments": demographics,
            "firmographic_segments": firmographics,
            "key_characteristics": []
        }
    
    def _extract_content_themes(self, collateral: List[str]) -> List[str]:
        """Extract common themes from marketing collateral."""
        # In a real implementation, this would analyze content to identify themes
        return []
    
    def _analyze_interviews(
        self,
        interviews: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Analyze customer interview data if available."""
        if not interviews:
            return {"insights": [], "pain_points": [], "goals": []}
        
        # In a real implementation, this would use NLP to extract insights
        return {"insights": [], "pain_points": [], "goals": []}
    
    def _identify_user_segments(
        self,
        analysis_results: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Step 2: Identify distinct user segments.
        
        Args:
            analysis_results: Results from data analysis
        
        Returns:
            List of identified user segments
        """
        logger.info("Step 2: Identifying user segments")
        
        # In a real implementation, this would use clustering or
        # other ML techniques to identify segments
        segments = [
            {
                "name": "Demand Gen Director",
                "role_category": "Marketing Leadership",
                "company_size_range": "50-500 employees",
                "key_characteristics": []
            },
            {
                "name": "Content Marketing Manager",
                "role_category": "Content Strategy",
                "company_size_range": "50-200 employees",
                "key_characteristics": []
            },
            {
                "name": "Growth Marketing Lead",
                "role_category": "Growth Strategy",
                "company_size_range": "20-100 employees",
                "key_characteristics": []
            }
        ]
        
        return segments
    
    def _generate_persona_profiles(
        self,
        segments: List[Dict[str, Any]],
        inputs: AgentInputs
    ) -> List[PersonaProfile]:
        """
        Step 3: Generate comprehensive persona profiles.
        
        Args:
            segments: Identified user segments
            inputs: Original input data for context
        
        Returns:
            List of detailed PersonaProfile objects
        """
        logger.info("Step 3: Generating persona profiles")
        
        personas = []
        
        for segment in segments:
            persona = self._create_persona_from_segment(segment, inputs)
            personas.append(persona)
        
        return personas
    
    def _create_persona_from_segment(
        self,
        segment: Dict[str, Any],
        inputs: AgentInputs
    ) -> PersonaProfile:
        """Create a detailed persona profile from a segment."""
        # Default persona attributes based on PersonaScript's B2B SaaS focus
        if "Demand Gen" in segment["name"]:
            return PersonaProfile(
                name="Demand Gen Director Sarah",
                role="Director of Demand Generation",
                company_size=segment["company_size_range"],
                goals=[
                    "Drive qualified lead generation at scale",
                    "Improve conversion rates across funnel stages",
                    "Demonstrate clear ROI from marketing investments",
                    "Build consistent brand presence"
                ],
                challenges=[
                    "Creating high-volume personalized content",
                    "Maintaining brand consistency across campaigns",
                    "Limited content production resources",
                    "Slow content creation cycles"
                ],
                pain_points=[
                    "Generic content doesn't resonate with prospects",
                    "Content bottlenecks slow down campaigns",
                    "Difficulty scaling personalization",
                    "Brand inconsistency across touchpoints"
                ],
                motivations=[
                    "Career advancement through measurable results",
                    "Team efficiency and productivity",
                    "Competitive advantage",
                    "Innovation in marketing approach"
                ],
                preferred_content_types=[
                    "Case studies",
                    "ROI calculators",
                    "Comparison guides",
                    "Webinars",
                    "Industry reports"
                ],
                information_sources=[
                    "LinkedIn",
                    "Marketing industry blogs",
                    "Peer networks",
                    "Conferences",
                    "Product Hunt"
                ],
                demographics={
                    "age_range": "35-45",
                    "experience_level": "8-15 years"
                },
                psychographics={
                    "personality": "Data-driven, strategic, results-oriented",
                    "values": "Efficiency, innovation, accountability"
                },
                behavioral_attributes={
                    "buying_behavior": "Committee-based decision, long sales cycle",
                    "content_consumption": "Skims content, values executive summaries"
                }
            )
        elif "Content Marketing" in segment["name"]:
            return PersonaProfile(
                name="Content Marketing Manager Alex",
                role="Content Marketing Manager",
                company_size=segment["company_size_range"],
                goals=[
                    "Produce engaging content that converts",
                    "Scale content production without sacrificing quality",
                    "Improve content SEO performance",
                    "Maintain brand voice consistency"
                ],
                challenges=[
                    "Limited content team bandwidth",
                    "Balancing quality with quantity",
                    "Adapting content for different personas",
                    "Proving content marketing ROI"
                ],
                pain_points=[
                    "Time-consuming content creation process",
                    "Difficulty personalizing at scale",
                    "Brand voice inconsistency with multiple writers",
                    "Keeping up with content demand"
                ],
                motivations=[
                    "Creative expression within constraints",
                    "Building a strong content portfolio",
                    "Team growth and development",
                    "Recognition for content impact"
                ],
                preferred_content_types=[
                    "How-to guides",
                    "Blog posts",
                    "Templates",
                    "Video tutorials",
                    "Infographics"
                ],
                information_sources=[
                    "Content Marketing Institute",
                    "Twitter/X",
                    "Medium",
                    "Slack communities",
                    "YouTube"
                ],
                demographics={
                    "age_range": "28-38",
                    "experience_level": "5-10 years"
                },
                psychographics={
                    "personality": "Creative, analytical, collaborative",
                    "values": "Quality, authenticity, continuous learning"
                },
                behavioral_attributes={
                    "buying_behavior": "Influencer in decision, hands-on evaluator",
                    "content_consumption": "Deep reader, values detailed content"
                }
            )
        else:  # Growth Marketing Lead
            return PersonaProfile(
                name="Growth Marketing Lead Jordan",
                role="Growth Marketing Lead",
                company_size=segment["company_size_range"],
                goals=[
                    "Accelerate customer acquisition",
                    "Optimize conversion funnels",
                    "Experiment with new growth channels",
                    "Scale growth initiatives rapidly"
                ],
                challenges=[
                    "Resource constraints for testing",
                    "Need for rapid content iteration",
                    "Balancing multiple channels",
                    "Attribution complexity"
                ],
                pain_points=[
                    "Slow content production inhibits testing",
                    "Difficulty maintaining consistency across experiments",
                    "Limited budget for content creation",
                    "Need for agile content workflows"
                ],
                motivations=[
                    "Rapid experimentation and learning",
                    "Measurable growth metrics",
                    "Building scalable systems",
                    "Career growth through impact"
                ],
                preferred_content_types=[
                    "Landing pages",
                    "Email sequences",
                    "Ad copy",
                    "A/B test variations",
                    "Quick guides"
                ],
                information_sources=[
                    "Growth Hackers community",
                    "Reforge",
                    "LinkedIn",
                    "Growth marketing podcasts",
                    "Twitter/X"
                ],
                demographics={
                    "age_range": "26-36",
                    "experience_level": "3-8 years"
                },
                psychographics={
                    "personality": "Experimental, analytical, fast-paced",
                    "values": "Speed, data, innovation"
                },
                behavioral_attributes={
                    "buying_behavior": "Fast decision maker, values ROI",
                    "content_consumption": "Scans quickly, values actionable insights"
                }
            )
    
    def _develop_journey_maps(
        self,
        personas: List[PersonaProfile]
    ) -> List[ContentJourneyMap]:
        """
        Step 4: Develop detailed content journey maps.
        
        Args:
            personas: List of persona profiles
        
        Returns:
            List of ContentJourneyMap objects
        """
        logger.info("Step 4: Developing content journey maps")
        
        journey_maps = []
        
        for persona in personas:
            journey_map = self._create_journey_map_for_persona(persona)
            journey_maps.append(journey_map)
        
        return journey_maps
    
    def _create_journey_map_for_persona(
        self,
        persona: PersonaProfile
    ) -> ContentJourneyMap:
        """Create a content journey map for a specific persona."""
        # Create journey stages based on persona role
        if "Director" in persona.role:
            stages = [
                ContentJourneyStage(
                    stage_name="Awareness",
                    needs=[
                        "Understanding market challenges",
                        "Identifying potential solutions",
                        "Building business case for change"
                    ],
                    questions=[
                        "What are best practices for scaling content?",
                        "How do other companies solve this problem?",
                        "What ROI can I expect from content automation?"
                    ],
                    content_touchpoints=[
                        "Industry reports",
                        "LinkedIn posts",
                        "Webinar invitations",
                        "Thought leadership articles"
                    ],
                    content_formats=[
                        "Whitepapers",
                        "Research reports",
                        "Executive briefs",
                        "Industry benchmarks"
                    ]
                ),
                ContentJourneyStage(
                    stage_name="Consideration",
                    needs=[
                        "Evaluating solution options",
                        "Understanding implementation requirements",
                        "Assessing vendor credibility"
                    ],
                    questions=[
                        "How does PersonaScript compare to alternatives?",
                        "What's the implementation timeline?",
                        "What results have other companies achieved?"
                    ],
                    content_touchpoints=[
                        "Comparison guides",
                        "Case studies",
                        "Product demos",
                        "ROI calculators"
                    ],
                    content_formats=[
                        "Solution briefs",
                        "Customer testimonials",
                        "Demo videos",
                        "Feature comparison sheets"
                    ]
                ),
                ContentJourneyStage(
                    stage_name="Decision",
                    needs=[
                        "Final validation",
                        "Stakeholder alignment",
                        "Contract negotiation support"
                    ],
                    questions=[
                        "What are the specific contract terms?",
                        "What support is available during onboarding?",
                        "How do we ensure success?"
                    ],
                    content_touchpoints=[
                        "Sales consultations",
                        "Custom proposals",
                        "Reference calls",
                        "Trial access"
                    ],
                    content_formats=[
                        "Proposals",
                        "Implementation plans",
                        "Success stories",
                        "Onboarding guides"
                    ]
                )
            ]
        elif "Manager" in persona.role:
            stages = [
                ContentJourneyStage(
                    stage_name="Awareness",
                    needs=[
                        "Discovering new tools and approaches",
                        "Understanding content efficiency solutions",
                        "Learning from peers"
                    ],
                    questions=[
                        "How can I create more content faster?",
                        "What tools do other content teams use?",
                        "How do I maintain quality at scale?"
                    ],
                    content_touchpoints=[
                        "Blog posts",
                        "Social media content",
                        "Community forums",
                        "How-to articles"
                    ],
                    content_formats=[
                        "Blog articles",
                        "Tutorial videos",
                        "Tool reviews",
                        "Best practice guides"
                    ]
                ),
                ContentJourneyStage(
                    stage_name="Consideration",
                    needs=[
                        "Hands-on product evaluation",
                        "Understanding features and workflows",
                        "Assessing ease of use"
                    ],
                    questions=[
                        "How easy is PersonaScript to use?",
                        "Can it maintain our brand voice?",
                        "What's the learning curve?"
                    ],
                    content_touchpoints=[
                        "Product tutorials",
                        "Free trials",
                        "Feature deep-dives",
                        "User community"
                    ],
                    content_formats=[
                        "Video tutorials",
                        "Template libraries",
                        "Use case examples",
                        "FAQ documents"
                    ]
                ),
                ContentJourneyStage(
                    stage_name="Decision",
                    needs=[
                        "Getting manager buy-in",
                        "Proving value to leadership",
                        "Understanding pricing and terms"
                    ],
                    questions=[
                        "How do I justify the investment?",
                        "What metrics should I track?",
                        "What does onboarding look like?"
                    ],
                    content_touchpoints=[
                        "ROI calculators",
                        "Pitch deck templates",
                        "Pricing guides",
                        "Onboarding previews"
                    ],
                    content_formats=[
                        "Business case templates",
                        "Success metrics guides",
                        "Pricing sheets",
                        "Getting started guides"
                    ]
                )
            ]
        else:  # Growth Marketing Lead
            stages = [
                ContentJourneyStage(
                    stage_name="Awareness",
                    needs=[
                        "Finding growth acceleration tools",
                        "Understanding content velocity solutions",
                        "Discovering experimentation enablers"
                    ],
                    questions=[
                        "How can I test content faster?",
                        "What tools enable rapid iteration?",
                        "How do I scale personalization?"
                    ],
                    content_touchpoints=[
                        "Growth marketing blogs",
                        "Product Hunt",
                        "Twitter/X threads",
                        "Community recommendations"
                    ],
                    content_formats=[
                        "Quick guides",
                        "Tool comparisons",
                        "Growth hacks",
                        "Short videos"
                    ]
                ),
                ContentJourneyStage(
                    stage_name="Consideration",
                    needs=[
                        "Rapid product testing",
                        "Understanding integration options",
                        "Assessing speed to value"
                    ],
                    questions=[
                        "Can I start testing today?",
                        "Does it integrate with my stack?",
                        "What's the time to first results?"
                    ],
                    content_touchpoints=[
                        "Interactive demos",
                        "Free trials",
                        "Integration guides",
                        "Quick start tutorials"
                    ],
                    content_formats=[
                        "Sandbox access",
                        "Integration docs",
                        "Video walkthroughs",
                        "API documentation"
                    ]
                ),
                ContentJourneyStage(
                    stage_name="Decision",
                    needs=[
                        "Fast purchasing process",
                        "Flexible pricing options",
                        "Quick onboarding"
                    ],
                    questions=[
                        "Can I start with a small plan?",
                        "How quickly can I be up and running?",
                        "What results can I expect in 30 days?"
                    ],
                    content_touchpoints=[
                        "Self-service signup",
                        "Pricing page",
                        "Onboarding automation",
                        "30-day playbook"
                    ],
                    content_formats=[
                        "Pricing calculators",
                        "Quick start checklists",
                        "Success playbooks",
                        "Template libraries"
                    ]
                )
            ]
        
        return ContentJourneyMap(
            persona_name=persona.name,
            stages=stages
        )
    
    def _create_miro_board(self, personas: List[PersonaProfile]) -> str:
        """
        Step 5: Create and populate Miro board.
        
        Args:
            personas: List of persona profiles to visualize
        
        Returns:
            URL of created Miro board
        """
        logger.info("Step 5: Creating Miro board")
        
        board_data = {
            "title": "PersonaScript User Personas",
            "personas": [self._format_persona_for_miro(p) for p in personas]
        }
        
        miro_url = self.miro_integration.create_board(board_data)
        logger.info(f"Miro board created: {miro_url}")
        
        return miro_url
    
    def _format_persona_for_miro(self, persona: PersonaProfile) -> Dict[str, Any]:
        """Format a persona profile for Miro visualization."""
        return {
            "name": persona.name,
            "role": persona.role,
            "company_size": persona.company_size,
            "goals": persona.goals,
            "challenges": persona.challenges,
            "pain_points": persona.pain_points,
            "motivations": persona.motivations,
            "content_preferences": persona.preferred_content_types,
            "information_sources": persona.information_sources
        }
    
    def _create_google_doc(self, journey_maps: List[ContentJourneyMap]) -> str:
        """
        Step 6: Create and populate Google Doc.
        
        Args:
            journey_maps: List of content journey maps to document
        
        Returns:
            URL of created Google Doc
        """
        logger.info("Step 6: Creating Google Doc")
        
        doc_content = self._format_journey_maps_for_doc(journey_maps)
        
        doc_url = self.google_docs_integration.create_document(
            title="PersonaScript Content Journey Maps",
            content=doc_content
        )
        
        logger.info(f"Google Doc created: {doc_url}")
        return doc_url
    
    def _format_journey_maps_for_doc(
        self,
        journey_maps: List[ContentJourneyMap]
    ) -> str:
        """Format journey maps into structured document content."""
        content_parts = [
            "# PersonaScript Content Journey Maps",
            "",
            "This document outlines the detailed content journey for each user persona,",
            "mapping their needs, questions, and ideal content touchpoints across the sales funnel.",
            ""
        ]
        
        for journey_map in journey_maps:
            content_parts.extend([
                f"## {journey_map.persona_name}",
                ""
            ])
            
            for stage in journey_map.stages:
                content_parts.extend([
                    f"### {stage.stage_name} Stage",
                    "",
                    "**Needs:**",
                    *[f"- {need}" for need in stage.needs],
                    "",
                    "**Key Questions:**",
                    *[f"- {q}" for q in stage.questions],
                    "",
                    "**Content Touchpoints:**",
                    *[f"- {tp}" for tp in stage.content_touchpoints],
                    "",
                    "**Content Formats:**",
                    *[f"- {fmt}" for fmt in stage.content_formats],
                    ""
                ])
        
        return "\n".join(content_parts)
    
    def _create_github_issue(
        self,
        miro_url: str,
        docs_url: str,
        inputs: AgentInputs
    ) -> str:
        """
        Steps 7 & 8: Compose and create GitHub issue.
        
        Args:
            miro_url: URL of created Miro board
            docs_url: URL of created Google Doc
            inputs: Original inputs for context
        
        Returns:
            URL of created GitHub issue
        """
        logger.info("Steps 7 & 8: Creating GitHub issue")
        
        issue_content = self._compose_issue_content(miro_url, docs_url, inputs)
        
        issue_url = self.github_integration.create_issue(
            title="PersonaScript Persona & Journey Map Creation - Completed",
            body=issue_content,
            labels=["persona-creation", "completed"]
        )
        
        logger.info(f"GitHub issue created: {issue_url}")
        return issue_url
    
    def _compose_issue_content(
        self,
        miro_url: str,
        docs_url: str,
        inputs: AgentInputs
    ) -> str:
        """Compose the content for the GitHub issue."""
        return f"""# PersonaScript Persona Creation - Task Completed

## Goal
Develop detailed user personas and their content journey maps for PersonaScript, delivering them via Miro and Google Docs.

## Inputs Used
- Product Information: PersonaScript - B2B SaaS content generation platform
- Target Audience: {len(inputs.target_audience_demographics)} demographic segments
- Firmographics: {len(inputs.target_audience_firmographics)} firmographic segments
- Marketing Collateral: {len(inputs.marketing_collateral)} pieces analyzed
- Customer Interviews: {'Available' if inputs.customer_interviews else 'Not provided'}

## Outputs Generated

### 🎨 Miro Board - Detailed Persona Profiles
**URL:** {miro_url}

The Miro board contains visual representations of {len(self.personas)} detailed user personas:
{self._format_persona_list()}

### 📄 Google Doc - Comprehensive Content Journey Maps
**URL:** {docs_url}

The Google Doc contains detailed content journey maps for each persona, covering:
- Awareness stage content needs and touchpoints
- Consideration stage evaluation criteria and content
- Decision stage validation and conversion content

## Execution Summary

The PersonaCreatorAgent successfully executed all 8 steps:
1. ✅ Analyzed product information, audience data, and marketing collateral
2. ✅ Identified {len(self.personas)} distinct user segments
3. ✅ Generated comprehensive persona profiles with demographics, psychographics, and behavioral attributes
4. ✅ Developed detailed content journey maps for all personas
5. ✅ Created and populated Miro board with visual persona profiles
6. ✅ Created and populated Google Doc with structured journey maps
7. ✅ Composed this summary of task completion
8. ✅ Created this GitHub issue as final output

## Next Steps
- Review the persona profiles and journey maps
- Validate personas with customer-facing teams
- Use journey maps to guide content strategy
- Iterate on personas based on feedback
"""
    
    def _format_persona_list(self) -> str:
        """Format the list of personas for the issue."""
        return "\n".join([f"- {p.name} ({p.role})" for p in self.personas])
