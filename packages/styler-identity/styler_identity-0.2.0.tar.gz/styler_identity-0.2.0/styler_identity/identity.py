# -*- coding: utf-8 -*-

""" Identity class

    Encapsulates the logic to handle JWT tokens
"""

import logging

from jwt.exceptions import InvalidTokenError
import jwt


class Identity:
    """ Holds the identity of the logged user
    """
    def __init__(self, token):
        self.token = token
        try:
            self.decoded = jwt.decode(self.token, verify=False)
        except InvalidTokenError:
            raise ValueError('Invalid JWT token')

    def get_user_id(self):
        """ Returns the user_id provided by firebase
        """
        return self.decoded.get('user_id')

    def get_shops(self):
        """ Returns a list of shop_ids that the user has access to
        """
        claims = self.decoded.get('claims')
        if not claims:
            logging.error('claims not found')
            return []
        return claims.get('shop')

    def get_organizations(self):
        """ Returns a list of organization_ids that the user has access to
        """
        claims = self.decoded.get('claims')
        if not claims:
            logging.error('claims not found')
            return []
        return claims.get('organization')

    def get_token(self):
        """ Returns the original JWT token
        """
        return self.token
