from django.test import TestCase

from rivers2.settings import FILES
from pms_app.classes.open_pos_csv import OpenPosCSV
from pms_app import models
from identify import Identify


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


class TestIdentify(TestReadyUp):
    def test_is_closed(self):
        """
        Test identity with closed only positions
        """
        self.ready_all()

        for key, position in enumerate(models.Position.objects.all()):
            self.identify = Identify(position)

            result = self.identify.is_closed()
            print 'no: %d, symbol: %s, stock qty: %d, options len: %d, result: %s' \
                  % (key, position.symbol, self.identify.stock.quantity,
                     len(self.identify.options), result)

            if key < 3:
                self.assertTrue(result)
            else:
                self.assertFalse(result)

    def test_is_stock(self):
        """
        Test identity with stock only positions
        """
        self.ready_all()

        for key, position in enumerate(models.Position.objects.all()):
            self.identify = Identify(position)

            result = self.identify.is_stock()
            print 'no: %d, symbol: %s, stock qty: %d, options len: %d, result: %s' \
                  % (key, position.symbol, self.identify.stock.quantity,
                     len(self.identify.options), result)

            if 2 < key < 5:
                self.assertTrue(result)
            else:
                self.assertFalse(result)

    def test_is_hedge(self):
        """
        Test identity with hedge (stock + options) positions
        """
        self.ready_all()

        for key, position in enumerate(models.Position.objects.all()):
            self.identify = Identify(position)

            result = self.identify.is_hedge()
            print 'no: %d, symbol: %s, stock qty: %d, options len: %d, result: %s' \
                  % (key, position.symbol, self.identify.stock.quantity,
                     len(self.identify.options), result)

            if 4 < key < 16:
                self.assertTrue(result)
            else:
                self.assertFalse(result)

    def test_is_one_leg_option(self):
        """
        Test identity with one leg option positions
        """
        self.ready_all()

        for key, position in enumerate(models.Position.objects.all()):
            self.identify = Identify(position)

            result = self.identify.is_one_leg_option()
            print 'no: %d, symbol: %s, stock qty: %d, options len: %d, result: %s' \
                  % (key, position.symbol, self.identify.stock.quantity,
                     len(self.identify.options), result)

            if 15 < key < 20:
                self.assertTrue(result)
            else:
                self.assertFalse(result)

    def test_is_two_legs_options(self):
        """
        Test identity with two leg options positions
        """
        self.ready_all()

        for key, position in enumerate(models.Position.objects.all()):
            self.identify = Identify(position)

            result = self.identify.is_two_legs_options()
            print 'no: %d, symbol: %s, stock qty: %d, options len: %d, result: %s' \
                  % (key, position.symbol, self.identify.stock.quantity,
                     len(self.identify.options), result)

            if 19 < key < 30:
                self.assertTrue(result)
            else:
                self.assertFalse(result)

    def test_is_three_legs_options(self):
        """
        Test identity with three leg options positions
        """
        self.ready_all()

        for key, position in enumerate(models.Position.objects.all()):
            self.identify = Identify(position)

            result = self.identify.is_three_legs_options()
            print 'no: %d, symbol: %s, stock qty: %d, options len: %d, result: %s' \
                  % (key, position.symbol, self.identify.stock.quantity,
                     len(self.identify.options), result)

            if 29 < key < 50:
                self.assertTrue(result)
            else:
                self.assertFalse(result)

    def test_is_four_legs_options(self):
        """
        Test identity with four leg options positions
        """
        self.ready_all()

        for key, position in enumerate(models.Position.objects.all()):
            self.identify = Identify(position)

            result = self.identify.is_four_legs_options()
            print 'no: %d, symbol: %s, stock qty: %d, options len: %d, result: %s' \
                  % (key, position.symbol, self.identify.stock.quantity,
                     len(self.identify.options), result)

            if 49 < key < 58:
                self.assertTrue(result)
            else:
                self.assertFalse(result)

    def test_identify(self):
        """
        """
        self.ready_all()

        for key, position in enumerate(models.Position.objects.all()):
            self.identify = Identify(position)
            self.identify.identify()

            print self.identify.name

    def test_legs_calculation(self):
        """
        4 legs pos
        """
        contracts = ['CALL', 'PUT']
        purchases = ['BUY', 'SELL']

        leg = ['%s %s' % (p, c) for p in purchases for c in contracts]

        spreads = list()
        count = 1
        for l1 in leg:
            for l2 in leg:
                for l3 in leg:
                    for l4 in leg:
                        l = [l1, l2, l3, l4]
                        l.sort()
                        spreads.append(tuple(l))
                        print count, l1, l2, l3, l4
                        count += 1

        set_all = set(spreads)
        for k, s in enumerate(set_all, start=1):
            print k, s

        # until 8th...