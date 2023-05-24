"""
Handles /domains endpoint
Doc: https://developers.mailersend.com/api/v1/domains.html
"""

import requests
from mailersend.base import base


class NewDomain(base.NewAPIClient):
    """
    Instantiates the /domains endpoint object
    """

    pass

    def get_domains(self):
        """
        Get a list of all domains

        Returns the JSON response of MailerSend API
        """
        request = requests.get(f"{self.api_base}/domains", headers=self.headers_default)
        return request.text

    def get_domain_by_id(self, domain_id):
        """
        Get info on a domain by its ID

        @params:
          domain_id (str): A domain ID

        Returns the JSON response of MailerSend API
        """
        request = requests.get(
            f"{self.api_base}/domains/{domain_id}", headers=self.headers_default
        )
        return request.text

    def add_domain(self, domain_data):
        """
        Add a domain

        @params:
          domain_data (dic): Contains key:value data needed for creating a new domain

        """

        request = requests.post(
            f"{self.api_base}/domains",
            headers=self.headers_default,
            json=domain_data,
        )
        return request.text

    def delete_domain(self, domain_id):
        """
        Delete a domain

        @params:
          domain_id (str): A domain ID

        Returns the JSON response of MailerSend API
        """
        request = requests.delete(
            f"{self.api_base}/domains/{domain_id}", headers=self.headers_default
        )
        return request.status_code

    def get_recipients_for_domain(self, domain_id):
        """
        List all recipients for a domain

        @params:
          domain_id (str): A domain ID

        Returns the JSON response of MailerSend API
        """
        request = requests.get(
            f"{self.api_base}/domains/{domain_id}/recipients",
            headers=self.headers_default,
        )
        return request.text

    def update_domain_setting(self, domain_id, domain_data):
        """
        Returns the JSON response of MailerSend API

        @params:
          domain_id (str): A domain ID
          domain_data (dict): A key:value list that contains parameters for updating domain name

        """
        request = requests.put(
            f"{self.api_base}/domains/{domain_id}/settings",
            headers=self.headers_default,
            json=domain_data,
        )
        return request.text

    def get_dns_records(self, domain_id):
        """
        Returns the JSON response of dns records

        @params:
          domain_id (str): A domain ID

        """

        request = requests.get(
            f"{self.api_base}/domains/{domain_id}/dns-records",
            headers=self.headers_default,
        )
        return request.text

    def verify_domain(self, domain_id):
        """
        Returns the JSON response of verified domain

        @params:
          domain_id (str): A domain ID

        """

        request = requests.get(
            f"{self.api_base}/domains/{domain_id}/verify", headers=self.headers_default
        )
        return request.text
