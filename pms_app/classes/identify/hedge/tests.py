import random
from pms_app.classes.identify.tests import TestReadyUp
from pms_app import models

from pms_app.classes.identify.hedge import HedgeIdentify
from pms_app.classes.spreads.hedge import hedge


class TestHedgeIdentify(TestReadyUp):
    def test_all_condition_methods(self):
        """
        Test all conditions method with related field
        """
        self.ready_all(key=2)

        for position in models.Position.objects.all():
            stock = models.PositionStock.objects.filter(position=position).first()
            """:type: PositionStock"""

            option = models.PositionOption.objects.filter(position=position).exclude(quantity=0).first()
            """:type: PositionOption"""

            hedge_identify = HedgeIdentify(stock, option)

            # long stock, short stock
            long_result = hedge_identify.long_stock()
            short_result = hedge_identify.short_stock()
            print 'stock quantity: %s, long stock result: %s' \
                  % (stock.quantity, long_result)
            print 'stock quantity: %s, short stock result: %s' \
                  % (stock.quantity, short_result)

            if stock.quantity > 0:
                self.assertTrue(long_result)
                self.assertFalse(short_result)
            else:
                self.assertFalse(long_result)
                self.assertTrue(short_result)

            # call and put
            buy_call_result = hedge_identify.buy_call_option()
            sell_call_result = hedge_identify.sell_call_option()
            buy_put_result = hedge_identify.buy_put_option()
            sell_put_result = hedge_identify.sell_put_option()
            print 'option qty: %s, option: %s' % (option.quantity, option.contract)
            print 'buy call result: %s' % buy_call_result
            print 'sell call result: %s' % sell_call_result
            print 'buy put result: %s' % buy_put_result
            print 'sell put result: %s\n' % sell_put_result

            if option.contract == 'CALL':
                if option.quantity > 0:
                    self.assertTrue(buy_call_result)
                    self.assertFalse(sell_call_result)
                else:
                    self.assertFalse(buy_call_result)
                    self.assertTrue(sell_call_result)
            else:
                if option.quantity > 0:
                    self.assertTrue(buy_put_result)
                    self.assertFalse(sell_put_result)
                else:
                    self.assertFalse(buy_put_result)
                    self.assertTrue(sell_put_result)

    def test_get_cls(self):
        """
        Test get name using stock identify class
        """
        self.ready_all(key=2)

        for position in models.Position.objects.all():
            stock = models.PositionStock.objects.filter(position=position).first()
            """:type: PositionStock"""

            option = models.PositionOption.objects.filter(position=position).first()
            """:type: PositionOption"""

            hedge_identify = HedgeIdentify(stock, option)

            cls = hedge_identify.get_cls()

            self.assertIn(
                cls,
                [hedge.CoveredCall, hedge.ProtectiveCall,
                 hedge.CoveredPut, hedge.ProtectivePut,
                 None]
            )

            if cls:
                print 'current class: %s' % cls.__name__

                inst = cls(stock, option)

                print inst

                for x in random.sample(xrange(-10, 10), 5):
                    price = inst.break_even.price + x
                    print 'price: %s, current status: %s' \
                          % (price, inst.current_status(price))

                print ''
