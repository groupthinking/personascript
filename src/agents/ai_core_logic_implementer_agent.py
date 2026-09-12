"""
AICoreLogicImplementerAgent - Main agent for designing and implementing PersonaScript's AI Core Logic.

This agent designs the AI core logic for:
1. Contextual content generation
2. Brand guideline enforcement
3. Personalization
and compiles this design into a RAG/NLP pipeline blueprint.
"""

import os
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from ..integrations.github_integration import GitHubIntegration

logger = logging.getLogger(__name__)


@dataclass
class AICoreLogicInputs:
    """Input data for the AICoreLogicImplementerAgent."""

    task_specifications: Dict[str, Any]
    brand_guidelines: str
    style_guides: str
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    pinecone_api_key: Optional[str] = None
    weaviate_api_key: Optional[str] = None


@dataclass
class AICoreLogicOutputs:
    """Output data from the AICoreLogicImplementerAgent."""

    blueprint_path: str
    github_issue_url: str
    architecture_design: Dict[str, Any]
    nlp_pipeline_design: Dict[str, Any]


class AICoreLogicImplementerAgent:
    """
    Main agent class for implementing the AI core logic blueprint.

    This agent follows a 7-step execution plan:
    1. Analyze provided task specifications to identify core requirements.
    2. Design the high-level architecture for the AI inference engine (RAG capabilities).
    3. Define components and workflow of the custom NLP pipeline.
    4. Outline LLM and vector database integration strategy.
    5. Specify required development environment setup.
    6. Compile a comprehensive technical design document (AI_CORE_LOGIC_BLUEPRINT.md).
    7. Create a detailed GitHub issue summarizing the implementation blueprint.
    """

    def __init__(
        self,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """
        Initialize the AICoreLogicImplementerAgent.

        Args:
            github_token: Token for GitHub API
            github_repo: Repository name (format: "owner/repo")
        """
        self.github_integration = GitHubIntegration(token=github_token, repo=github_repo)
        logger.info("AICoreLogicImplementerAgent initialized")

    def execute(self, inputs: AICoreLogicInputs) -> AICoreLogicOutputs:
        """
        Execute the complete design and documentation workflow.

        Args:
            inputs: Input specifications, guidelines, and API/DB keys.

        Returns:
            AICoreLogicOutputs containing paths, URLs, and design schemas.
        """
        logger.info("Starting AICoreLogicImplementerAgent execution")

        # Step 1: Analyze provided task specifications to identify core requirements
        requirements = self._analyze_specifications(inputs)

        # Step 2: Design the high-level architecture for the AI inference engine with RAG
        rag_design = self._design_rag_architecture(requirements)

        # Step 3: Define components and workflow of the custom NLP pipeline
        nlp_pipeline = self._define_nlp_pipeline(inputs)

        # Step 4: Outline integration strategy for LLMs and vector databases
        integration_strategy = self._outline_integration_strategy(inputs)

        # Step 5: Specify required development environment setup
        env_setup = self._specify_env_setup()

        # Step 6: Compile a comprehensive technical design document
        blueprint_path = "AI_CORE_LOGIC_BLUEPRINT.md"
        self._generate_blueprint_document(
            blueprint_path,
            inputs,
            requirements,
            rag_design,
            nlp_pipeline,
            integration_strategy,
            env_setup
        )

        # Step 7: Create a detailed GitHub issue summarizing the blueprint
        github_issue_url = self._create_github_issue(
            blueprint_path,
            inputs,
            requirements,
            rag_design,
            nlp_pipeline
        )

        outputs = AICoreLogicOutputs(
            blueprint_path=blueprint_path,
            github_issue_url=github_issue_url,
            architecture_design=rag_design,
            nlp_pipeline_design=nlp_pipeline
        )

        logger.info("AICoreLogicImplementerAgent execution completed successfully")
        return outputs

    def _analyze_specifications(self, inputs: AICoreLogicInputs) -> Dict[str, Any]:
        """Step 1: Analyze provided task specifications to identify core requirements."""
        logger.info("Step 1: Analyzing task specifications and core requirements")
        specs = inputs.task_specifications

        requirements = {
            "content_generation": specs.get("content_generation", {
                "formats": ["Email sequences", "Blog posts", "Landing page copy", "Social media posts"],
                "funnel_stages": ["Awareness", "Consideration", "Decision"],
                "scalability": "High volume capability with fast turnaround"
            }),
            "brand_guideline_enforcement": {
                "source_guidelines_summary": inputs.brand_guidelines[:300] + "..." if len(inputs.brand_guidelines) > 300 else inputs.brand_guidelines,
                "tone_requirements": specs.get("tone_requirements", ["B2B professional", "Authoritative yet friendly", "Action-oriented"]),
                "forbidden_elements": specs.get("forbidden_elements", ["Overly hype terms", "Competitor names", "Over-promising claims"])
            },
            "personalization": {
                "dimensions": ["Persona (e.g., Demand Gen, Content Mgr)", "Company Size", "Industry Vertical", "Funnel Stage"],
                "data_inputs": ["Persona Profiles", "Content Journey Maps", "Custom User Metadata"]
            }
        }
        return requirements

    def _design_rag_architecture(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Step 2: Design the high-level architecture for the AI inference engine with RAG."""
        logger.info("Step 2: Designing RAG-enabled inference engine")
        return {
            "ingestion_pipeline": {
                "document_parsers": ["PDF", "Markdown", "JSON", "Plain Text"],
                "chunking_strategy": "Recursive character splitting (chunk size: 1000, overlap: 200)",
                "metadata_enrichment": ["Document type", "Persona alignment", "Funnel stage", "Last updated"]
            },
            "embedding_layer": {
                "model": "text-embedding-3-small (OpenAI)",
                "dimension": 1536,
                "metric": "Cosine similarity"
            },
            "retrieval_strategy": {
                "hybrid_search": "BM25 keyword search combined with vector search",
                "reranking_model": "cohere-rerank-v3 or similar (optional)",
                "top_k": 5,
                "filters": "Dynamic metadata filtering based on target persona and funnel stage"
            },
            "inference_engine": {
                "orchestration_framework": "LangChain or LlamaIndex",
                "generation_llm": "gpt-4o (OpenAI) or claude-3-5-sonnet (Anthropic)",
                "prompt_templating": {
                    "system_prompt": "Enforce role, retrieved brand guidelines, and target persona traits.",
                    "user_prompt": "Generate personalized content using the retrieved context."
                }
            }
        }

    def _define_nlp_pipeline(self, inputs: AICoreLogicInputs) -> Dict[str, Any]:
        """Step 3: Define components and workflow of the custom NLP pipeline."""
        logger.info("Step 3: Defining custom NLP pipeline components and workflow")
        return {
            "pre_processing": [
                "Input sanitization and safety filtering",
                "Context extraction and parameter mapping"
            ],
            "analysis_and_scoring": {
                "tone_analyzer": {
                    "method": "Few-shot semantic similarity comparison / classifier",
                    "target_metrics": ["Formality", "Humor", "Professionalism", "Friendliness"]
                },
                "style_checker": {
                    "method": "Regex-based rule matching combined with LLM critique",
                    "checks": ["Sentence length", "Active voice", "Grammar & readability index"]
                },
                "brand_adherence_guardrails": {
                    "method": "Exact keyword list matching & semantic distance checks",
                    "checks": ["Forbidden words list", "Competitor mention detection", "Cliché detection"]
                }
            },
            "post_processing_feedback_loop": {
                "action": "Conditional iteration / self-correction",
                "max_retries": 3,
                "refinement_trigger": "Failures in style checker or brand adherence score < 85%"
            }
        }

    def _outline_integration_strategy(self, inputs: AICoreLogicInputs) -> Dict[str, Any]:
        """Step 4: Outline integration strategy for LLMs and vector databases."""
        logger.info("Step 4: Outlining API/SDK integration strategy")
        return {
            "llm_providers": {
                "openai": {
                    "sdk": "openai-python",
                    "key_configured": inputs.openai_api_key is not None,
                    "model": "gpt-4o"
                },
                "anthropic": {
                    "sdk": "anthropic-python",
                    "key_configured": inputs.anthropic_api_key is not None,
                    "model": "claude-3-5-sonnet"
                }
            },
            "vector_databases": {
                "pinecone": {
                    "sdk": "pinecone-client",
                    "key_configured": inputs.pinecone_api_key is not None,
                    "index_schema": {
                        "dimension": 1536,
                        "metric": "cosine",
                        "metadata_config": ["id", "text", "source", "persona", "funnel_stage"]
                    }
                },
                "weaviate": {
                    "sdk": "weaviate-client",
                    "key_configured": inputs.weaviate_api_key is not None,
                    "class_schema": {
                        "class": "BrandGuidelineChunk",
                        "properties": [
                            {"name": "text", "dataType": ["text"]},
                            {"name": "source", "dataType": ["text"]},
                            {"name": "persona", "dataType": ["text"]},
                            {"name": "funnel_stage", "dataType": ["text"]}
                        ]
                    }
                }
            }
        }

    def _specify_env_setup(self) -> Dict[str, Any]:
        """Step 5: Specify required development environment setup."""
        logger.info("Step 5: Specifying required development environment setup")
        return {
            "python_version": "Python 3.11+",
            "core_frameworks": [
                "PyTorch >= 2.0.0 (for custom NLP local model operations, if any)",
                "transformers >= 4.30.0 (Hugging Face for local encoders/classifiers)"
            ],
            "key_packages": [
                "openai >= 1.0.0",
                "anthropic >= 0.15.0",
                "pinecone-client >= 3.0.0",
                "weaviate-client >= 4.0.0",
                "pydantic >= 2.0.0",
                "spacy >= 3.5.0",
                "nltk >= 3.8.0",
                "langchain >= 0.1.0"
            ]
        }

    def _generate_blueprint_document(
        self,
        filepath: str,
        inputs: AICoreLogicInputs,
        requirements: Dict[str, Any],
        rag_design: Dict[str, Any],
        nlp_pipeline: Dict[str, Any],
        integration_strategy: Dict[str, Any],
        env_setup: Dict[str, Any]
    ) -> None:
        """Step 6: Compile a comprehensive technical design document."""
        logger.info(f"Step 6: Generating blueprint document at {filepath}")

        # Build document content
        content = f"""# PersonaScript: AI Core Logic Technical Blueprint

This document details the complete technical design blueprint for PersonaScript's core AI logic, incorporating a Retrieval-Augmented Generation (RAG) architecture and a custom NLP pipeline.

---

## 1. Executive Summary & Goals

The goal of the **AICoreLogic** subsystem is to deliver a robust AI inference engine that:
1. Generates hyper-personalized marketing content tailored to specific personas and buyer journey funnel stages.
2. Strictly enforces brand guidelines and style limits to maintain consistent brand voice and messaging.
3. Incorporates a Retrieval-Augmented Generation (RAG) framework utilizing industry-standard LLMs and vector databases.
4. Leverages a multi-stage custom NLP pipeline to validate generated content before final delivery.

---

## 2. Core Requirements Analysis

Based on the provided task specifications and inputs, the subsystem supports:

### 2.1 Contextual Content Generation
- **Formats Supported**: {", ".join(requirements["content_generation"]["formats"])}
- **Funnel Stages**: {", ".join(requirements["content_generation"]["funnel_stages"])}
- **Scalability Target**: {requirements["content_generation"]["scalability"]}

### 2.2 Brand Guideline Enforcement
- **Guidelines Source**:
  ```text
  {requirements["brand_guideline_enforcement"]["source_guidelines_summary"]}
  ```
- **Target Tone Characteristics**: {", ".join(requirements["brand_guideline_enforcement"]["tone_requirements"])}
- **Prohibited / Forbidden Elements**: {", ".join(requirements["brand_guideline_enforcement"]["forbidden_elements"])}

### 2.3 Personalization Dimensions
- **Core Dimensions**: {", ".join(requirements["personalization"]["dimensions"])}
- **Data Inputs Utilized**: {", ".join(requirements["personalization"]["data_inputs"])}

---

## 3. High-Level RAG Architecture Design

The inference engine utilizes RAG to fetch contextual brand guidelines and product details dynamically, preventing hallucination and ensuring accurate terminology.

```
       [ Document Ingestion: Brand Guidelines / Style Guides ]
                                 │
                     [ Chunking & Metadata tagging ]
                                 │
                     [ Embedding (1536-dim OpenAI) ]
                                 │
                                 ▼
                     [ Vector Database: Pinecone/Weaviate ]
                                 │
[ User Prompt / Target Persona ] ┼ ───► [ Hybrid Vector + Keyword Retrieval ]
                                 │
                                 ▼
                      [ In-Context LLM Prompt ]
                                 │
                                 ▼
                [ LLM Generation: GPT-4o/Claude-3.5 ]
                                 │
                                 ▼
                    [ Custom NLP Pipeline Audit ]
```

### 3.1 Document Ingestion & Chunking
- **Chunking Method**: {rag_design["ingestion_pipeline"]["chunking_strategy"]}
- **Metadata Enriched**: {", ".join(rag_design["ingestion_pipeline"]["metadata_enrichment"])}

### 3.2 Embedding & Retrieval Strategy
- **Embedding Model**: {rag_design["embedding_layer"]["model"]} ({rag_design["embedding_layer"]["dimension"]} dimensions, metric: {rag_design["embedding_layer"]["metric"]})
- **Retrieval Strategy**: {rag_design["retrieval_strategy"]["hybrid_search"]}
- **Metadata Filtering**: {rag_design["retrieval_strategy"]["filters"]}
- **Top K**: {rag_design["retrieval_strategy"]["top_k"]}

### 3.3 Inference Engine & Prompting
- **Orchestrator**: {rag_design["inference_engine"]["orchestration_framework"]}
- **LLM Selection**: {rag_design["inference_engine"]["generation_llm"]}
- **System Prompt Design**:
  - *"{rag_design["inference_engine"]["prompt_templating"]["system_prompt"]}"*
- **User Prompt Design**:
  - *"{rag_design["inference_engine"]["prompt_templating"]["user_prompt"]}"*

---

## 4. Custom NLP Pipeline Architecture

Generated content undergoes multi-layered post-generation evaluations to audit brand compliance, tone correctness, and style metrics before being returned to the user.

### 4.1 Pipeline Components
1. **Tone Analyzer**:
   - **Method**: {nlp_pipeline["analysis_and_scoring"]["tone_analyzer"]["method"]}
   - **Metrics Checked**: {", ".join(nlp_pipeline["analysis_and_scoring"]["tone_analyzer"]["target_metrics"])}
2. **Style Checker**:
   - **Method**: {nlp_pipeline["analysis_and_scoring"]["style_checker"]["method"]}
   - **Rule Audits**: {", ".join(nlp_pipeline["analysis_and_scoring"]["style_checker"]["checks"])}
3. **Brand Adherence Guardrails**:
   - **Method**: {nlp_pipeline["analysis_and_scoring"]["brand_adherence_guardrails"]["method"]}
   - **Guards Activated**: {", ".join(nlp_pipeline["analysis_and_scoring"]["brand_adherence_guardrails"]["checks"])}

### 4.2 Post-Processing & Feedback Loop
- **Action**: {nlp_pipeline["post_processing_feedback_loop"]["action"]}
- **Max Retries**: {nlp_pipeline["post_processing_feedback_loop"]["max_retries"]}
- **Refinement Trigger**: {nlp_pipeline["post_processing_feedback_loop"]["refinement_trigger"]}

---

## 5. SDK & API Integration Strategy

### 5.1 LLM SDK configurations
- **OpenAI Integration**: SDK `openai-python` configured to use model `{integration_strategy["llm_providers"]["openai"]["model"]}`.
- **Anthropic Integration**: SDK `anthropic-python` configured to use model `{integration_strategy["llm_providers"]["anthropic"]["model"]}`.

### 5.2 Vector Databases configurations
- **Pinecone Config**:
  - Index schema uses dimension `{integration_strategy["vector_databases"]["pinecone"]["index_schema"]["dimension"]}`, metric `{integration_strategy["vector_databases"]["pinecone"]["index_schema"]["metric"]}`.
  - Tracked metadata fields: `{", ".join(integration_strategy["vector_databases"]["pinecone"]["index_schema"]["metadata_config"])}`.
- **Weaviate Config**:
  - Target Class Schema: `{integration_strategy["vector_databases"]["weaviate"]["class_schema"]["class"]}`
  - Properties: `[text, source, persona, funnel_stage]`

---

## 6. Development Environment Setup

### 6.1 Requirements
- **Runtime**: {env_setup["python_version"]}
- **Core AI/ML Frameworks**: {", ".join(env_setup["core_frameworks"])}
- **Required Packages**:
{chr(10).join([f"  - {pkg}" for pkg in env_setup["key_packages"] or []])}

### 6.2 Installation Command
```bash
pip install {" ".join([p.split(" ")[0] for p in env_setup["key_packages"]])}
```

---

## 7. Step-by-Step Implementation Execution Plan

1. **Phase 1: Environment & SDK Setup**
   - Configure Python 3.11/3.12 workspace, install PyTorch and SDK dependencies.
   - Set up `.env` with OpenAI, Anthropic, Pinecone, and Weaviate API keys.
2. **Phase 2: RAG Ingestion & Vector DB Setup**
   - Write standard chunking script with overlap and enrich chunk metadata with persona & stage parameters.
   - Initialize index in Pinecone or schema collection in Weaviate.
   - Implement document upload/upsert pipeline.
3. **Phase 3: LLM Inference Engine & Context Retrieval**
   - Create the contextual search client mapping query metadata to filters.
   - Build orchestrator prompts merging retrieved chunks with target persona profiles.
4. **Phase 4: Custom NLP Pipeline Enforcement**
   - Implement the tone analyzer, grammar and readability checks.
   - Implement prohibited keyword matcher.
   - Code the automated feedback retry loops allowing the LLM to refine failed content.
5. **Phase 5: Evaluation & Automated Tests**
   - Write tests simulating content generation and ensuring generated copies abide by guideline scoring parameters.
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"Blueprint design document successfully written to {filepath}")

    def _create_github_issue(
        self,
        blueprint_path: str,
        inputs: AICoreLogicInputs,
        requirements: Dict[str, Any],
        rag_design: Dict[str, Any],
        nlp_pipeline: Dict[str, Any]
    ) -> str:
        """Step 7: Create a detailed GitHub issue summarizing the agent's goal, inputs, expected outputs, and execution plan."""
        logger.info("Step 7: Composing and creating GitHub issue summarizing the blueprint")

        title = "AI Core Logic Implementation Blueprint - Completed"

        body = f"""# AI Core Logic Implementation Blueprint

## Goal
Implement the core AI logic for contextual content generation, brand guideline enforcement, and personalization, delivering a robust AI inference engine with RAG capabilities and a custom NLP pipeline.

## Inputs Used
- Task specifications (Personalization, Brand Tone, Content Formats)
- Brand Guidelines: Provided ({len(inputs.brand_guidelines)} chars)
- Style Guides: Provided ({len(inputs.style_guides)} chars)
- OpenAI/Anthropic APIs: Configured / Standardized
- Pinecone/Weaviate vector databases: Configured / Standardized

## Generated Outputs
- **Technical Design Document**: `{blueprint_path}` (Created successfully)

---

## Technical Blueprint Highlights

### 1. High-Level RAG Architecture
- **Embedding Model**: {rag_design["embedding_layer"]["model"]}
- **Retrieval Engine**: Hybrid search combining Vector and Keyword querying with metadata filters (persona, funnel stage).
- **Generation LLM**: {rag_design["inference_engine"]["generation_llm"]}

### 2. Custom NLP Pipeline
- **Tone Analyzer**: Few-shot classifier mapping generated content to {", ".join(requirements["brand_guideline_enforcement"]["tone_requirements"])}.
- **Style Checker**: Readability indexing, active voice check, and length rules.
- **Brand Guardrails**: Exact prohibited word/phrases list verification.
- **Automated Retry Loop**: Max of {nlp_pipeline["post_processing_feedback_loop"]["max_retries"]} self-correction attempts if compliance score is under 85%.

### 3. SDK & API Integration
- Uses `openai-python`, `anthropic-python`, `pinecone-client`, and `weaviate-client`.
- Fully standard schemas mapping context documents to metadata layers.

---

## Implementation Execution Plan

1. **Phase 1: Environment & Workspace Setup**
   - Setup Python workspace with PyTorch & core AI SDKs (`openai`, `anthropic`, `pinecone-client`, `weaviate-client`).
2. **Phase 2: RAG Ingestion Pipeline**
   - Build recursive chunking logic and populate Pinecone/Weaviate with metadata-enriched guideline documents.
3. **Phase 3: Core Retrieval & Inference Orchestrator**
   - Build retrieval logic with context-matched filtering. Generate prompt maps.
4. **Phase 4: Custom NLP Audit & Feedback Loop**
   - Code validation layers (Tone, Style, Brand Guardrails) and self-correction retry cycles.
5. **Phase 5: Comprehensive testing & metrics**
   - Write pytest test suite asserting output compliance metrics.

*Review the comprehensive blueprint in the file `{blueprint_path}`.*
"""
        issue_content = {
            "title": title,
            "body": body
        }

        issue_url = self.github_integration.create_issue(
            title=title,
            body=body,
            labels=["ai-core-logic", "rag", "nlp-pipeline", "blueprint"]
        )
        return issue_url
