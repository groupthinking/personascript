# PersonaScript Integrations: HubSpot CMS/CRM & Contentful Headless CMS

This guide covers the architecture, setup, field mapping strategy, usage, and troubleshooting for the HubSpot and Contentful API integrations in PersonaScript.

---

## 💡 Overview

The `PersonaScriptIntegrationAgent` provides a fully automated pipeline to map, validate, deploy, and document PersonaScript-generated marketing contents (e.g., blog posts, email sequences) into:
1. **HubSpot CRM/CMS**: For blog publishing and single-send marketing emails.
2. **Contentful Headless CMS**: For structured, localized content entries.

---

## 🔑 Authentication & API Configuration

To authenticate connection requests, configure the following credentials as environment variables or in your `.env` configuration file:

### 1. HubSpot Configuration

HubSpot supports both modern OAuth Access Tokens/Private App Tokens and legacy Developer API Keys.

*   **`HUBSPOT_ACCESS_TOKEN`** (Recommended): A HubSpot Private App Token.
    *   To set this up, go to *Settings -> Integrations -> Private Apps* in HubSpot and click **Create private app**.
    *   Under **Scopes**, request:
        *   `content` (for CMS blog post creation/publishing).
        *   `marketing-email` (for template and Single-Send Email operations).
*   **`HUBSPOT_API_KEY`** (Legacy): Your portal's Developer HAPIKEY.

### 2. Contentful Configuration

The Contentful integration utilizes Contentful's **Management API** (CMA) to create draft entries and publish them.

*   **`CONTENTFUL_SPACE_ID`**: The target space ID containing your content models.
*   **`CONTENTFUL_ACCESS_TOKEN`**: A Contentful Management Token (starts with `CFPAT-`).
    *   To generate this, go to *Settings -> APIs -> Content management tokens* in your Contentful space dashboard.
*   **`CONTENTFUL_ENVIRONMENT_ID`** (Optional): The target environment (defaults to `master`).

---

## 🗺️ Content Schema Mapping Strategy

To bridge PersonaScript's internal schemas and platform-specific objects/fields, the agent implements a smart semantic mapper.

### HubSpot CMS/CRM Mapping

The agent translates generic payload fields into the property structure expected by HubSpot:
*   **CMS Blog Posts (V3 CMS API)**:
    *   `title` or `name` $\rightarrow$ `name` and `htmlTitle` (Required fields).
    *   `body` or `content` $\rightarrow$ `postBody`.
    *   `summary` or `excerpt` $\rightarrow$ `postSummary`.
    *   `author` $\rightarrow$ `blogAuthorId`.
    *   `publish_date` $\rightarrow$ `publishDate`.
*   **Marketing Emails (V3 Marketing API)**:
    *   `title` or `subject` $\rightarrow$ `subject` and `name`.
    *   `body` or `html_content` $\rightarrow$ `htmlBody`.
    *   `from_name` $\rightarrow$ `fromName`.
    *   `reply_to` $\rightarrow$ `replyTo`.

### Contentful Localized Entry Mapping

Contentful stores entries under localized structures. The agent accepts standard flat properties and automatically converts them to localized field maps.
For example, a flat mapped dictionary like:
```json
{
  "title": "A New Strategy Guide",
  "body": "Markdown text..."
}
```
Is transformed into the following localized Contentful entry structure (using `en-US` as default):
```json
{
  "fields": {
    "title": {
      "en-US": "A New Strategy Guide"
    },
    "body": {
      "en-US": "Markdown text..."
    }
  }
}
```

---

## 🚀 Usage Instructions

Below is a complete code example showing how to run the `PersonaScriptIntegrationAgent` programmatically:

```python
from src.agents.persona_script_integration_agent import (
    PersonaScriptIntegrationAgent,
    ContentSchema,
    HubSpotObjectDefinition,
    ContentfulContentModelDefinition,
    IntegrationAgentInputs
)
from src.config import get_config

# 1. Retrieve credentials
config = get_config()

# 2. Instantiate the integration agent
agent = PersonaScriptIntegrationAgent(
    hubspot_access_token=config["hubspot"]["access_token"],
    contentful_space_id=config["contentful"]["space_id"],
    contentful_access_token=config["contentful"]["access_token"],
    github_token=config["github"]["token"],
    github_repo=config["github"]["repo"]
)

# 3. Structure PersonaScript content
content_payload = {
    "title": "Scaling Content Velocity in Growth-Stage B2B SaaS",
    "body": "This is a detailed guide on automated personalization...",
    "summary": "Accelerate growth funnel conversions with consistent brand content.",
    "author": "Jordan Growth",
    "publish_date": "2025-10-12"
}

# 4. Define content schema
content_schema = ContentSchema(
    content_type="blog_post",
    fields={
        "title": "string",
        "body": "string",
        "summary": "string",
        "author": "string",
        "publish_date": "string"
    }
)

# 5. Define target objects structures
hubspot_object_def = HubSpotObjectDefinition(
    object_type="blog_post",
    properties=["name", "htmlTitle", "postBody", "postSummary", "blogAuthorId", "publishDate"]
)

contentful_content_model_def = ContentfulContentModelDefinition(
    content_type_id="blogPost",
    fields=["title", "body", "summary", "author", "publishDate"]
)

# 6. Bundle inputs
inputs = IntegrationAgentInputs(
    content_payload=content_payload,
    content_schema=content_schema,
    hubspot_object_def=hubspot_object_def,
    contentful_content_model_def=contentful_content_model_def
)

# 7. Execute the publishing workflow
outputs = agent.execute(inputs)

# 8. Access deployment results
if outputs.success:
    print(f"✅ Deployment successful!")
    print(f"HubSpot ID: {outputs.hubspot_deployment_status['id']}")
    print(f"Contentful Entry ID: {outputs.contentful_deployment_status['id']}")
    print(f"GitHub Issue URL: {outputs.github_issue_url}")
else:
    print(f"❌ Deployment failed.")
```

---

## 🛠️ Troubleshooting & Common Resolutions

### 1. Contentful Version Conflicts (`VersionMismatch`)
*   **Symptom**: `requests.put` to Contentful update/publish returns `409 Conflict`.
*   **Cause**: Contentful requires providing the exact, most up-to-date entry version number inside the `X-Contentful-Version` header. If a concurrent change occurred or the version tracking in your code is stale, updates will fail.
*   **Resolution**: Always parse and record the version field from Contentful's latest response `data["sys"]["version"]` before making an update.

### 2. Missing HubSpot Required Fields
*   **Symptom**: HubSpot blog posts publishing fails with validation error.
*   **Cause**: HubSpot blog post creation requires `name` and `htmlTitle` fields.
*   **Resolution**: The `PersonaScriptIntegrationAgent`'s semantic mapper automatically maps source `title` fields to both properties if missing. Ensure your source payload contains a valid `title` or `name` field.

### 3. Localization Mismatch on Contentful
*   **Symptom**: Field mapping is ignored or returns structure errors when reading the Contentful entry.
*   **Cause**: The Contentful target space's model expects a different default locale (e.g., `en-GB`, `de-DE`) instead of `en-US`.
*   **Resolution**: Customize the `locale` parameter in `create_entry` or `localize_fields` calls to match your Space's default locale.
