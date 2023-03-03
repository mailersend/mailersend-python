"""
Handles /identities endpoint
"""

import requests
from mailersend.base import base

class NewSenderIdentities(base.NewAPIClient):
    """
    Instantiates the /identities endpoint object
    """

    # you shall not
    pass

    def get_identities(self, domain_id=None, page=None, limit=25):
        """
        Get all sender identities

        @params:
          domain_id (string)
          page (int)
          limit (int): Min: `10`, Max: `100`, default is 25
        """

        passed_arguments = locals()
        query_params = {}

        for key, value in passed_arguments.items():
            if key != "self" and value is not None:
                query_params[key] = value

        request = requests.get(
            f"{self.api_base}/identities",
            headers=self.headers_default,
            params=query_params,
        )

        return f"{request.status_code}\n{request.text}"
    
    def get_identity(self, identity_id):
        """
        Get a single sender identity

        @params:
          identity_id (string)
        """

        request = requests.get(
            f"{self.api_base}/identities/{identity_id}",
            headers=self.headers_default,
        )

        return f"{request.status_code}\n{request.text}"
    
    def add_identitity(self, domain_id, name, email, reply_to_email=None, reply_to_name=None, add_note=False, personal_note=None):
        """
        Add a sender identity

        @params:
          domain_id (string)
          name (string) - Max 191 characters
          email (string) - Max 191 characters, unique
          reply_to_email (string)
          reply_to_name (string)
          add_note (boolean)
          personal_note (string)
        """

        data = {
            "domain_id": domain_id, 
            "name": name,
            "email": email
        }

        if reply_to_email != None:
            data["reply_to_email"] = reply_to_email

        if reply_to_name != None:
            data["reply_to_name"] = reply_to_name
        
        if add_note == True:
            data["add_note"] = add_note
            data["personal_note"] = personal_note

        request = requests.post(
            f"{self.api_base}/identities",
            headers=self.headers_default,
            json=data,
        )

        return f"{request.status_code}\n{request.text}"
    
    def update_identitity(self, identity_id, domain_id=None, name=None, email=None, reply_to_email=None, reply_to_name=None, add_note=False, personal_note=None):
        """
        Update a sender identity

        @params:
          identity_id (string)
          domain_id (string)
          name (string) - Max 191 characters
          email (string) - Max 191 characters, unique
          reply_to_email (string)
          reply_to_name (string)
          add_note (boolean)
          personal_note (string)
        """
        
        passed_arguments = locals()
        data = {}

        for key, value in passed_arguments.items():
            if key != "self" and key != "identity_id" and value is not None:
                data[key] = value

        request = requests.put(
            f"{self.api_base}/identities/{identity_id}",
            headers=self.headers_default,
            json=data,
        )

        return f"{request.status_code}\n{request.text}"
    
    def delete_identity(self, identity_id):
        """
        Delete a sender identity

        @params:
          identity_id (string)
        """
        
        request = requests.delete(
            f"{self.api_base}/identities/{identity_id}",
            headers=self.headers_default,
        )

        return request.text