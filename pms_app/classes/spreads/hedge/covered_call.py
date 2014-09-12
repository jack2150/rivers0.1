from pms_app.classes.spreads.hedge import HedgeContext


class CoveredCall(HedgeContext):
    """
    Covered Call position and calculation
    """
    def __init__(self, position):
        HedgeContext.__init__(self, position)

        self.name = 'covered_call'

        # start profit
        self.pl.start_profit.price = self.calc_break_even()
        self.pl.start_profit.condition = '>'

        # start loss
        self.pl.start_loss.price = self.calc_break_even()
        self.pl.start_loss.condition = '<'

        # break even
        self.pl.break_even.price = self.calc_break_even()
        self.pl.break_even.condition = '=='

        # max profit
        self.pl.max_profit.amount = self.calc_max_profit()
        self.pl.max_profit.limit = True
        self.pl.max_profit.price = float(self._options[0].strike_price)
        self.pl.max_profit.condition = '>='

        # max loss
        self.pl.max_loss.amount = self.calc_max_loss()
        self.pl.max_loss.limit = True
        self.pl.max_loss.price = 0.0
        self.pl.max_loss.condition = '=='

    def calc_break_even(self):
        """
        Calculate then return break even value
        :return: float
        """
        return float(self._stock.trade_price - self._options[0].trade_price)

    def calc_max_profit(self):
        """
        Calculate then return max profit value
        :return: float
        """
        return float((self._options[0].trade_price + self._options[0].strike_price
                     - self._stock.trade_price) * self._stock.quantity)

    def calc_max_loss(self):
        """
        Calculate then return max loss value
        :return: float
        """
        return float((self._stock.trade_price - self._options[0].trade_price)
                     * self._stock.quantity)