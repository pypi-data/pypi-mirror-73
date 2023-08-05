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
        self._token = token
        try:
            self._decoded = jwt.decode(self._token, verify=False)
        except InvalidTokenError:
            raise ValueError('Invalid JWT token')

    def user_id(self):
        """ Returns the user_id provided by firebase
        """
        return self._decoded.get('user_id')

    def shops(self):
        """ Returns a list of shop_ids that the user has access to
        """
        claims = self._decoded.get('claims')
        if not claims:
            logging.error('claims not found')
            return []
        return claims.get('shop')

    def organizations(self):
        """ Returns a list of organization_ids that the user has access to
        """
        claims = self._decoded.get('claims')
        if not claims:
            logging.error('claims not found')
            return []
        return claims.get('organization')

    def data(self):
        """ Return the entire data from the token
        """
        return self._decoded

    def token(self):
        """ Returns the original JWT token
        """
        return self._token
