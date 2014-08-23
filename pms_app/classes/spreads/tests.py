from django.test import TestCase
from rivers2.settings import FILES
from pms_app.classes.open_pos_csv import OpenPosCSV
from pms_app import models

from spreads import Spreads


class TestSpreads(TestCase):
    def setUp(self):
        """
        ready up all variables and test class
        """
        print '=' * 100
        print "<%s> currently run: %s" % (self.__class__.__name__, self._testMethodName)
        print '-' * 100 + '\n'

        self.spreads = None

    def tearDown(self):
        """
        remove variables after test
        """
        print '\n' + '=' * 100 + '\n\n'

        del self.spreads

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
            '2014-03-10-stock_only.csv',
            '2014-03-11-stock_options_combine.csv',
            '2014-03-12-one-leg-option.csv',
            '2014-03-13-two-legs-options.csv'
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

    def test_is_stock(self):
        """
        Test identity with stock only positions
        """
        self.ready_all()

        for key, position in enumerate(models.Position.objects.all()):
            self.spreads = Spreads(position)

            print 'no: %d, symbol: %s, stock qty: %d, options len: %d, result: %s' \
                  % (key, position.symbol, self.spreads.stock.quantity,
                     len(self.spreads.options), self.spreads.is_two_leg_options())

            if key < 2:
                self.assertTrue(self.spreads.is_stock())
            else:
                self.assertFalse(self.spreads.is_stock())

    def test_is_hedge(self):
        """
        Test identity with hedge (stock + options) positions
        """
        self.ready_all()

        for key, position in enumerate(models.Position.objects.all()):
            self.spreads = Spreads(position)

            print 'symbol: %s, stock qty: %d, options len: %d, result: %s' \
                  % (position.symbol, self.spreads.stock.quantity,
                     len(self.spreads.options), self.spreads.is_hedge())

            if 1 < key < 13:
                self.assertTrue(self.spreads.is_hedge())
            else:
                self.assertFalse(self.spreads.is_hedge())

    def test_is_one_leg_option(self):
        """
        Test identity with one leg option positions
        """
        self.ready_all()

        for key, position in enumerate(models.Position.objects.all()):
            self.spreads = Spreads(position)

            print 'no: %d, symbol: %s, stock qty: %d, options len: %d, result: %s' \
                  % (key, position.symbol, self.spreads.stock.quantity,
                     len(self.spreads.options), self.spreads.is_two_leg_options())

            if 12 < key < 17:
                self.assertTrue(self.spreads.is_one_leg_option())
            else:
                self.assertFalse(self.spreads.is_one_leg_option())

    def test_is_two_leg_options(self):
        """
        Test identity with two leg options positions
        """
        self.ready_all()

        for key, position in enumerate(models.Position.objects.all()):
            self.spreads = Spreads(position)

            print 'no: %d, symbol: %s, stock qty: %d, options len: %d, result: %s' \
                  % (key, position.symbol, self.spreads.stock.quantity,
                     len(self.spreads.options), self.spreads.is_two_leg_options())

            if 16 < key < 31:
                self.assertTrue(self.spreads.is_two_leg_options())
            else:
                self.assertFalse(self.spreads.is_two_leg_options())


    #  todo: 4 legs...







