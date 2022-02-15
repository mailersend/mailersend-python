"""
Handles /inbound endpoint
Doc: https://developers.mailersend.com/api/v1/inbound.html
"""

import requests
from mailersend.base import base


class NewInbound(base.NewAPIClient):
    """
    Instantiates the /inbound endpoint object
    """

    pass

    def get_inbound_routes(self):
        """
        Get a list of all inbound routes

        Returns the JSON response of MailerSend API
        """
        request = requests.get(f"{self.api_base}/inbound", headers=self.headers_default)
        return f"{request.status_code}\n{request.text}"

    def get_inbound_by_id(self, inbound_id):
        """
        Get info on an inbound route by its ID

        @params:
          inbound_id (str): An inbound route ID

        Returns the JSON response of MailerSend API
        """
        request = requests.get(
            f"{self.api_base}/inbound/{inbound_id}", headers=self.headers_default
        )
        return request.text

    def update_inbound_route(self, inbound_id, options):
        """
        Update an inbound route

        @params:
          inbound_id (str): An inbound route ID
          key (str): The key param to change
          value (object): The value to update key with

        Returns the JSON response of MailerSend API
        """

        request = requests.put(
            f"{self.api_base}/inbound/{inbound_id}",
            headers=self.headers_default,
            json=options,
        )
        return f"{request.status_code}\n{request.text}"

    def delete_inbound_route(self, inbound_id):
        """
        Returns the status code of delete inbound route operation

        @params:
          inbound_id (str): An inbound route ID
        """

        request = requests.delete(
            f"{self.api_base}/inbound/{inbound_id}",
            headers=self.headers_default,
        )
        return request.status_code

    def set_name(self, name, options):
        """
        Appends the 'name' param of inbound route options
        """
        options["name"] = name

    def set_domain_enabled(self, enabled, options):
        """
        Appends the 'domain_enabled' param of inbound route options
        """
        options["domain_enabled"] = enabled

    def set_inbound_domain(self, domain, options):
        """
        Appends the 'inbound_domain' param of inbound route options
        """
        options["inbound_domain"] = domain

    def set_catch_filter(self, content_json, options):
        """
        Appends the 'catch_filter' param of inbound route options
        """
        options["catch_filter"] = content_json

    def set_match_filter(self, content_json, options):
        """
        Appends the 'match_filter' param of inbound route options
        """
        options["match_filter"] = content_json

    def set_forwards(self, content_json, options):
        """
        Appends the 'forwards' param of inbound route options
        """
        options["forwards"] = content_json

    def add_inbound_route(self, domain_id, options):
        """
        Add a new inbound route

        @params:
          domain_id (str): For which domain will inbound route be created
          options (str): Creation options as defined in https://developers.mailersend.com/api/v1/inbound.html#add-an-inbound-route

        """

        options["domain_id"] = domain_id

        request = requests.post(
            f"{self.api_base}/inbound",
            headers=self.headers_default,
            json=options,
        )
        return f"{request.text}\n{request.status_code}"
