from django.test import TestCase
from spreads import StartProfit, MaxProfit, StartLoss, MaxLoss, BreakEven


class TestSpread(TestCase):
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

    def test_start_profit_start_loss(self):
        """
        """
        prices = [11.62, 33.8, 240, 24.96]
        conditions = ['>=', '<', '<=', '>']

        for price, condition in zip(prices, conditions):
            start_profit = StartProfit(price, condition)
            start_loss = StartLoss(price, condition)
            print '%s\n%s\n' % (start_profit, start_loss)

            self.assertEqual(start_profit.price, price)
            self.assertEqual(start_profit.condition, condition)

            self.assertEqual(start_loss.price, price)
            self.assertEqual(start_loss.condition, condition)

    def test_max_profit_max_loss(self):
        """
        Test max profit and max loss class
        """
        amount = [12.5, 55.34, 60.28, 27.54]
        limits = [False, True, True, False]
        prices = [11.62, 33.8, 240, 24.96]
        conditions = ['>=', '<', '<=', '>']

        for amount, limit, price, condition in zip(amount, limits, prices, conditions):
            max_profit = MaxProfit(amount, limit, price, condition)
            max_loss = MaxLoss(amount, limit, price, condition)
            print '%s\n%s\n' % (max_profit, max_loss)

            self.assertEqual(max_profit.limit, limit)
            self.assertEqual(max_profit.price, price)
            self.assertEqual(max_profit.condition, condition)

            self.assertEqual(max_loss.limit, limit)
            self.assertEqual(max_loss.price, price)
            self.assertEqual(max_loss.condition, condition)

            if max_profit.limit:
                self.assertEqual(max_profit.profit, amount)
                self.assertEqual(max_loss.loss, amount)
            else:
                self.assertEqual(max_profit.profit, float('inf'))
                self.assertEqual(max_loss.loss, float('inf'))

    def test_max_profit_max_loss_range(self):
        """
        Test max profit and max loss class with range (2 points, double)
        """
        profits_a = [12.5, 55.34, 60.28, 27.54]
        profits_b = [10.75, 50.9, 72.8, 33.69]
        
        limits_a = [False, True, True, False]
        limits_b = [False, True, False, True]
        
        prices_a = [11.62, 33.8, 240, 24.96]
        prices_b = [18.62, 41.8, 224.5, 30.8]
        
        conditions_a = ['>=', '<', '<=', '>']
        conditions_b = ['<=', '>', '>', '<=']
        
        range_a = zip(profits_a, limits_a, prices_a, conditions_a)
        range_b = zip(profits_b, limits_b, prices_b, conditions_b)

        for a, b in zip(range_a, range_b):
            max_profit_a = MaxProfit(*a)
            max_profit_b = MaxProfit(*b)

            max_loss_a = MaxLoss(*a)
            max_loss_b = MaxLoss(*b)

            print '%s && %s' % (max_profit_a, max_profit_b)
            print '%s && %s\n' % (max_loss_a, max_loss_b)

    def test_break_even_single_double(self):
        """
        Test break even class with single and range (double)
        """
        prices = [11.62, 33.8, 240, 24.96]
        conditions = ['==', '==', '<=', '=>']

        for price, condition in zip(prices, conditions):
            break_even = BreakEven(price, condition)

            print '%s' % break_even

            self.assertEqual(break_even.price, price)
            self.assertEqual(break_even.condition, condition)

        prices_a = [11.62, 33.8, 240, 24.96]
        prices_b = [18.62, 41.8, 224.5, 30.8]

        conditions_a = ['>=', '<', '<=', '>']
        conditions_b = ['<=', '>', '>', '<=']
        
        range_a = zip(prices_a, conditions_a)
        range_b = zip(prices_b, conditions_b)

        print ''
        
        for a, b in zip(range_a, range_b):
            break_even_a = BreakEven(*a)
            break_even_b = BreakEven(*b)

            print '%s && %s' % (break_even_a, break_even_b)
        

