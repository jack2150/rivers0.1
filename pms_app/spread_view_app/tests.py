from django.core.urlresolvers import reverse

from rivers2.settings import FILES
from pms_app.classes.identify.tests import TestReadyUp


# Create your tests here.
class TestSpreadViewAppViews(TestReadyUp):
    def setUp(self):
        """
        ready up all variables and test class
        """
        print '=' * 100
        print "<%s> currently run: %s" % (self.__class__.__name__, self._testMethodName)
        print '-' * 100 + '\n'

        self.real_date = '2014-09-05'
        self.path = FILES['tos_positions'] + '2014-09-06-PositionStatement.csv'

    def tearDown(self):
        """
        remove variables after test
        """
        print '\n' + '=' * 100 + '\n\n'

    def ready_spreads(self):
        """
        Ready positions in database before start test
        """
        self.ready_fname(date=self.real_date, path=self.path)

    def test_spreads_json(self):
        """
        Test spreads json return correct data
        """
        contexts = ['stock', 'hedge', 'leg_one']

        self.ready_spreads()

        response = self.client.get(
            reverse('spread_view_spreads_json', args=(self.real_date, contexts[0]))
        )

        print response.content
