"""
Handles /email-verification endpoint
"""

import requests
from mailersend.base import base


class NewEmailVerification(base.NewAPIClient):
    """
    Instantiates the /email-verification endpoint object
    """

    # you shall not
    pass

    def get_all_lists(self, page=1, limit=25):
        """
        Returns all email verification lists
        :param page: int
        :param limit: int
        """
        query_params = {"page": page, "limit": limit}

        request = requests.get(
            f"{self.api_base}/email-verification",
            headers=self.headers_default,
            params=query_params,
        )

        return f"{request.status_code}\n{request.text}"

    def get_list(self, email_verification_id):
        """
        Retrieve single email verification list
        :type email_verification_id: object
        """

        query_params = {"email_verification_id": email_verification_id}

        request = requests.get(
            f"{self.api_base}/email-verification",
            headers=self.headers_default,
            params=query_params,
        )

        return f"{request.status_code}\n{request.text}"

    def create_list(self, name, emails):
        """
        Create email verification list
        :param name: str
        :param emails: list
        :return:
        """

        data = {"name": name, "emails": emails}

        request = requests.post(
            f"{self.api_base}/email-verification",
            headers=self.headers_default,
            json=data,
        )

        return f"{request.status_code}\n{request.text}"

    def verify_list(self, email_verification_id):
        """
        Verify an email verification list
        :type email_verification_id: str
        """

        request = requests.get(
            f"{self.api_base}/email-verification/{email_verification_id}/verify",
            headers=self.headers_default,
        )

        return f"{request.status_code}\n{request.text}"

    def get_list_results(self, email_verification_id):
        """
        Get the result for each individual email of an email verification list
        :type email_verification_id: str
        """

        request = requests.get(
            f"{self.api_base}/email-verification/{email_verification_id}/results",
            headers=self.headers_default,
        )

        return f"{request.status_code}\n{request.text}"
