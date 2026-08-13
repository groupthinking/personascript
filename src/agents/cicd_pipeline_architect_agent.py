"""
PersonaScriptCICDPipelineArchitectAgent - Main agent for designing and documenting CI/CD pipelines.

This agent analyzes business context and automation requirements to:
1. Parse the input task and identify scope.
2. Research best practices for frontend, backend, and AI service pipelines.
3. Formulate high-level architectures for each pipeline.
4. Draft detailed GitHub Actions workflow YAML configurations/pseudocode.
5. Consolidate architecture and YAMLs into a comprehensive blueprint.
6. Construct GitHub issue content and create the issue.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from ..integrations.github_integration import GitHubIntegration

logger = logging.getLogger(__name__)


@dataclass
class CICDInputs:
    """Input data for the CICDPipelineArchitectAgent."""

    business_context: str
    task_to_automate: str
    target_platform: str = "GitHub Actions"
    github_token: Optional[str] = None
    github_repo: Optional[str] = None


@dataclass
class CICDOutputs:
    """Output data from the CICDPipelineArchitectAgent."""

    high_level_architecture: str
    frontend_yaml: str
    backend_yaml: str
    ai_service_yaml: str
    consolidated_blueprint: str
    github_issue_url: str


class CICDPipelineArchitectAgent:
    """
    Agent for designing, documenting, and implementing CI/CD pipeline blueprints
    for frontend, backend, and AI/ML services using GitHub Actions.
    """

    def __init__(
        self,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """
        Initialize the CICDPipelineArchitectAgent.

        Args:
            github_token: Token for GitHub API
            github_repo: Repository name (format: "owner/repo")
        """
        self.github_integration = GitHubIntegration(token=github_token, repo=github_repo)
        logger.info("CICDPipelineArchitectAgent initialized")

    def execute(self, inputs: CICDInputs) -> CICDOutputs:
        """
        Execute the complete agent workflow.

        Args:
            inputs: Input data containing business context and target requirements.

        Returns:
            CICDOutputs containing high-level architecture, YAMLs, consolidated blueprint, and issue URL.
        """
        logger.info("Starting CICDPipelineArchitectAgent execution")

        # Step 1: Parse input task and identify scope
        scope = self._parse_scope(inputs)

        # Step 2: Formulate high-level architecture
        architecture = self._formulate_architecture(inputs, scope)

        # Step 3: Draft detailed GitHub Actions YAML configurations
        frontend_yaml = self._draft_frontend_yaml()
        backend_yaml = self._draft_backend_yaml()
        ai_service_yaml = self._draft_ai_service_yaml()

        # Step 4: Consolidate architecture and YAMLs into a blueprint
        blueprint = self._consolidate_blueprint(
            inputs, architecture, frontend_yaml, backend_yaml, ai_service_yaml
        )

        # Step 5: Construct GitHub issue content and create issue
        github_issue_url = self._create_github_issue(inputs, blueprint)

        outputs = CICDOutputs(
            high_level_architecture=architecture,
            frontend_yaml=frontend_yaml,
            backend_yaml=backend_yaml,
            ai_service_yaml=ai_service_yaml,
            consolidated_blueprint=blueprint,
            github_issue_url=github_issue_url
        )

        logger.info("CICDPipelineArchitectAgent execution completed successfully")
        return outputs

    def _parse_scope(self, inputs: CICDInputs) -> Dict[str, Any]:
        """Step 1: Parse input task and identify scope."""
        logger.info("Step 1: Parsing input task and identifying scope")
        return {
            "services": ["frontend", "backend", "ai_services"],
            "stages": ["automated_testing", "building", "deployment"],
            "target_platform": inputs.target_platform,
            "business_alignment": "PersonaScript high-volume content generation & personalization"
        }

    def _formulate_architecture(self, inputs: CICDInputs, scope: Dict[str, Any]) -> str:
        """Step 2: Formulate high-level architecture for frontend, backend, and AI pipelines."""
        logger.info("Step 2: Formulating high-level architecture")

        architecture = f"""### High-Level CI/CD Architecture

We design a multi-service, fully automated CI/CD pipeline architecture tailored for **PersonaScript** utilizing **{inputs.target_platform}**.

This architecture guarantees that all code pushed to the repository is thoroughly tested, securely built, and seamlessly deployed. The pipelines are optimized for modularity, safety, and velocity.

```
                  ┌──────────────────────────────┐
                  │      Developer Push/PR       │
                  └──────────────┬───────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │ (frontend-path/)      │ (backend-path/)       │ (ai-path/)
         ▼                       ▼                       ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Frontend CI    │    │    Backend CI    │    │  AI Service CI   │
│  - ESLint/Pret   │    │  - Ruff/Black    │    │  - Linter/Types  │
│  - Jest/Vitest   │    │  - Pytest        │    │  - Model Test    │
│  - Build App     │    │  - Bandit        │    │  - Pytest        │
└────────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘
         │                       │                       │
         ▼ (on main)             ▼ (on main)             ▼ (on main/tag)
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Frontend CD    │    │    Backend CD    │    │  AI Service CD   │
│  - Deploy S3/    │    │  - Docker Build  │    │  - Log ML model  │
│    CloudFront    │    │  - Push GHCR/ECR │    │  - Build Docker  │
│  - Cache Inval   │    │  - Deploy ECS/K8s│    │  - Deploy SageMk │
└──────────────────┘    └──────────────────┘    └──────────────────┘
```

#### 1. Frontend CI/CD Pipeline (Node.js/React)
- **CI Stage (Verification)**: Runs on every Pull Request targeting `main`. Triggers linters (`eslint`, `prettier`), dependency audits (`npm audit`), and unit/integration tests (`jest` or `vitest`).
- **CD Stage (Deployment)**: Runs on merge/push to `main`. Automatically builds the static assets, uploads them to an object storage bucket (e.g., AWS S3 or Google Cloud Storage), and invalidates the CDN distribution (e.g., CloudFront).

#### 2. Backend CI/CD Pipeline (Python)
- **CI Stage (Verification)**: Runs on Pull Requests. Enforces code styling and checks using `ruff`, `black`, and `mypy` for static typing. Executes comprehensive suite of tests with `pytest` with code coverage reports. Analyzes security vulnerabilities using `bandit` and `safety`.
- **CD Stage (Deployment)**: Runs on merge to `main`. Builds a production-ready multi-stage Docker image, tags it with the Git SHA, pushes it to GitHub Container Registry (GHCR) or AWS Elastic Container Registry (ECR), and performs a rolling update deployment to AWS ECS or Kubernetes.

#### 3. AI/ML Service CI/CD Pipeline (Python + ML Ops)
- **CI Stage (Verification)**: Runs on changes to AI/ML directories. Linting/testing plus a specific **Model Validation** stage where offline model evaluation scripts are executed against benchmark datasets to verify that accuracy/F1 performance has not degraded below predefined thresholds.
- **CD Stage (Deployment)**: Triggers on manual approval, Git tag releases, or merge to `main`. Logs model artifacts using MLflow or DVC, packages the serving API (FastAPI) inside a GPU-supported Docker image, and deploys to a managed endpoints host (e.g., AWS SageMaker or GCP Vertex AI) with blue-green routing.
"""
        return architecture

    def _draft_frontend_yaml(self) -> str:
        """Step 3a: Draft detailed GitHub Actions YAML for Frontend."""
        logger.info("Step 3a: Drafting Frontend YAML")
        return """name: Frontend CI/CD

on:
  push:
    branches: [ main ]
    paths:
      - 'frontend/**'
      - '.github/workflows/frontend.yml'
  pull_request:
    branches: [ main ]
    paths:
      - 'frontend/**'
      - '.github/workflows/frontend.yml'

jobs:
  test:
    name: Lint & Test
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: frontend

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install Dependencies
        run: npm ci

      - name: Code Formatting Check
        run: npm run format:check

      - name: Linting
        run: npm run lint

      - name: Security Audit
        run: npm audit --audit-level=high

      - name: Run Unit Tests
        run: npm run test -- --coverage --watchAll=false

      - name: Upload Coverage
        uses: actions/upload-artifact@v4
        with:
          name: frontend-coverage
          path: frontend/coverage/

  build-and-deploy:
    name: Build & Deploy
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: frontend

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install Dependencies
        run: npm ci

      - name: Build Application
        run: npm run build
        env:
          REACT_APP_API_URL: ${{ secrets.PRODUCTION_API_URL }}

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to S3 Bucket
        run: aws s3 sync build/ s3://${{ secrets.S3_BUCKET_NAME }} --delete

      - name: Invalidate CloudFront Cache
        run: aws cloudfront create-invalidation --distribution-id ${{ secrets.CLOUDFRONT_DIST_ID }} --paths "/*"
"""

    def _draft_backend_yaml(self) -> str:
        """Step 3b: Draft detailed GitHub Actions YAML for Backend."""
        logger.info("Step 3b: Drafting Backend YAML")
        return """name: Backend CI/CD

on:
  push:
    branches: [ main ]
    paths:
      - 'backend/**'
      - '.github/workflows/backend.yml'
  pull_request:
    branches: [ main ]
    paths:
      - 'backend/**'
      - '.github/workflows/backend.yml'

jobs:
  quality-and-test:
    name: Lint, Type Check & Test
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install ruff mypy pytest pytest-cov bandit safety

      - name: Ruff Lint & Format Check
        run: ruff check .

      - name: Static Type Checking
        run: mypy .

      - name: Run Security Scan (Bandit)
        run: bandit -r . -x ./tests

      - name: Check Dependencies Security (Safety)
        run: safety check

      - name: Run Unit Tests with Coverage
        run: pytest --cov=app --cov-report=xml

      - name: Upload Coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          file: ./backend/coverage.xml

  build-and-push:
    name: Build & Push Docker Image
    needs: quality-and-test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GitHub Container Registry (GHCR)
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and Push Docker Image
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          file: ./backend/Dockerfile
          push: true
          tags: |
            ghcr.io/${{ github.repository }}/personascript-backend:latest
            ghcr.io/${{ github.repository }}/personascript-backend:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    name: Continuous Deployment
    needs: build-and-push
    runs-on: ubuntu-latest

    steps:
      - name: Deploy to Cloud Provider (e.g., GCP Cloud Run)
        uses: google-github-actions/deploy-cloudrun@v2
        with:
          service: personascript-backend
          image: ghcr.io/${{ github.repository }}/personascript-backend:${{ github.sha }}
          region: us-central1
          credentials: ${{ secrets.GCP_SA_KEY }}
"""

    def _draft_ai_service_yaml(self) -> str:
        """Step 3c: Draft detailed GitHub Actions YAML for AI Service."""
        logger.info("Step 3c: Drafting AI Service YAML")
        return """name: AI Service CI/CD

on:
  push:
    branches: [ main ]
    paths:
      - 'ai_services/**'
      - '.github/workflows/ai.yml'
  pull_request:
    branches: [ main ]
    paths:
      - 'ai_services/**'
      - '.github/workflows/ai.yml'
  workflow_dispatch:

jobs:
  lint-and-validate:
    name: Validate Code and Model Performance
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ai_services

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python (ML Environment)
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install ruff pytest

      - name: Code Quality (Ruff)
        run: ruff check .

      - name: Run Unit Tests (Inference APIs)
        run: pytest tests/unit

      - name: Model Validation (Accuracy & F1 score)
        run: python scripts/validate_model.py
        env:
          TEST_DATA_PATH: "./data/eval_set.csv"
          THRESHOLD_ACCURACY: "0.85"

  build-ai-container:
    name: Package AI Service with GPU Support
    needs: lint-and-validate
    if: github.ref == 'refs/heads/main' && (github.event_name == 'push' || github.event_name == 'workflow_dispatch')
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Log in to AWS ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build and Push GPU Docker Image
        uses: docker/build-push-action@v5
        with:
          context: ./ai_services
          file: ./ai_services/Dockerfile.gpu
          push: true
          tags: |
            ${{ steps.login-ecr.outputs.registry }}/personascript-ai-service:latest
            ${{ steps.login-ecr.outputs.registry }}/personascript-ai-service:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-to-sagemaker:
    name: Deploy to AWS SageMaker Endpoint
    needs: build-ai-container
    runs-on: ubuntu-latest

    steps:
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Update SageMaker Endpoint
        run: |
          python ai_services/scripts/deploy_endpoint.py \\
            --image-uri "${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.us-east-1.amazonaws.com/personascript-ai-service:${{ github.sha }}" \\
            --role-arn "${{ secrets.SAGEMAKER_ROLE_ARN }}" \\
            --endpoint-name "personascript-ai-generation-endpoint"
"""

    def _consolidate_blueprint(
        self,
        inputs: CICDInputs,
        architecture: str,
        frontend_yaml: str,
        backend_yaml: str,
        ai_service_yaml: str
    ) -> str:
        """Step 4: Consolidate high-level architecture and drafted YAML configs."""
        logger.info("Step 4: Consolidating blueprint")
        return f"""# PersonaScript CI/CD Blueprint Document

This comprehensive blueprint describes the continuous integration and continuous deployment (CI/CD) pipelines designed specifically for the **PersonaScript** platform.

## Business Context & Value Proposition Alignment
PersonaScript empowers B2B SaaS teams to rapidly generate brand-aligned, hyper-personalized, and high-volume content. To maintain the rapid velocity required by B2B teams, the engineering workflows must be backed by absolute stability, robust code quality verification, and low-friction continuous delivery. This blueprint ensures that:
- Every bug in the NLP models, backend API, or frontend UI is caught before hitting production.
- Security and vulnerability audits are executed on every commit.
- Deployment of validated code, components, and models is entirely hands-off.

---

{architecture}

---

### Detailed GitHub Actions Configurations

#### 1. Frontend Workflow (`.github/workflows/frontend.yml`)
```yaml
{frontend_yaml}
```

#### 2. Backend Workflow (`.github/workflows/backend.yml`)
```yaml
{backend_yaml}
```

#### 3. AI Service Workflow (`.github/workflows/ai.yml`)
```yaml
{ai_service_yaml}
```

---

### Security & Secrets Management
All credentials and configuration variables must be managed securely through GitHub Actions Secrets. The following secrets are required:
- `PRODUCTION_API_URL`: The production API endpoint.
- `AWS_ACCESS_KEY_ID` & `AWS_SECRET_ACCESS_KEY`: AWS credentials for frontend S3 sync and ECR/SageMaker deployment.
- `S3_BUCKET_NAME`: The S3 bucket holding frontend build artifacts.
- `CLOUDFRONT_DIST_ID`: CDN distribution ID for invalidation.
- `CODECOV_TOKEN`: Token for uploading backend test coverage reports.
- `GCP_SA_KEY`: Service Account key for Google Cloud Run deployment.
- `SAGEMAKER_ROLE_ARN`: AWS IAM execution role ARN for SageMaker.

---
*Created by PersonaScript CICDPipelineArchitectAgent.*
"""

    def _create_github_issue(
        self,
        inputs: CICDInputs,
        blueprint: str
    ) -> str:
        """Step 5: Compose and create GitHub issue."""
        logger.info("Step 5: Creating GitHub issue")

        title = "PersonaScript CI/CD Pipeline Blueprint - GitHub Actions Architecture"
        body = f"""# CI/CD Pipeline Blueprint - Architecture Design Complete

## Agent Goal
To design and document a comprehensive blueprint for CI/CD pipelines across the PersonaScript frontend application, backend services, and AI/ML services, and create a tracking issue.

## Inputs Received
- **Business Context**: {inputs.business_context}
- **Task to Automate**: {inputs.task_to_automate}
- **Target Platform**: {inputs.target_platform}

## Consolidate Pipeline Blueprint

{blueprint}

## Execution Plan & Progress Summary
The `CICDPipelineArchitectAgent` executed the following steps:
1. ✅ **Parse Scope**: Analyzed PersonaScript requirements for frontend, backend, and AI pipeline coverage.
2. ✅ **Research & Architecture**: Formulated custom, multi-service architecture aligned with industry best-practices.
3. ✅ **Draft YAMLs**: Generated fully-formed, production-ready GitHub Actions YAML pseudocode.
4. ✅ **Consolidate**: Built a comprehensive Markdown blueprint consolidating code, structures, and secrets.
5. ✅ **Create GitHub Issue**: Created this issue automatically using the GitHub REST API.

## Next Steps
- [ ] Review the proposed CI/CD workflows with the engineering team.
- [ ] Set up the specified GitHub Secrets in repository settings.
- [ ] Create the `.github/workflows/` directory and commit the YAML workflows.
- [ ] Perform trial runs of the pipelines to verify permissions.
"""
        issue_url = self.github_integration.create_issue(
            title=title,
            body=body,
            labels=["ci-cd", "architecture-blueprint", "github-actions"]
        )
        return issue_url
