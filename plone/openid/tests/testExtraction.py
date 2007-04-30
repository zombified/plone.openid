from plone.openid.tests.oitestcase import FunctionalOpenIdTestCase
from zExceptions import Redirect


class TestOpenIdExtraction(FunctionalOpenIdTestCase):

    def testEmptyExtraction(self):
        """Test if we do not invent credentials out of thin air.
        """
        creds=self.app.folder.openid.extractCredentials(self.app.REQUEST)
        self.assertEqual(creds, {})


    def testRedirect(self):
        """Test if a redirect is generated for a login attempt.
        This test requires a working internet connection!
        """
        self.app.REQUEST.form["__ac_identity_url"]=self.identity
        self.assertRaises(Redirect,
                self.app.folder.openid.extractCredentials,
                self.app.REQUEST)


    def testPositiveOpenIdResponse(self):
        """Test if a positive authentication is extracted.
        """
        self.app.REQUEST.form.update(self.server_response)
        creds=self.app.folder.openid.extractCredentials(self.app.REQUEST)
        self.assertEqual(creds["openid.identity"], self.identity)
        self.assertEqual(creds["openid.mode"], "id_res")
        self.assertEqual(creds["openid.return_to"], "return_to")


    def testNegativeOpenIdResponse(self):
        """Check if a cancelled authentication request is correctly ignored.
        """
        self.app.REQUEST.form.update(self.server_response)
        self.app.REQUEST.form["openid.mode"]="cancel"
        creds=self.app.folder.openid.extractCredentials(self.app.REQUEST)
        self.assertEqual(creds, {})


    def testFormRedirectPriorities(self):
        """Check if a new login identity has preference over openid server
        reponse.
        """
        self.app.REQUEST.form.update(self.server_response)
        self.app.REQUEST.form["__ac_identity_url"]=self.identity
        self.assertRaises(Redirect,
                self.app.folder.openid.extractCredentials,
                self.app.REQUEST)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite=TestSuite()
    suite.addTest(makeSuite(TestOpenIdExtraction))
    return suite
