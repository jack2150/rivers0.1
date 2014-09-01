from pms_app.classes.identify.tests import TestReadyUp
from pms_app import models

from pms_app.classes.identify.stock import StockIdentify
from pms_app.classes.spreads.stock import StockLong, StockShort


class TestStockIdentify(TestReadyUp):
    def test_get_cls(self):
        """
        Test get name using stock identify class
        """
        self.ready_all(key=1)

        for key, position in enumerate(models.Position.objects.all()):
            stock = models.PositionStock.objects.filter(position=position).first()
            """:type: PositionStock"""

            stock_identify = StockIdentify(stock)

            cls = stock_identify.get_cls()

            if stock.quantity > 0:
                self.assertEqual(cls, StockLong)
            else:
                self.assertEqual(cls, StockShort)

            print 'stock quantity: %d' % stock.quantity
            print 'class module: %s\n' % cls

            print cls(stock)

            for price in [60, 73.58, 94.93, 100]:
                print 'price: %.2f -> current status: %s' \
                      % (price, cls(stock).current_status(price))

            print '\n' + '-' * 100 + '\n'