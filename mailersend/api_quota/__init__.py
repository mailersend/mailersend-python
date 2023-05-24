"""
Handles /api-quota endpoint
"""

import requests
from mailersend.base import base


class NewApiQuota(base.NewAPIClient):
    """
    Instantiates the /api-quota endpoint object
    """

    pass

    def get_quota(self, page=1, limit=25, verified=False):
        query_params = {"page": page, "limit": limit, "verified": verified}

        request = requests.get(
            f"{self.api_base}/api-quota",
            headers=self.headers_default,
            params=query_params,
        )

        return request.text
