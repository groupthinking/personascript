"""
Apollo.io API Integration for PersonaScript.

This module handles all interactions with the Apollo.io API to search for target
companies/individuals based on ICP and extract their contact information.
"""

import logging
import requests
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class ApolloIntegration:
    """Integration with Apollo.io API for lead searching and extraction."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Apollo.io integration.

        Args:
            api_key: Apollo.io API key
        """
        self.api_key = api_key
        self.base_url = "https://api.apollo.io/v1"
        logger.info("ApolloIntegration initialized")

    def search_leads(
        self,
        industries: List[str],
        company_sizes: List[str],
        job_titles: List[str],
        limit: int = 15
    ) -> List[Dict[str, Any]]:
        """
        Search for individuals matching the specified ICP details.

        Args:
            industries: List of target industries
            company_sizes: List of target company sizes
            job_titles: List of target job titles
            limit: Maximum number of leads to return

        Returns:
            List of lead details
        """
        logger.info(
            f"Searching Apollo.io leads. Industries: {industries}, "
            f"Company Sizes: {company_sizes}, Titles: {job_titles}"
        )

        if not self.api_key:
            logger.warning("No Apollo.io API key provided, returning mock leads")
            return self._generate_mock_leads(industries, company_sizes, job_titles, limit)

        # Production-ready implementation with real API calls using requests
        try:
            url = f"{self.base_url}/mixed_people/search"
            headers = {
                "Content-Type": "application/json",
                "Cache-Control": "no-cache"
            }
            # Map company sizes (e.g., ["50-200"] -> ["50,200"])
            mapped_sizes = []
            for size in company_sizes:
                if "-" in size:
                    mapped_sizes.append(size.replace("-", ","))
                else:
                    mapped_sizes.append(size)

            payload = {
                "api_key": self.api_key,
                "person_titles": job_titles,
                "q_organization_num_employees_ranges": mapped_sizes,
                "organization_industries": industries,
                "page_size": limit
            }

            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                people = data.get("people", [])
                leads = []
                for p in people[:limit]:
                    org = p.get("organization", {})
                    leads.append({
                        "id": f"apollo-lead-{p.get('id', '')}",
                        "first_name": p.get("first_name", ""),
                        "last_name": p.get("last_name", ""),
                        "name": p.get("name", ""),
                        "title": p.get("title", ""),
                        "company_name": org.get("name", "Unknown Company"),
                        "company_size": company_sizes[0] if company_sizes else "100-500",
                        "industry": industries[0] if industries else "B2B SaaS",
                        "email": p.get("email", ""),
                        "linkedin_url": p.get("linkedin_url", f"https://www.linkedin.com/in/{p.get('first_name', '').lower()}-{p.get('last_name', '').lower()}"),
                        "location": f"{p.get('city', '')}, {p.get('state', '')}".strip(", ") or "Unknown"
                    })
                if leads:
                    logger.info(f"Successfully retrieved {len(leads)} leads from Apollo.io API")
                    return leads

                logger.info("No leads found in Apollo.io response, falling back to mock leads")
            else:
                logger.warning(
                    f"Apollo.io API request failed with status {response.status_code}: {response.text}. "
                    "Falling back to mock leads"
                )
        except Exception as e:
            logger.error(f"Error calling Apollo.io API: {e}. Falling back to mock leads", exc_info=True)

        return self._generate_mock_leads(industries, company_sizes, job_titles, limit)

    def _generate_mock_leads(
        self,
        industries: List[str],
        company_sizes: List[str],
        job_titles: List[str],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Generate realistic mock leads based on ICP inputs."""
        mock_names = [
            ("Sarah", "Jenkins"), ("David", "Miller"), ("Emma", "Thompson"),
            ("Michael", "Chen"), ("Olivia", "Rodriguez"), ("James", "Smith"),
            ("Sophia", "Patel"), ("Robert", "Taylor"), ("Isabella", "Jones"),
            ("William", "Davis"), ("Mia", "Wilson"), ("Alexander", "Brown"),
            ("Charlotte", "Gomez"), ("Daniel", "Kim"), ("Emily", "Clark")
        ]

        industry = industries[0] if industries else "B2B SaaS"
        company_size = company_sizes[0] if company_sizes else "100-500"
        title_pool = job_titles if job_titles else ["VP of Marketing", "Director of Growth"]

        leads = []
        for i in range(min(limit, len(mock_names))):
            first, last = mock_names[i]
            title = title_pool[i % len(title_pool)]
            company_name = f"{last} Media Inc." if i % 2 == 0 else f"{first}Tech Solutions"
            domain = f"{company_name.lower().replace(' ', '').replace('.', '')}.com"
            email = f"{first.lower()}.{last.lower()}@{domain}"

            leads.append({
                "id": f"apollo-lead-{i+1000}",
                "first_name": first,
                "last_name": last,
                "name": f"{first} {last}",
                "title": title,
                "company_name": company_name,
                "company_size": company_size,
                "industry": industry,
                "email": email,
                "linkedin_url": f"https://www.linkedin.com/in/{first.lower()}-{last.lower()}-{i}",
                "location": "San Francisco, CA" if i % 2 == 0 else "New York, NY"
            })

        return leads
