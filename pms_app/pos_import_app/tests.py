from django.test import TestCase
from django.core.urlresolvers import reverse
import pms_app.models as pm

from rivers2.settings import FILES
from os import rename
from os.path import isfile


# Create your tests here.
class TestViews(TestCase):
    def setUp(self):
        """
        ready up all variables and test class
        """
        print '=' * 100
        print "<%s> currently run: %s" % (self.__class__.__name__, self._testMethodName)
        print '-' * 100 + '\n'

        fname = '2014-08-01-PositionStatement.csv'
        self.original_path = FILES['tos_positions'] + fname
        self.completed_path = FILES['tos_positions_completed'] + fname

    def tearDown(self):
        """
        remove variables after test
        """
        print '\n' + '=' * 100 + '\n\n'

    def move_csv_back_to_folder(self):
        """
        Move saved csv file back into original folder
        """
        # move back into original folder
        if isfile(self.completed_path):
            rename(self.completed_path, self.original_path)

    def test_index(self):
        """
        Test index page is working fine that
        display all positions csv files in javascript
        """
        response = self.client.get(reverse('pos_import_app_index'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'PositionStatement.csv', count=2)
        self.assertContains(response, '"id": "2014-08-01"', count=1)
        self.assertContains(response, '"id": "2014-08-02"', count=1)
        self.assertContains(response, response.context['files'])

    def test_complete(self):
        """
        Test complete page is working fine that
        save all positions into db and response correctly
        """
        self.move_csv_back_to_folder()

        date = '2014-08-01'
        response = self.client.get(reverse('pos_import_app_complete', args=(date,)))

        print 'date: %s' % date

        self.assertEqual(response.status_code, 200)

        positions = pm.Position.objects.all()
        self.assertEqual(positions.count(), 20)
        print 'positions saved: %d' % positions.count()

        instruments = pm.PositionInstrument.objects.all()
        self.assertEqual(instruments.count(), 20)
        print 'instruments saved: %d' % instruments.count()

        stocks = pm.PositionStock.objects.all()
        self.assertEqual(stocks.count(), 20)
        print 'stocks saved: %d' % stocks.count()

        options = pm.PositionOption.objects.all()
        self.assertEqual(options.count(), 41)
        print 'options saved: %d' % options.count()

        overall = pm.Overall.objects.all()
        self.assertEqual(overall.count(), 1)
        print 'overall saved: %d' % overall.count()

        # check saved file is in completed folder
        self.assertTrue(isfile(self.completed_path))
        print 'file now in: %s' % self.completed_path

        # move back into positions folder
        self.move_csv_back_to_folder()
        self.assertTrue(isfile(self.original_path))

        # view parameters test
        self.assertEqual(date, response.context['date'])
        self.assertIn(date, response.context['fname'])
        self.assertIn('saved', response.content)






