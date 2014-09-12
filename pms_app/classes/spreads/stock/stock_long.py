from pms_app.classes.spreads.stock.stock_context import StockContext


class StockLong(StockContext):
    """
    A spread position for long stock only
    """
    def __init__(self, position):
        """
        :param position: Position
        """
        StockContext.__init__(self, position)

        self.name = 'long_stock'

        # start profit section
        self.pl.start_profit.price = float(self._stock.trade_price)
        self.pl.start_profit.condition = '>'

        # max profit section
        self.pl.max_profit.amount = 0
        self.pl.max_profit.limit = False
        self.pl.max_profit.price = float('inf')
        self.pl.max_profit.condition = '=='

        # start loss section
        self.pl.start_loss.price = float(self._stock.trade_price)
        self.pl.start_loss.condition = '<'

        # max loss section
        self.pl.max_loss.amount = float(self._stock.trade_price * self._stock.quantity)
        self.pl.max_loss.limit = True
        self.pl.max_loss.price = 0
        self.pl.max_loss.condition = '=='

        # break even section
        self.pl.break_even.price = float(self._stock.trade_price)
        self.pl.break_even.condition = '=='