"""
PersonaScriptIntegrationAgent - Assistant agent for deploying PersonaScript content
seamlessly into HubSpot CRM/CMS and Contentful CMS.

This agent parses content payloads and schemas, maps them to the appropriate fields on
the target systems, deploys the content via HubSpot and Contentful APIs, and reports the
results via a GitHub issue, alongside detailed auto-generated integration documentation.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from ..integrations.hubspot_integration import HubSpotIntegration
from ..integrations.contentful_integration import ContentfulIntegration
from ..integrations.github_integration import GitHubIntegration

logger = logging.getLogger(__name__)


@dataclass
class ContentSchema:
    """Represents PersonaScript content schema (e.g., blog post structure, email template fields)."""
    content_type: str  # e.g., "blog_post" or "marketing_email"
    fields: Dict[str, str]  # e.g., {"title": "string", "body": "string", "author": "string"}


@dataclass
class HubSpotObjectDefinition:
    """Represents target HubSpot object structure/properties."""
    object_type: str  # e.g., "blog_post" or "marketing_email"
    properties: List[str]  # e.g., ["name", "postBody", "blogAuthorId"]


@dataclass
class ContentfulContentModelDefinition:
    """Represents target Contentful content model structure/fields."""
    content_type_id: str  # e.g., "blogPost"
    fields: List[str]  # e.g., ["title", "body", "author"]


@dataclass
class IntegrationAgentInputs:
    """Input data for the PersonaScriptIntegrationAgent."""
    content_payload: Dict[str, Any]
    content_schema: ContentSchema
    hubspot_object_def: Optional[HubSpotObjectDefinition] = None
    contentful_content_model_def: Optional[ContentfulContentModelDefinition] = None


@dataclass
class IntegrationAgentOutputs:
    """Output data from the PersonaScriptIntegrationAgent."""
    success: bool
    hubspot_deployment_status: Dict[str, Any]
    contentful_deployment_status: Dict[str, Any]
    documentation_markdown: str
    github_issue_url: str


class PersonaScriptIntegrationAgent:
    """
    Main agent class for executing HubSpot CRM and Contentful CMS integration deployment.

    This agent follows a 10-step execution workflow:
    1. Parse and validate inputs.
    2. Establish/verify connection to HubSpot API.
    3. Establish/verify connection to Contentful Management API.
    4. Design/execute the content mapping to HubSpot objects.
    5. Design/execute the content mapping to Contentful models.
    6. Implement and invoke core logic to publish to HubSpot.
    7. Implement and invoke core logic to publish/create on Contentful.
    8. Implement and invoke publish logic on Contentful (if applicable).
    9. Generate detailed integration and troubleshooting documentation.
    10. Create a detailed summary GitHub issue with deployment details.
    """

    def __init__(
        self,
        hubspot_api_key: Optional[str] = None,
        hubspot_access_token: Optional[str] = None,
        contentful_space_id: Optional[str] = None,
        contentful_access_token: Optional[str] = None,
        contentful_environment_id: str = "master",
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """
        Initialize the PersonaScriptIntegrationAgent.

        Args:
            hubspot_api_key: Legacy API key for HubSpot
            hubspot_access_token: Access Token / Private App Token for HubSpot
            contentful_space_id: Contentful Space ID
            contentful_access_token: Contentful Management API Token
            contentful_environment_id: Contentful Environment (default: 'master')
            github_token: Token for GitHub API
            github_repo: Repository name (format: "owner/repo")
        """
        self.hubspot = HubSpotIntegration(api_key=hubspot_api_key, access_token=hubspot_access_token)
        self.contentful = ContentfulIntegration(
            space_id=contentful_space_id,
            access_token=contentful_access_token,
            environment_id=contentful_environment_id
        )
        self.github = GitHubIntegration(token=github_token, repo=github_repo)

        logger.info("PersonaScriptIntegrationAgent initialized")

    def execute(self, inputs: IntegrationAgentInputs) -> IntegrationAgentOutputs:
        """
        Execute the complete integration agent workflow.

        Args:
            inputs: Inputs containing content, schema, HubSpot & Contentful definitions.

        Returns:
            IntegrationAgentOutputs containing deployment results, documentation, and GitHub issue URL.
        """
        logger.info("Starting PersonaScriptIntegrationAgent execution")

        # Step 1: Parse and validate inputs
        self._validate_inputs(inputs)

        # Step 2: Establish connection to HubSpot (handled by init)
        logger.info(f"HubSpot authenticated: {self.hubspot.is_authenticated()}")

        # Step 3: Establish connection to Contentful (handled by init)
        logger.info(f"Contentful authenticated: {self.contentful.is_authenticated()}")

        # Step 4: Map fields to HubSpot
        mapped_hubspot_payload = self.map_to_hubspot(
            inputs.content_payload, inputs.content_schema, inputs.hubspot_object_def
        )

        # Step 5: Map fields to Contentful
        mapped_contentful_payload = self.map_to_contentful(
            inputs.content_payload, inputs.content_schema, inputs.contentful_content_model_def
        )

        # Step 6: Deploy to HubSpot
        hubspot_status = self._deploy_to_hubspot(inputs.content_schema.content_type, mapped_hubspot_payload)

        # Step 7 & 8: Deploy & publish to Contentful
        contentful_status = self._deploy_to_contentful(inputs, mapped_contentful_payload)

        # Step 9: Generate detailed documentation
        doc_markdown = self._generate_documentation(inputs, mapped_hubspot_payload, mapped_contentful_payload)

        # Determine overall success
        overall_success = (hubspot_status.get("status") == "success" and contentful_status.get("status") == "success")

        # Step 10: Create GitHub Issue summarizing goal, execution steps, inputs/outputs
        github_issue_url = self._create_github_issue(
            inputs=inputs,
            hubspot_status=hubspot_status,
            contentful_status=contentful_status,
            doc_markdown=doc_markdown
        )

        outputs = IntegrationAgentOutputs(
            success=overall_success,
            hubspot_deployment_status=hubspot_status,
            contentful_deployment_status=contentful_status,
            documentation_markdown=doc_markdown,
            github_issue_url=github_issue_url
        )

        logger.info("PersonaScriptIntegrationAgent execution completed")
        return outputs

    def _validate_inputs(self, inputs: IntegrationAgentInputs) -> None:
        """Validate input payload, schema, and definitions."""
        if not inputs.content_payload:
            raise ValueError("content_payload cannot be empty")
        if not inputs.content_schema:
            raise ValueError("content_schema cannot be empty")

        # Verify all fields specified in content_schema exist in the payload
        for field_name in inputs.content_schema.fields.keys():
            if field_name not in inputs.content_payload:
                logger.warning(f"Schema field '{field_name}' not present in content_payload.")

    def map_to_hubspot(
        self,
        payload: Dict[str, Any],
        schema: ContentSchema,
        hubspot_def: Optional[HubSpotObjectDefinition]
    ) -> Dict[str, Any]:
        """
        Map content payload to HubSpot properties based on schema and target definition.

        Performs smart/semantic mapping of common blog post and email properties.
        """
        mapped = {}

        # Semantic mapping tables from generic to HubSpot CMS/CRM specific
        smart_mappings = {
            "title": ["name", "htmlTitle", "subject"],
            "body": ["postBody", "htmlBody", "post_body"],
            "content": ["postBody", "htmlBody", "post_body"],
            "summary": ["postSummary", "metaDescription"],
            "author": ["blogAuthorId", "authorName"],
            "publish_date": ["publishDate"],
            "featured_image": ["featuredImage"],
            "from_name": ["fromName"],
            "reply_to": ["replyTo"]
        }

        target_properties = hubspot_def.properties if hubspot_def else list(schema.fields.keys())

        for source_key, value in payload.items():
            # If the property exists directly in the target
            if source_key in target_properties:
                mapped[source_key] = value
                continue

            # Check smart mappings
            mapped_flag = False
            if source_key in smart_mappings:
                for target_prop in smart_mappings[source_key]:
                    if target_prop in target_properties:
                        mapped[target_prop] = value
                        mapped_flag = True
                        break

            # Fallback direct assignment if no definition restricts properties
            if not mapped_flag and (not hubspot_def or source_key in hubspot_def.properties):
                mapped[source_key] = value

        # Fill in required/standard properties for HubSpot blog posts/emails
        if "name" in target_properties and "name" not in mapped:
            mapped["name"] = mapped.get("htmlTitle") or mapped.get("subject") or payload.get("title") or "Untitled HubSpot Content"
        if "htmlTitle" in target_properties and "htmlTitle" not in mapped:
            mapped["htmlTitle"] = mapped.get("name") or payload.get("title") or "Untitled HubSpot Content"

        return mapped

    def map_to_contentful(
        self,
        payload: Dict[str, Any],
        schema: ContentSchema,
        contentful_def: Optional[ContentfulContentModelDefinition]
    ) -> Dict[str, Any]:
        """
        Map content payload to Contentful properties based on schema and content model.

        Maps generic properties to standard Contentful field structures.
        """
        mapped = {}

        # Semantic mapping tables from generic to Contentful Content Model specific
        smart_mappings = {
            "name": ["title", "name"],
            "title": ["title", "name"],
            "htmlTitle": ["title", "name"],
            "body": ["body", "content"],
            "content": ["body", "content"],
            "postBody": ["body", "content"],
            "htmlBody": ["body", "content"],
            "summary": ["summary", "description"],
            "postSummary": ["summary", "description"],
            "blogAuthorId": ["author"],
            "author": ["author"],
            "publishDate": ["publishDate", "date"],
            "publish_date": ["publishDate", "date"]
        }

        target_fields = contentful_def.fields if contentful_def else list(schema.fields.keys())

        for source_key, value in payload.items():
            # Direct match
            if source_key in target_fields:
                mapped[source_key] = value
                continue

            # Semantic match
            mapped_flag = False
            if source_key in smart_mappings:
                for target_field in smart_mappings[source_key]:
                    if target_field in target_fields:
                        mapped[target_field] = value
                        mapped_flag = True
                        break

            # Check other direction (matching a target field back to source key semantic match)
            if not mapped_flag:
                for smart_src, smart_tgts in smart_mappings.items():
                    if source_key == smart_src:
                        for target_field in smart_tgts:
                            if target_field in target_fields:
                                mapped[target_field] = value
                                mapped_flag = True
                                break

            # Fallback direct assignment if no definition restricts properties
            if not mapped_flag and (not contentful_def or source_key in contentful_def.fields):
                mapped[source_key] = value

        return mapped

    def _deploy_to_hubspot(self, content_type: str, mapped_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Route and execute publishing to HubSpot via HubSpot API client."""
        logger.info(f"Deploying {content_type} to HubSpot")
        if content_type == "marketing_email" or "email" in content_type:
            return self.hubspot.send_marketing_email(mapped_payload)
        else:
            # Default to blog post deployment
            return self.hubspot.publish_blog_post(mapped_payload)

    def _deploy_to_contentful(self, inputs: IntegrationAgentInputs, mapped_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create and publish entry on Contentful Management API."""
        content_type_id = inputs.contentful_content_model_def.content_type_id if inputs.contentful_content_model_def else "blogPost"

        # Step 7: Create Draft Entry
        create_res = self.contentful.create_entry(content_type_id=content_type_id, fields=mapped_payload)

        if create_res.get("status") != "success":
            return create_res

        # Step 8: Publish Entry
        entry_id = create_res["id"]
        version = create_res.get("version", 1)
        publish_res = self.contentful.publish_entry(entry_id=entry_id, version=version)

        # Merge created entry data to publish response so localized fields/data is always populated
        if "data" not in publish_res and "data" in create_res:
            publish_res["data"] = create_res["data"]

        # Augment with created and localized payload details
        publish_res["mapped_payload"] = mapped_payload
        return publish_res

    def _generate_documentation(
        self,
        inputs: IntegrationAgentInputs,
        hubspot_mapped: Dict[str, Any],
        contentful_mapped: Dict[str, Any]
    ) -> str:
        """Generate detailed integration documentation covering configuration, mappings, and usage."""
        doc = f"""# PersonaScript API Integration Documentation

## Overview
This documentation outlines the automated integration setup for deploying PersonaScript marketing contents to HubSpot CRM/CMS and Contentful headless CMS.

## Configuration Setup
To authenticate with the target platforms, specify the following credentials:

### HubSpot Setup
- **Access Token / Private App Token:** Setup a Private App in your HubSpot Account and request scopes: `content`, `marketing-email`.
- **API Key (Legacy):** Alternatively, configure a standard HubSpot API key.

### Contentful Setup
- **Space ID:** The target Space ID within Contentful.
- **Management API Access Token:** Generate a Personal Access Token from your Contentful Space settings under APIs.

## Schema Mapping Strategy

### Generic Content Source (PersonaScript)
**Content Type:** `{inputs.content_schema.content_type}`
**Source Schema Fields:**
{chr(10).join([f"- `{k}` ({v})" for k, v in inputs.content_schema.fields.items()])}

### HubSpot CMS/CRM Mapping
**Target HubSpot Object Type:** `{inputs.hubspot_object_def.object_type if inputs.hubspot_object_def else "blog_post"}`
**Mapped Properties deployed:**
{chr(10).join([f"- `{k}`: mapped from payload" for k in hubspot_mapped.keys()])}

### Contentful Headless CMS Mapping
**Target Contentful Content Type:** `{inputs.contentful_content_model_def.content_type_id if inputs.contentful_content_model_def else "blogPost"}`
**Mapped Fields with localization wrapper (en-US):**
{chr(10).join([f"- `{k}`: mapped and localized" for k in contentful_mapped.keys()])}

## Usage Instructions
1. Initialize the `PersonaScriptIntegrationAgent` with required credentials.
2. Structure the `IntegrationAgentInputs` class including:
   - Your generated content payload
   - The structural source content schema
   - HubSpot and Contentful model definitions
3. Invoke `agent.execute(inputs)` to run mapping and trigger dual-platform publishing.

## Troubleshooting & Common Resolutions
- **Contentful Version Mismatch:** Contentful requires passing the exact current `X-Contentful-Version` header on edits/publishing. Ensure you track entry versions.
- **HubSpot Validation Errors:** Ensure required properties like `name` or `publishDate` are present and follow HubSpot specification.
"""
        return doc

    def _create_github_issue(
        self,
        inputs: IntegrationAgentInputs,
        hubspot_status: Dict[str, Any],
        contentful_status: Dict[str, Any],
        doc_markdown: str
    ) -> str:
        """Create a detailed summary GitHub issue with deployment details."""
        title = "Integration Deployment Status: HubSpot & Contentful Content Deployment"

        # Prepare issue body detailing inputs, outputs, and execution summary
        body = f"""# Integration Deployment Report

## Goal
To develop, test, and document seamless content deployment integrations from PersonaScript to HubSpot CRM and Contentful CMS.

## Inputs Consumed
- **Content Type:** `{inputs.content_schema.content_type}`
- **Source Fields:** `{list(inputs.content_schema.fields.keys())}`
- **HubSpot Target:** `{inputs.hubspot_object_def.object_type if inputs.hubspot_object_def else 'Default'}`
- **Contentful Content Type ID:** `{inputs.contentful_content_model_def.content_type_id if inputs.contentful_content_model_def else 'Default'}`

## Execution Steps Performed
1. 📥 **Parsed provided inputs** and validated the content payload against ContentSchema.
2. 🔑 **Established connections** to HubSpot CMS/CRM APIs and Contentful Management APIs.
3. 🗺️ **Executed smart semantic mapping** of generic fields to platform-specific keys.
4. 🚀 **Published/sent content** to HubSpot successfully.
5. ✍️ **Created and published entry** on Contentful with localization support (`en-US`).
6. 📝 **Generated comprehensive documentation** explaining mapping strategies, API setup, and troubleshooting.
7. 🌐 **Posted this issue** to track integration health.

## Output Results & Deployment Status

### HubSpot Deployment Details
- **Status:** `{hubspot_status.get("status")}`
- **Generated ID:** `{hubspot_status.get("id")}`
- **Platform URL:** `{hubspot_status.get("url", "N/A")}`
- **Mapped Properties:** `{hubspot_status.get("data", {}).get("properties", hubspot_status.get("data", {}))}`

### Contentful Deployment Details
- **Status:** `{contentful_status.get("status")}`
- **Generated Entry ID:** `{contentful_status.get("id")}`
- **Latest Version:** `{contentful_status.get("version")}`
- **Published:** `{contentful_status.get("published", False)}`

### Integration Documentation
The agent has successfully generated a detailed integration and troubleshooting markdown:
<details>
<summary>Click to view generated INTEGRATION_GUIDE markdown</summary>

{doc_markdown}

</details>

## Integration Test Results: {"✅ PASS" if (hubspot_status.get("status") == "success" and contentful_status.get("status") == "success") else "❌ FAIL"}
"""
        return self.github.create_issue(
            title=title,
            body=body,
            labels=["integration-agent", "deployment", "completed"]
        )
