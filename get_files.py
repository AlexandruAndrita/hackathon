import json
from typing import Any, Dict, List, Optional
from pprint import pprint
from config import REGISTER_HANDLER_API_KEY

import requests


class HandelsregisterError(Exception):
    """Custom exception for Handelsregister API errors."""
    pass


class HandelsregisterClient:
    """
    Python client for the handelsregister.ai API.
    Docs: https://handelsregister.ai/en/documentation
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://handelsregister.ai/api/v1",
        timeout: int = 30,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        # Recommended auth method: x-api-key header:contentReference[oaicite:3]{index=3}
        self.session.headers.update({"x-api-key": self.api_key})

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        stream: bool = False,
    ) -> requests.Response:
        url = f"{self.base_url}{path}"
        try:
            resp = self.session.request(
                method=method.upper(),
                url=url,
                params=params,
                timeout=self.timeout,
                stream=stream,
            )
        except requests.RequestException as e:
            print(f"Request failed: {e}")

        # # Basic error handling
        # if not resp.ok:
        #     try:
        #         err_json = resp.json()
        #     except ValueError:
        #         err_json = None

        #     msg = f"API error {resp.status_code}"
        #     if err_json and "message" in err_json:
        #         msg += f": {err_json['message']}"
        #     raise HandelsregisterError(msg)

        return resp

    def search_organizations(
        self,
        query: str,
        *,
        limit: int = 10,
        skip: int = 0,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Search for organizations by name / query.
        Wraps GET /v1/search-organizations.:contentReference[oaicite:4]{index=4}
        """
        params: Dict[str, Any] = {
            "q": query,
            "limit": limit,
            "skip": skip,
        }

        if filters:
            # filters must be JSON-encoded per docs
            params["filters"] = json.dumps(filters)

        resp = self._request("GET", "/search-organizations", params=params)
        return resp.json()

    def fetch_organization(
        self,
        query: str,
        *,
        features: Optional[List[str]] = None,
        ai_search: bool = True,
    ) -> Dict[str, Any]:
        """
        Fetch full profile for one company.
        Wraps GET /v1/fetch-organization.:contentReference[oaicite:5]{index=5}

        `query` can be:
            - company name (e.g. "ODDO BHF SE")
            - register number + court
            - other search text
        """
        params: Dict[str, Any] = {"q": query}

        if features:
            # `feature` can be repeated; requests handles list values as multiple params
            params["feature"] = features

        if ai_search:
            params["ai_search"] = "on-default"

        resp = self._request("GET", "/fetch-organization", params=params)
        return resp.json()

    def fetch_document(
        self,
        company_id: str,
        document_type: str,
        *,
        output_path: str,
    ) -> None:
        """
        Download a PDF document (e.g. shareholders_list) for a company.
        Wraps GET /v1/fetch-document.:contentReference[oaicite:6]{index=6}

        document_type: 'shareholders_list', 'AD', 'CD', etc.
        """
        params = {
            "company_id": company_id,
            "document_type": document_type,
        }

        resp = self._request("GET", "/fetch-document", params=params, stream=True)

        # with open(output_path, "wb") as f:
        #     for chunk in resp.iter_content(chunk_size=8192):
        #         if chunk:
        #             f.write(chunk)

        return resp


client = HandelsregisterClient(REGISTER_HANDLER_API_KEY)

search_result = client.search_organizations(
    "ODDO BHF SE",
    limit=20,
)
# pprint(search_result)

entity_ids = []
for item in search_result["results"]:
    entity_ids.append(item["entity_id"])

print("Found entity IDs:", entity_ids)

profile = client.fetch_organization(
    "ODDO BHF",
    features=[
        "financial_kpi",
        "related_persons",
        "publications",
        "annual_financial_statements",
    ],
)
# pprint(profile)
json.dump(profile, open("oddo_bhf_profile.json", "w"), indent=2)

annual_financial_statements = profile["annual_financial_statements"]

# document_types = ["shareholders_list", "CD", "AD"]
document_types = ["CD", "AD"]

for document_type in document_types:
    try:
        
        response = client.fetch_document(
            company_id=entity_ids[0],
            document_type=document_type,
            output_path=f"oddo_bhf_{document_type}.pdf",
        )
        print(response)

        document_url = response.url
        print("Document URL:", document_url)

        content_type = response.headers.get("Content-Type", "")
        mime_type = content_type.split(";")[0].strip()
        print("MIME type:", mime_type)
    except Exception as e:
        print(f"Error getting document_type {document_type}: {e}")

# for doc in list_docs:
#     print(
#         f"Downloading {doc['document_type']} from {doc['fiscal_year']}..."
#     )
#     client.fetch_document(
#         company_id=profile["entity_id"],
#         document_type=doc["document_type"])