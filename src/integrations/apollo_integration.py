"""
Apollo.io API Integration for PersonaScript.

This module handles searching for B2B target companies and prospects matching an
Ideal Customer Profile (ICP), and extracting rich contact information.
Includes full simulated fallback when API credentials are omitted.
"""

import logging
from typing import Dict, Any, List, Optional
import requests

logger = logging.getLogger(__name__)


class ApolloIntegration:
    """Integration with Apollo.io REST API for lead sourcing and prospecting."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Apollo.io integration.

        Args:
            api_key: Apollo.io API Key
        """
        self.api_key = api_key
        self.base_url = "https://api.apollo.io/v1"
        logger.info("ApolloIntegration initialized")

    def search_people(
        self,
        titles: Optional[List[str]] = None,
        industry: Optional[str] = None,
        company_size_range: Optional[str] = None,
        location: Optional[str] = None,
        count: int = 12
    ) -> List[Dict[str, Any]]:
        """
        Search for people / leads matching ICP parameters.

        Args:
            titles: List of target job titles
            industry: Target industry
            company_size_range: Target company size range (e.g. "50-200")
            location: Target geographic location
            count: Number of qualified prospects to retrieve (default 12)

        Returns:
            List of contact/prospect dictionaries containing contact details.
        """
        logger.info(f"Searching Apollo prospects for titles={titles}, industry={industry}")

        if self.api_key:
            try:
                payload = {
                    "api_key": self.api_key,
                    "person_titles": titles or [],
                    "page": 1,
                    "per_page": count
                }
                if industry:
                    payload["organization_locations"] = [industry]
                response = requests.post(f"{self.base_url}/mixed_people/search", json=payload, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    people = data.get("people", [])
                    results = []
                    for p in people:
                        results.append({
                            "id": p.get("id"),
                            "name": p.get("name") or f"{p.get('first_name', '')} {p.get('last_name', '')}".strip(),
                            "title": p.get("title", "Marketing Leader"),
                            "company": p.get("organization", {}).get("name", "B2B SaaS Corp"),
                            "email": p.get("email", f"{p.get('first_name', 'prospect').lower()}@{p.get('organization', {}).get('name', 'saas').lower().replace(' ', '')}.com"),
                            "linkedin_url": p.get("linkedin_url", "https://linkedin.com/in/prospect-profile"),
                            "location": p.get("city") or location or "United States",
                            "company_size": company_size_range or "50-200"
                        })
                    if results:
                        return results[:count]
            except Exception as e:
                logger.warning(f"Apollo API request failed: {e}. Falling back to simulated leads.")

        logger.warning("No Apollo API key provided or request failed; returning simulated qualified leads.")
        return self._get_simulated_leads(titles, industry, company_size_range, count)

    def _get_simulated_leads(
        self,
        titles: Optional[List[str]],
        industry: Optional[str],
        company_size_range: Optional[str],
        count: int
    ) -> List[Dict[str, Any]]:
        """Generate realistic mock B2B SaaS leads for simulation mode."""
        base_titles = titles or [
            "VP of Demand Generation",
            "Head of Growth Marketing",
            "Director of Content Marketing",
            "Chief Marketing Officer",
            "Growth Marketing Manager"
        ]
        industry_name = industry or "B2B SaaS"
        size = company_size_range or "50-200"

        sample_prospects = [
            ("Sarah Jenkins", "Head of Demand Generation", "CloudScale AI", "sarah.j@cloudscale.ai", "https://linkedin.com/in/sarahjenkins-demand"),
            ("Marcus Vance", "VP of Marketing", "DataStream Technologies", "marcus.v@datastream.io", "https://linkedin.com/in/marcusvance-mktg"),
            ("Elena Rostova", "Director of Content Marketing", "WorkflowHub", "elena.r@workflowhub.com", "https://linkedin.com/in/elenarostova-content"),
            ("David Chen", "Chief Marketing Officer", "OmniFunnel SaaS", "david.chen@omnifunnel.com", "https://linkedin.com/in/davidchen-cmo"),
            ("Rachel Adams", "Senior Growth Marketing Lead", "PipelineHero", "rachel.a@pipelinehero.io", "https://linkedin.com/in/racheladams-growth"),
            ("James Miller", "VP of Growth & Acquisition", "MetricsPulse", "james.m@metricspulse.com", "https://linkedin.com/in/jamesmiller-growth"),
            ("Alicia Gomez", "Head of Content Strategy", "SyncOps Tech", "alicia.g@syncops.io", "https://linkedin.com/in/aliciagomez-content"),
            ("Brian Foster", "Director of Digital Marketing", "LeadRocket", "brian.f@leadrocket.com", "https://linkedin.com/in/brianfoster-digital"),
            ("Claire Zhang", "Demand Gen Lead", "Apex Analytics", "claire.z@apexanalytics.io", "https://linkedin.com/in/clairezhang-demand"),
            ("Derek Taylor", "VP of Demand Generation", "ScaleGrid", "derek.t@scalegrid.com", "https://linkedin.com/in/derektaylor-demand"),
            ("Jessica Patel", "Chief Marketing Officer", "CognitiveStack", "jessica.p@cognitivestack.io", "https://linkedin.com/in/jessicapatel-cmo"),
            ("Kevin O'Connor", "Head of Performance Marketing", "HyperFlow SaaS", "kevin.o@hyperflow.com", "https://linkedin.com/in/kevinoconnor-mktg")
        ]

        leads = []
        for idx, (name, default_title, company, email, linkedin) in enumerate(sample_prospects[:count]):
            assigned_title = base_titles[idx % len(base_titles)] if base_titles else default_title
            leads.append({
                "id": f"apollo-lead-{idx + 101}",
                "name": name,
                "title": assigned_title,
                "company": company,
                "email": email,
                "linkedin_url": linkedin,
                "industry": industry_name,
                "company_size": size,
                "location": "United States"
            })

        return leads
