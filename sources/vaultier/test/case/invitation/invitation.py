from django.test.testcases import TransactionTestCase
from django.utils import unittest
from django.utils.unittest.suite import TestSuite
from rest_framework.status import HTTP_200_OK
from modelext.version.context import version_context_manager
from vaultier.test.tools.auth.api import register_api_call, auth_api_call
from vaultier.test.tools.member.api import invite_member_api_call
from vaultier.test.tools import format_response
from vaultier.test.tools.workspace.api import create_workspace_api_call


class ApiInviteTest(TransactionTestCase):

    def setUp(self):
        version_context_manager.set_enabled(False)

    def test_000_invitation(self):
        # create first user
        email = 'tomas@rclick.cz'
        register_api_call(email=email, nickname='tomas').data
        user1token = auth_api_call(email=email).data.get('token')

        # create workspace
        workspace1 = create_workspace_api_call(user1token, name='workspace1').data

        # user1 tries to invite user2
        response = invite_member_api_call(user1token,
                                          email='jan.misek@rclick.cz',
                                          workspace=workspace1.get('id'),
                                          send=True,
                                          resend=True
        )
        self.assertEqual(
            response.status_code,
            HTTP_200_OK,
            format_response(response))


def invitation_suite():
    suite = TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ApiInviteTest))
    return suite