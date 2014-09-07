from pms_app.classes.identify.tests import TestReadyUp
from pms_app.classes import spreads
from pms_app import models

import leg_one


class TestLegOneSpreads(TestReadyUp):
    def test_leg_one_context(self):
        """
        Test one leg context and all methods working
        """
        one_leg = leg_one.LegOne()

        print one_leg

        self.assertFalse(one_leg.name)
        self.assertEqual(type(one_leg.max_profit), spreads.MaxProfit)
        self.assertEqual(type(one_leg.start_profit), spreads.StartProfit)
        self.assertEqual(type(one_leg.max_loss), spreads.MaxLoss)
        self.assertEqual(type(one_leg.start_loss), spreads.StartLoss)
        self.assertEqual(type(one_leg.break_even), spreads.BreakEven)

    def test_long_call(self):
        """
        Test long call and calculation inside correct
        """
        self.ready_all(key=3)

        for position in models.Position.objects.all():
            option = models.PositionOption.objects.filter(position=position).first()
            """:type: PositionOption"""

            if option.contract == 'CALL' and option.quantity > 0:
                print option.__unicode__() + '\n'

                long_call = leg_one.CallLong(option)

                print long_call

                self.assertEqual(long_call.name, 'Long Call')
                self.assertEquals(
                    long_call.break_even.price,
                    long_call.start_profit.price,
                    long_call.start_loss.price
                )
                self.assertEqual(long_call.start_profit.condition, '>')
                self.assertEqual(long_call.start_loss.condition, '<')
                self.assertEqual(long_call.break_even.condition, '==')

                self.assertFalse(long_call.max_profit.limit)
                self.assertEqual(long_call.max_profit.condition, '==')
                self.assertEqual(long_call.max_profit.profit, float('inf'))
                self.assertEqual(long_call.max_profit.price, float('inf'))

                self.assertTrue(long_call.max_loss.limit)
                self.assertEqual(long_call.max_loss.condition, '<=')
                self.assertEqual(long_call.max_loss.price, option.strike_price)
                self.assertEqual(long_call.max_loss.loss, float(option.trade_price))

                for price in [99.86, 120, 90, 99.5, 100]:
                    print 'price: %8.2f, result: %s' % (price, long_call.current_status(price))

                print ''

    def test_naked_call(self):
        """
        Test naked call and calculation inside correct
        """
        self.ready_all(key=3)

        for position in models.Position.objects.all():
            option = models.PositionOption.objects.filter(position=position).first()
            """:type: PositionOption"""

            if option.contract == 'CALL' and option.quantity < 0:
                print option.__unicode__() + '\n'

                long_call = leg_one.CallNaked(option)

                print long_call

                self.assertEqual(long_call.name, 'Naked Call')
                self.assertEquals(
                    long_call.break_even.price,
                    long_call.start_profit.price,
                    long_call.start_loss.price
                )
                self.assertEqual(long_call.start_profit.condition, '<')
                self.assertEqual(long_call.start_loss.condition, '>')
                self.assertEqual(long_call.break_even.condition, '==')

                self.assertTrue(long_call.max_profit.limit)
                self.assertEqual(long_call.max_profit.condition, '<=')
                self.assertEqual(long_call.max_profit.profit, float(option.trade_price))
                self.assertEqual(long_call.max_profit.price, float(option.strike_price))

                self.assertFalse(long_call.max_loss.limit)
                self.assertEqual(long_call.max_loss.condition, '==')
                self.assertEqual(long_call.max_loss.price, float('inf'))
                self.assertEqual(long_call.max_loss.loss, float('inf'))

                for price in [76.87, 76.5, 77, 75, 80]:
                    print 'price: %8.2f, result: %s' % (price, long_call.current_status(price))

                print ''

    def test_long_put(self):
        """
        Test long put and calculation inside correct
        """
        self.ready_all(key=3)

        for position in models.Position.objects.all():
            option = models.PositionOption.objects.filter(position=position).first()
            """:type: PositionOption"""

            if option.contract == 'PUT' and option.quantity > 0:
                print option.__unicode__() + '\n'

                long_call = leg_one.PutLong(option)

                print long_call

                self.assertEqual(long_call.name, 'Long Put')
                self.assertEquals(
                    long_call.break_even.price,
                    long_call.start_profit.price,
                    long_call.start_loss.price
                )
                self.assertEqual(long_call.start_profit.condition, '<')
                self.assertEqual(long_call.start_loss.condition, '>')
                self.assertEqual(long_call.break_even.condition, '==')

                self.assertTrue(long_call.max_profit.limit)
                self.assertEqual(long_call.max_profit.condition, '==')
                self.assertEqual(long_call.max_profit.profit,
                                 float(option.strike_price - option.trade_price))
                self.assertEqual(long_call.max_profit.price, 0.0)

                self.assertTrue(long_call.max_loss.limit)
                self.assertEqual(long_call.max_loss.condition, '>=')
                self.assertEqual(long_call.max_loss.price, float(option.strike_price))
                self.assertEqual(long_call.max_loss.loss, float(option.trade_price))

                for price in [182.27, 183, 181, 175, 190]:
                    print 'price: %8.2f, result: %s' % (price, long_call.current_status(price))

                print ''

    def test_naked_put(self):
        """
        Test long put and calculation inside correct
        """
        self.ready_all(key=3)

        for position in models.Position.objects.all():
            option = models.PositionOption.objects.filter(position=position).first()
            """:type: PositionOption"""

            if option.contract == 'PUT' and option.quantity < 0:
                print option.__unicode__() + '\n'

                long_call = leg_one.PutNaked(option)

                print long_call

                self.assertEqual(long_call.name, 'Naked Put')
                self.assertEquals(
                    long_call.break_even.price,
                    long_call.start_profit.price,
                    long_call.start_loss.price
                )
                self.assertEqual(long_call.start_profit.condition, '>')
                self.assertEqual(long_call.start_loss.condition, '<')
                self.assertEqual(long_call.break_even.condition, '==')

                self.assertTrue(long_call.max_profit.limit)
                self.assertEqual(long_call.max_profit.condition, '>=')
                self.assertEqual(long_call.max_profit.profit, float(option.trade_price))
                self.assertEqual(long_call.max_profit.price, float(option.strike_price))

                self.assertTrue(long_call.max_loss.limit)
                self.assertEqual(long_call.max_loss.condition, '<=')
                self.assertEqual(long_call.max_loss.price, 0.0)
                self.assertEqual(long_call.max_loss.loss,
                                 float(option.strike_price - option.trade_price))

                for price in [63.09, 64, 62, 60, 65]:
                    print 'price: %8.2f, result: %s' % (price, long_call.current_status(price))

                print ''