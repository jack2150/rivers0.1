from django.test import TestCase
from django.core.urlresolvers import reverse


class TestViews(TestCase):
    def setUp(self):
        """
        ready up all variables and test class
        """
        print '=' * 100
        print "<%s> currently run: %s" % (self.__class__.__name__, self._testMethodName)
        print '-' * 100 + '\n'

    def tearDown(self):
        """
        remove variables after test
        """
        print '\n' + '=' * 100 + '\n\n'

    def test_index(self):
        """
        Not yet!!!
        """
        pass

    def test_webix_js(self):
        """
        Test webix js url return a correct files
        """
        response = self.client.get(reverse('pos_view_webix_js'))

        print 'content-type: %s\n' % response['Content-Type']
        self.assertEqual(response['Content-Type'], 'application/javascript')

        for item in ['positions', 'menu_links']:
            print '"%s" var found!' % item
            self.assertIn(item, response.content)

    def test_logic_js(self):
        """
        Test logic js url return a correct files
        """
        response = self.client.get(reverse('pos_view_logic_js'))

        print 'content-type: %s\n' % response['Content-Type']
        self.assertEqual(response['Content-Type'], 'application/javascript')

        for item in ['menu_init']:
            print '"%s" var found!' % item
            self.assertIn(item, response.content)

