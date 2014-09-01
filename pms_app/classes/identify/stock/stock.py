from pms_app.classes.spreads.stock import StockLong, StockShort


class StockIdentify(object):
    def __init__(self, stock):
        self.stock = stock
        """:type: PositionStock"""

        self.cls_name = None

    def get_cls(self):
        """
        Return the class name use for analysis PL and etc
        :return: str
        """
        if self.stock.quantity > 0:
            self.cls_name = StockLong
        elif self.stock.quantity < 0:
            self.cls_name = StockShort
        else:
            raise Exception('Invalid stock identify. Stock have zero quantity.')

        return self.cls_name