from django.test import TestCase
import models


# Create your tests here.
class TestModels(TestCase):
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

    def test_pos_set_save_json(self):
        """
        Test set dict data into pos
        """
        items = {
            'symbol': 'SPX',
            'company': 'SPX',
            'date': '2014-08-01',
        }

        pos = models.Position(**items)
        pos.save()
        print 'Pos saved!\n'

        print 'pos id: %d' % pos.id
        print 'pos in json: %s' % pos

        self.assertTrue(pos.id)

        json = pos.__unicode__()
        self.assertEqual('{', json[0])
        self.assertEqual('}', json[-1])

        for key, item in items.items():
            self.assertIn(key, json)
            self.assertIn(item, json)

    def test_pos_instrument_set_save_json(self):
        """
        Test set dict data into pos instrument
        """
        items = {
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

        pos_ins = models.PositionInstrument()
        pos_ins.position = self.ready_pos()
        pos_ins.set_dict(items)
        pos_ins.save()
        print 'PosIns saved!\n'

        json = pos_ins.__unicode__()

        print 'pos id: %d' % pos_ins.id
        print 'pos in json:'
        print json[:102] + '\n' + json[102:]

        self.assertTrue(pos_ins.id)

        self.assertEqual('{', json[0])
        self.assertEqual('}', json[-1])

    def test_pos_stock_set_save_json(self):
        """
        Test set dict data into pos stock
        """
        items = {
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

        pos_stock = models.PositionStock()
        pos_stock.position = self.ready_pos()
        pos_stock.set_dict(items)
        pos_stock.save()
        print 'PosStock saved!\n'

        json = pos_stock.__unicode__()

        print 'pos id: %d' % pos_stock.id
        print 'pos in json:'
        print json[:102] + '\n' + json[102:]

        self.assertTrue(pos_stock.id)

        self.assertEqual('{', json[0])
        self.assertEqual('}', json[-1])

    def test_pos_options_set_save_json(self):
        """
        Test set dict data into pos options
        """
        items = [
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
             'quantity': -3.0, 'gamma': -6.74, 'trade_price': 0.25}]

        pos = self.ready_pos()

        for item in items:
            pos_options = models.PositionOption()
            pos_options.position = pos
            pos_options.set_dict(item)
            pos_options.save()

            print 'PosOptions saved!\n'

            json = pos_options.__unicode__()

            print 'pos id: %d' % pos_options.id
            print 'pos in json:'
            print json[:102] + '\n' + json[102:204] + '\n' + json[204:]

            self.assertTrue(pos_options.id)

            self.assertEqual('{', json[0])
            self.assertEqual('}', json[-1])

            print '\n' + '-' * 100 + '\n'

    def test_overall_set_save_json(self):
        """
        Test
        """
        date = '2014-08-01'

        items = {
            'available': 1873.49,
            'bp_adjustment': 0.0,
            'futures_bp': 1873.49,
            'pl_ytd': -5609.52,
            'cash_sweep': 3773.49
        }

        overall = models.Overall(**items)
        overall.date = date
        overall.save()
        print 'Overall saved!\n'

        json = overall.__unicode__()

        print 'overall id: %d' % overall.id
        print 'overall in json:'
        print json[:102] + '\n' + json[102:]
