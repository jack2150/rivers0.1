from pms_app.classes.identify.tests import TestReadyUp
from pms_app.classes import spreads
from pms_app import models

import leg_one


class TestLegOneSpreads(TestReadyUp):
    def test_leg_one_context(self):
        """
        Test one leg context and all methods working
        """
        one_leg = leg_one.LegOneContext()

        print one_leg

        self.assertEqual(one_leg.context, 'leg_one')
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
                self.assertEqual(long_call.max_profit.amount, float('inf'))
                self.assertEqual(long_call.max_profit.price, float('inf'))

                self.assertTrue(long_call.max_loss.limit)
                self.assertEqual(long_call.max_loss.condition, '<=')
                self.assertEqual(long_call.max_loss.price, option.strike_price)
                self.assertEqual(long_call.max_loss.amount, float(option.trade_price * option.right))

                for price in [99.86, 120, 90, 99.5, 100]:
                    status = long_call.current_status(price)
                    print 'price: %8.2f, result: %s' % (price, status)
                    self.assertIn(status, ['even', 'profit', 'loss', 'max_profit', 'max_loss'])

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

                naked_call = leg_one.CallNaked(option)

                print naked_call

                self.assertEqual(naked_call.name, 'Naked Call')
                self.assertEquals(
                    naked_call.break_even.price,
                    naked_call.start_profit.price,
                    naked_call.start_loss.price
                )
                self.assertEqual(naked_call.start_profit.condition, '<')
                self.assertEqual(naked_call.start_loss.condition, '>')
                self.assertEqual(naked_call.break_even.condition, '==')

                self.assertTrue(naked_call.max_profit.limit)
                self.assertEqual(naked_call.max_profit.condition, '<=')
                self.assertEqual(naked_call.max_profit.amount,
                                 float(option.trade_price * abs(option.quantity) * option.right))
                self.assertEqual(naked_call.max_profit.price, float(option.strike_price))

                self.assertFalse(naked_call.max_loss.limit)
                self.assertEqual(naked_call.max_loss.condition, '==')
                self.assertEqual(naked_call.max_loss.price, float('inf'))
                self.assertEqual(naked_call.max_loss.amount, float('inf'))

                for price in [76.87, 76.5, 77, 75, 80]:
                    status = naked_call.current_status(price)
                    print 'price: %8.2f, result: %s' % (price, status)
                    self.assertIn(status, ['even', 'profit', 'loss', 'max_profit', 'max_loss'])

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

                long_put = leg_one.PutLong(option)

                print long_put

                self.assertEqual(long_put.name, 'Long Put')
                self.assertEquals(
                    long_put.break_even.price,
                    long_put.start_profit.price,
                    long_put.start_loss.price
                )
                self.assertEqual(long_put.start_profit.condition, '<')
                self.assertEqual(long_put.start_loss.condition, '>')
                self.assertEqual(long_put.break_even.condition, '==')

                self.assertTrue(long_put.max_profit.limit)
                self.assertEqual(long_put.max_profit.condition, '==')
                self.assertEqual(long_put.max_profit.amount,
                                 float((option.strike_price - option.trade_price) * option.right))
                self.assertEqual(long_put.max_profit.price, 0.0)

                self.assertTrue(long_put.max_loss.limit)
                self.assertEqual(long_put.max_loss.condition, '>=')
                self.assertEqual(long_put.max_loss.price, float(option.strike_price))
                self.assertEqual(long_put.max_loss.amount,
                                 float(option.trade_price * option.quantity * option.right))

                for price in [182.27, 183, 181, 175, 190]:
                    status = long_put.current_status(price)
                    print 'price: %8.2f, result: %s' % (price, status)
                    self.assertIn(status, ['even', 'profit', 'loss', 'max_profit', 'max_loss'])

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

                naked_put = leg_one.PutNaked(option)

                print naked_put

                self.assertEqual(naked_put.name, 'Naked Put')
                self.assertEquals(
                    naked_put.break_even.price,
                    naked_put.start_profit.price,
                    naked_put.start_loss.price
                )
                self.assertEqual(naked_put.start_profit.condition, '>')
                self.assertEqual(naked_put.start_loss.condition, '<')
                self.assertEqual(naked_put.break_even.condition, '==')

                self.assertTrue(naked_put.max_profit.limit)
                self.assertEqual(naked_put.max_profit.condition, '>=')
                self.assertEqual(naked_put.max_profit.amount,
                                 float(option.trade_price * abs(option.quantity) * option.right))
                self.assertEqual(naked_put.max_profit.price, float(option.strike_price))

                self.assertTrue(naked_put.max_loss.limit)
                self.assertEqual(naked_put.max_loss.condition, '<=')
                self.assertEqual(naked_put.max_loss.price, 0.0)
                self.assertEqual(naked_put.max_loss.amount,
                                 float((option.strike_price - option.trade_price) * option.right))

                for price in [63.09, 64, 62, 60, 65]:
                    status = naked_put.current_status(price)
                    print 'price: %8.2f, result: %s' % (price, status)
                    self.assertIn(status, ['even', 'profit', 'loss', 'max_profit', 'max_loss'])

                print ''

    def test_json(self):
        """
        Test spread data into json format
        """
        self.ready_all(key=2)

        for position in models.Position.objects.all():
            option = models.PositionOption.objects.filter(position=position).first()
            """:type: PositionOption"""

            if option.contract == 'CALL' and option.quantity > 0:
                spread = leg_one.CallLong(option)
            elif option.contract == 'CALL' and option.quantity < 0:
                spread = leg_one.CallNaked(option)
            elif option.contract == 'PUT' and option.quantity > 0:
                spread = leg_one.PutLong(option)
            elif option.contract == 'PUT' and option.quantity < 0:
                spread = leg_one.PutNaked(option)
            else:
                spread = None

            if spread:
                json = spread.json()

                print 'json view:'
                for i in range(0, int(round(len(json) / 100.0)) * 100, 100):
                    print json[i: i + 100]
                print ''

                var = eval(json)
                """ :type: dict """

                self.assertEqual(type(var), dict)
                self.assertEqual(len(var), 7)

                print 'dict view:'
                for v in var.items():
                    print v
                print '-' * 100 + '\n'