from spreads.identify.test_identify import TestReadyUp
import spreads
from pms_app import models

import hedge_only


class TestHedgeContext(TestReadyUp):
    def test_hedge_context(self):
        """
        Test hedge context in functions is working
        """
        hedge_pos = hedge_only.HedgeContext()

        hedge_pos.name = 'Test'

        print hedge_pos

        self.assertEqual(type(hedge_pos.max_profit), spreads.MaxProfit)
        self.assertEqual(type(hedge_pos.start_profit), spreads.StartProfit)
        self.assertEqual(type(hedge_pos.max_loss), spreads.MaxLoss)
        self.assertEqual(type(hedge_pos.start_loss), spreads.StartLoss)
        self.assertEqual(type(hedge_pos.break_even), spreads.BreakEven)

    def test_covered_call(self):
        """
        Test covered call and calculation inside correct
        """
        self.ready_all(key=2)

        for key, position in enumerate(models.Position.objects.all()):
            stock = models.PositionStock.objects.filter(position=position).first()
            """:type: PositionStock"""

            option = models.PositionOption.objects.filter(position=position).first()
            """:type: PositionOption"""

            if stock.quantity > 0 and option.contract == 'CALL' and option.quantity < 0:
                print stock
                print option.__unicode__() + '\n'

                cc = hedge_only.CoveredCall(stock, option)

                print cc

                self.assertEqual(cc.name, 'Covered Call')
                self.assertEquals(
                    cc.break_even.price,
                    cc.start_profit.price,
                    cc.start_loss.price
                )
                self.assertEqual(cc.start_profit.condition, '>')
                self.assertEqual(cc.start_loss.condition, '<')
                self.assertEqual(cc.break_even.condition, '==')

                self.assertTrue(cc.max_profit.limit)
                self.assertFalse(cc.max_loss.limit)
                self.assertEqual(cc.max_loss.condition, '==')

                self.assertEqual(cc.max_loss.price, 0.0)
                self.assertEqual(cc.max_profit.condition, '>=')

                for price in [71.11, 73.52, 70, 75.5, 0]:
                    print 'price: %8.2f, result: %s' % (price, cc.current_status(price))

                print ''

    def test_protective_call(self):
        """
        Test protective call and all calculation is correct
        """
        self.ready_all(key=2)

        for key, position in enumerate(models.Position.objects.all()):
            stock = models.PositionStock.objects.filter(position=position).first()
            """:type: PositionStock"""

            option = models.PositionOption.objects.filter(position=position).first()
            """:type: PositionOption"""

            if stock.quantity < 0 and option.contract == 'CALL' and option.quantity > 0:
                print stock
                print option.__unicode__() + '\n'

                pc = hedge_only.ProtectiveCall(stock, option)

                print pc

                self.assertEqual(pc.name, 'Protective Call')
                self.assertEquals(
                    pc.break_even.price,
                    pc.start_profit.price,
                    pc.start_loss.price
                )
                self.assertEqual(pc.start_profit.condition, '<')
                self.assertEqual(pc.start_loss.condition, '>')
                self.assertEqual(pc.break_even.condition, '==')

                self.assertTrue(pc.max_loss.limit)
                self.assertEqual(pc.max_loss.condition, '>=')

                self.assertFalse(pc.max_profit.limit)
                self.assertEqual(pc.max_profit.price, 0.0)
                self.assertEqual(pc.max_profit.condition, '==')

                for price in [14.65, 13, 14.8, 15.8, 0]:
                    print 'price: %8.2f, result: %s' % (price, pc.current_status(price))

                print ''

    def test_covered_put(self):
        """
        Test covered put and all calculation is correct
        """
        self.ready_all(key=2)

        for key, position in enumerate(models.Position.objects.all()):
            stock = models.PositionStock.objects.filter(position=position).first()
            """:type: PositionStock"""

            option = models.PositionOption.objects.filter(position=position).first()
            """:type: PositionOption"""

            if stock.quantity < 0 and option.contract == 'PUT' and option.quantity < 0:
                print stock
                print option.__unicode__() + '\n'

                cp = hedge_only.CoveredPut(stock, option)

                print cp

                self.assertEqual(cp.name, 'Covered Put')
                self.assertEquals(
                    cp.break_even.price,
                    cp.start_profit.price,
                    cp.start_loss.price
                )
                self.assertEqual(cp.start_profit.condition, '<')
                self.assertEqual(cp.start_loss.condition, '>')
                self.assertEqual(cp.break_even.condition, '==')

                self.assertTrue(cp.max_profit.limit)
                self.assertFalse(cp.max_loss.limit)
                self.assertEqual(cp.max_loss.condition, '==')

                self.assertEqual(cp.max_loss.price, float('inf'))
                self.assertEqual(cp.max_profit.condition, '<=')

                for price in [49.43, 49, 49.75, 100, 0]:
                    print 'price: %8s, result: %s' % (price, cp.current_status(price))

                print ''

    def test_protective_put(self):
        """
        Test protective put and all calculation is correct
        """
        self.ready_all(key=2)

        for key, position in enumerate(models.Position.objects.all()):
            stock = models.PositionStock.objects.filter(position=position).first()
            """:type: PositionStock"""

            option = models.PositionOption.objects.filter(position=position).first()
            """:type: PositionOption"""

            if stock.quantity > 0 and option.contract == 'PUT' and option.quantity > 0:
                print stock
                print option.__unicode__() + '\n'

                pp = hedge_only.ProtectivePut(stock, option)

                print pp

                self.assertEqual(pp.name, 'Protective Put')
                self.assertEquals(
                    pp.break_even.price,
                    pp.start_profit.price,
                    pp.start_loss.price
                )
                self.assertEqual(pp.start_profit.condition, '>')
                self.assertEqual(pp.start_loss.condition, '<')
                self.assertEqual(pp.break_even.condition, '==')

                self.assertTrue(pp.max_loss.limit)
                self.assertFalse(pp.max_profit.limit)
                self.assertEqual(pp.max_loss.condition, '<=')

                self.assertEqual(pp.max_profit.price, float('inf'))
                self.assertEqual(pp.max_profit.condition, '==')

                for price in [44.29, 45, 44.1, 42.5, 100]:
                    print 'price: %8s, result: %s' % (price, pp.current_status(price))

                print ''
