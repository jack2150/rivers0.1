# perfect...
from django.test import TestCase
from pms_app import models
from django.db.models.query import QuerySet
from pprint import pprint
from pms_app.classes import OpenPosCSV
from rivers2.settings import FILES


class TestSetUp(TestCase):
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


class TestSetUpModel(TestSetUp):
    def ready_pos(self):
        """
        Ready up pos object and use as foreign key
        """
        items = {
            'symbol': 'SPX',
            'company': 'SPX',
            'date': '2014-08-01',
        }

        pos = models.Position(**items)
        pos.save()

        return pos


class TestReadyUp(TestCase):
    def setUp(self):
        """
        ready up all variables and test class
        """
        print '=' * 100
        print "<%s> currently run: %s" % (self.__class__.__name__, self._testMethodName)
        print '-' * 100 + '\n'

        self.identify = None

    def tearDown(self):
        """
        remove variables after test
        """
        print '\n' + '=' * 100 + '\n\n'

        del self.identify

    def ready_fname(self, date, path):
        """
        Insert positions and overall into db then start testing
        """
        positions, overall = OpenPosCSV(path).read()

        for position in positions:
            # save positions
            pos = models.Position(
                symbol=position['Symbol'],
                company=position['Company'],
                date=date
            )
            pos.save()

            # save instrument
            instrument = models.PositionInstrument()
            instrument.set_dict(position['Instrument'])
            instrument.position = pos
            instrument.save()

            # save stock
            stock = models.PositionStock()
            stock.set_dict(position['Stock'])
            stock.position = pos
            stock.save()

            # save options
            for pos_option in position['Options']:
                option = models.PositionOption()
                option.set_dict(pos_option)
                option.position = pos
                option.save()

        pos_overall = models.Overall(**overall)
        pos_overall.date = date
        pos_overall.save()

    def ready_all(self, key=None):
        """
        Ready specific files or all files for testing
        """
        test_fname = [
            '2014-03-07-closed.csv',
            '2014-03-10-stock.csv',
            '2014-03-11-hedge.csv',
            '2014-03-12-one-leg.csv',
            '2014-03-13-two-legs.csv',
            '2014-03-14-three-legs.csv',
            '2014-03-17-four-legs-part-1.csv'
        ]

        if key is not None:
            test_fname = [test_fname[key]]

        for fname in test_fname:
            date = fname[:10]
            path = FILES['tos_positions'] + 'tests/' + fname
            self.ready_fname(date=date, path=path)

        pos_count = models.Position.objects.count()
        overall_count = models.Overall.objects.count()

        print 'pos count: %d and overall count: %d\n' % (pos_count, overall_count)


class TestPosition(TestSetUp):
    def setUp(self):
        TestSetUp.setUp(self)

        self.items = {
            'symbol': 'SPX',
            'company': 'SPX',
            'date': '2014-08-01',
        }

        self.pos = models.Position(**self.items)

    def test_save(self):
        """
        Test set dict data into pos
        """
        self.pos.save()

        print 'Position saved!'
        print 'pos id: %d' % self.pos.id

        self.assertTrue(self.pos.id)

    def test_json(self):
        """
        Test output json format data
        """
        print 'pos in json: %s' % self.pos

        json = self.pos.__unicode__()
        self.assertEqual('{', json[0])
        self.assertEqual('}', json[-1])

        for key, item in self.items.items():
            self.assertIn(key, json)
            self.assertIn(item, json)


class TestPositionInstrument(TestSetUpModel):
    def setUp(self):
        TestSetUpModel.setUp(self)

        self.items = {
            'name': 'SPX',
            'mark_change': 0.0,
            'pl_open': -50.0,
            'days': 0.0,
            'mark': 0.0,
            'vega': 17.48,
            'pl_day': 92.5,
            'delta': 3.93,
            'bp_effect': 0.0,
            'theta': -11.96,
            'pct_change': -2.0,
            'quantity': 0.0,
            'gamma': 0.15,
            'trade_price': 0.0
        }

        self.pos_ins = models.PositionInstrument()
        self.pos_ins.position = self.ready_pos()
        self.pos_ins.set_dict(self.items)

    def test_save(self):
        """
        Test set dict data into pos instrument
        """
        self.pos_ins.save()
        print 'PositionInstrument saved!\n'
        print 'pos id: %d' % self.pos_ins.id
        self.assertTrue(self.pos_ins.id)

    def test_json(self):
        """
        Test output json data format
        """
        json = self.pos_ins.__unicode__()

        print 'pos in json:'
        print json[:80] + '...'

        self.assertEqual('{', json[0])
        self.assertEqual('}', json[-1])


class TestPositionStock(TestSetUpModel):
    def setUp(self):
        TestSetUpModel.setUp(self)

        self.items = {
            'mark_change': -5.87,
            'name': '3 D SYSTEMS CORP COM',
            'pl_open': 0.0,
            'days': 0.0,
            'mark': 50.2,
            'vega': 0.0,
            'pl_day': 0.0,
            'delta': 0.0,
            'bp_effect': 0.0,
            'theta': 0.0,
            'pct_change': 0.0,
            'quantity': 0.0,
            'gamma': 0.0,
            'trade_price': 0.0
        }

        self.pos_stock = models.PositionStock()
        self.pos_stock.position = self.ready_pos()
        self.pos_stock.set_dict(self.items)

    def test_save(self):
        """
        Test save dict data into pos stock
        """
        self.pos_stock.save()
        print 'PositionStock saved!\n'
        print 'pos id: %d' % self.pos_stock.id
        self.assertTrue(self.pos_stock.id)

    def test_json(self):
        json = self.pos_stock.__unicode__()

        print 'pos in json:'
        print json[:102] + '\n' + json[102:]

        self.assertEqual('{', json[0])
        self.assertEqual('}', json[-1])


class TestPositionOption(TestSetUpModel):
    def setUp(self):
        TestSetUpModel.setUp(self)

        self.items = [
            {'name': {'ex_month': 'AUG', 'right': '100', 'strike_price': '58.5',
                      'contract': 'PUT', 'ex_year': '14', 'special': 'Normal'},
             'mark_change': -0.63, 'pl_open': -219.0, 'days': 15.0,
             'mark': 0.38, 'vega': 18.07, 'pl_day': -189.0, 'delta': 52.79,
             'bp_effect': 0.0, 'theta': -9.71, 'pct_change': 0.0,
             'quantity': 3.0, 'gamma': 18.98, 'trade_price': 1.11},
            {'name': {'ex_month': 'AUG', 'right': '100', 'strike_price': '72.5',
                      'contract': 'CALL', 'ex_year': '14', 'special': 'Normal'},
             'mark_change': -0.14, 'pl_open': 57.0, 'days': 15.0,
             'mark': 0.06, 'vega': -6.02, 'pl_day': 42.0, 'delta': -11.92,
             'bp_effect': 0.0, 'theta': 3.11, 'pct_change': 0.0,
             'quantity': -3.0, 'gamma': -6.74, 'trade_price': 0.25}
        ]

    def test_save(self):
        """
        Test save dict data into pos options
        """
        pos = self.ready_pos()

        for item in self.items:
            pos_option = models.PositionOption()
            pos_option.position = pos
            pos_option.set_dict(item)
            pos_option.save()

            print 'PositionOption saved!'
            print 'pos id: %d\n' % pos_option.id

            self.assertTrue(pos_option.id)

    def test_json(self):
        """
        Test output json data format
        """
        pos = self.ready_pos()

        for item in self.items:
            pos_option = models.PositionOption()
            pos_option.position = pos
            pos_option.set_dict(item)
            json = pos_option.__unicode__()

            print 'pos in json:'
            print json[:80] + '...'

            self.assertEqual('{', json[0])
            self.assertEqual('}', json[-1])

            print '\n' + '-' * 100 + '\n'


class TestOverall(TestSetUp):
    def setUp(self):
        TestSetUp.setUp(self)

        self.date = '2014-08-01'

        self.items = {
            'available': 1873.49,
            'bp_adjustment': 0.0,
            'futures_bp': 1873.49,
            'pl_ytd': -5609.52,
            'cash_sweep': 3773.49
        }

    def test_save(self):
        """
        Test sample data save into db
        """
        print 'sample data:'
        pprint(self.items)

        overall = models.Overall(**self.items)
        overall.date = self.date
        overall.save()
        print '\n' + 'Overall saved!\n'

        self.assertTrue(overall.id)
        print 'overall id: %d' % overall.id

        print 'overall data:'
        print overall.__unicode__()[:80] + '...'

    def test_json(self):
        """
        Test json output
        """
        overall = models.Overall(**self.items)
        overall.date = self.date
        overall.save()

        json = eval(overall.__unicode__())

        print 'json output:'
        pprint(json)


class TestPositionSet(TestReadyUp):
    def setUp(self):
        TestReadyUp.setUp(self)

        self.ready_all(key=2)

        position = models.Position.objects.all().first()

        self.pos_set = models.PositionSet(position)

    def test_property(self):
        """
        Test property inside position set
        """

        print 'Position: %s' % self.pos_set.position
        print 'Instrument: %s' % self.pos_set.instrument
        print 'Stock: %s' % self.pos_set.stock
        print 'Options: %s' % self.pos_set.options

        self.assertEqual(type(self.pos_set.position), models.Position)
        self.assertEqual(type(self.pos_set.instrument), models.PositionInstrument)
        self.assertEqual(type(self.pos_set.stock), models.PositionStock)
        self.assertEqual(type(self.pos_set.options), QuerySet)
        self.assertEqual(type(self.pos_set.options.first()), models.PositionOption)

        self.assertTrue(self.pos_set.position.id)
        self.assertTrue(self.pos_set.instrument.id)
        self.assertTrue(self.pos_set.stock.id)
        self.assertTrue(self.pos_set.options.first().id)
        self.assertEqual(self.pos_set.options.count(), 1)

    def test_get_option(self):
        """
        Test option property that get first option
        """
        print 'first option: %s' % self.pos_set.option

        self.assertEqual(type(self.pos_set.option), models.PositionOption)
        self.assertEqual(self.pos_set.option, self.pos_set.options.first())
