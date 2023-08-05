#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `styler_identity` package."""

from unittest.mock import patch
import pytest


from styler_identity.identity import Identity


@pytest.fixture
def token():
    return (
        'eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc2MjNlMTBhMDQ1MTQwZjFjZmQ0YmUwNDY2Y2'
        'Y4MDM1MmI1OWY4MWUiLCJ0eXAiOiJKV1QifQ.eyJyb2xlcyI6WyJzeXNhZG1pbiIsI'
        'nN0YWZmIiwiYWRtaW4iXSwiY2xhaW1zIjp7InNob3AiOlsiMTIzNDUiLCIzMzQ0MiJ'
        'dLCJvcmdhbml6YXRpb24iOlsiMzMzMzMiXX0sImlzcyI6Imh0dHBzOi8vc2VjdXJld'
        'G9rZW4uZ29vZ2xlLmNvbS9mYWN5LWRldmVsb3BtZW50IiwiYXVkIjoiZmFjeS1kZXZ'
        'lbG9wbWVudCIsImF1dGhfdGltZSI6MTU5NDAwNjAxNiwidXNlcl9pZCI6IjZuYWY4M'
        'Gp0eWJWUnVQMjJlWWNJWUdYMktKSzIiLCJzdWIiOiI2bmFmODBqdHliVlJ1UDIyZVl'
        'jSVlHWDJLSksyIiwiaWF0IjoxNTk0MDA2MDE2LCJleHAiOjE1OTQwMDk2MTYsImVtY'
        'WlsIjoiYnJ1bm8uc3VnYW5vQHN0eWxlci5saW5rIiwiZW1haWxfdmVyaWZpZWQiOmZ'
        'hbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImJydW5vLnN1Z'
        '2Fub0BzdHlsZXIubGluayJdfSwic2lnbl9pbl9wcm92aWRlciI6ImN1c3RvbSJ9fQ.'
        'EkyieQPlrQ7kQ9nAaTMz7O_PCNXo_c77Apx2aIes1CKfkeD1kXwLCd6V_Vy8NfNebL'
        '-aOymuCpssHv6Eew3qaIJ1qCrPWcLQ3xOvSYoStbk8dq4ZFHnKz68M7JPaUQg-wD0J'
        '5wnbkqHDtLwEG9QPdsFHK3pYNtgtz-5nP6P9RgDpmkmsz_Orf0el2etMzmPN_DZN0F'
        'zExd_4l2xcyk2Hs5Hrfz1OlZp6wuppoP4fNfgVzqdFS_uYugIgUR2Nn_dpD0qzh61T'
        '9MW8Rw5r68jBgaA04DUAY5EZtBIZotDFRMh-ZEMLD7HBDtE4ytawO-ADr_C5fAh4KP'
        'HS-mgPvZA0ag'
    )

@pytest.fixture
def empty_token():
    return (
        'eyJhbGciOiJSUzI1NiIsImtpZCI6IjdkNTU0ZjBjMTJjNjQ3MGZiMTg1MmY3OWRiZjY'
        '0ZjhjODQzYmIxZDciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXR'
        'va2VuLmdvb2dsZS5jb20vZmFjeS1kZXZlbG9wbWVudCIsImF1ZCI6ImZhY3ktZGV2ZW'
        'xvcG1lbnQiLCJhdXRoX3RpbWUiOjE1OTM2NzI5MzYsInVzZXJfaWQiOiI2bmFmODBqd'
        'HliVlJ1UDIyZVljSVlHWDJLSksyIiwic3ViIjoiNm5hZjgwanR5YlZSdVAyMmVZY0lZ'
        'R1gyS0pLMiIsImlhdCI6MTU5MzY3MjkzNiwiZXhwIjoxNTkzNjc2NTM2LCJlbWFpbCI'
        '6ImJydW5vLnN1Z2Fub0BzdHlsZXIubGluayIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZS'
        'wiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJicnVuby5zdWdhbm9Ac'
        '3R5bGVyLmxpbmsiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.iRtVz'
        'aAEXvWVSGXTi5CFu6bG_kIX3D8M85mZI66yku4hzK5YQ0UUlBYiiz_wO1lTqsIUy5e6'
        'rO8-xWYSfh-rtFQP_e3uDtNFIZGoUuD_UJjgLPT0MXWYsTt4Ov2Qhyh1PPNrnGMxNKQ'
        'YB46uq4qiCkay9oNbo3Gs5edS_bRTxrdv8lSqEvOJbnzJy4TbD6KDrCO0tU3onEcKYz'
        'qfB7308k08N-rmqjtMpI5xxAvHrbg3Fqop7gRWg2wi6PCRjD-UB-Euez7BsVXgF6nYQ'
        'PUQzu1sVnAkhiDCXNDbH8f3mG5h_aR92ri_GfcsEh52MlLOc0MtSLvMIZ3Sv_NoLauK1A'
    )

class TestIdentity:
    """ Tests 
    """
    def test_invalid_token(self):
        with pytest.raises(ValueError) as expected:
            Identity('invalid token')

        assert str(expected.value) == 'Invalid JWT token'

    def test_valid_token(self, token):
        idem = Identity(token)

        assert isinstance(idem, Identity)

    def test_token(self, token):
        idem = Identity(token)

        tk = idem.token()

        assert token == tk

    def test_user_id(self, token):
        idem = Identity(token)

        user_id = idem.user_id()

        assert user_id == '6naf80jtybVRuP22eYcIYGX2KJK2'

    def test_shops(self, token):
        idem = Identity(token)

        shops = idem.shops()

        assert shops == ['12345', '33442']

    @patch('logging.error')
    def test_shops_none(self, mocked_error, empty_token):
        idem = Identity(empty_token)

        shops = idem.shops()

        assert shops == []
        mocked_error.assert_called_once

    def test_organizations(self, token):
        idem = Identity(token)

        organizations = idem.organizations()

        assert organizations == ['33333']

    @patch('logging.error')
    def test_organizations_none(self, mocked_error, empty_token):
        idem = Identity(empty_token)

        organizations = idem.organizations()

        assert organizations == []
        mocked_error.assert_called_once

    def test_data(self, token):
        idem = Identity(token)
        expected_keys = {
            'roles',
            'claims',
            'iss',
            'aud',
            'auth_time',
            'user_id',
            'sub',
            'iat',
            'exp',
            'email',
            'email_verified',
            'firebase'
        }

        data = idem.data()

        assert set(data.keys()) == expected_keys
