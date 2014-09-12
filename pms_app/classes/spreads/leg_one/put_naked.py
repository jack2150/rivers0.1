from pms_app.classes.spreads.leg_one import LegOneContext


class PutNaked(LegOneContext):
    """
    Naked Put positions
    """
    def __init__(self, position):
        LegOneContext.__init__(self, position)

        # set name
        self.name = 'naked_put'
        
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
        self.pl.max_profit.price = float(self.option.strike_price)
        self.pl.max_profit.condition = '>='

        # max loss
        self.pl.max_loss.amount = self.calc_max_loss()
        self.pl.max_loss.limit = True
        self.pl.max_loss.price = 0.0
        self.pl.max_loss.condition = '<='

    def calc_break_even(self):
        """
        Calculate then return the break even value
        :return: float
        """
        return float(self.option.strike_price - self.option.trade_price)

    def calc_max_profit(self):
        """
        Calculate then return the max profit value
        :return: float
        """
        return float(self.option.trade_price * abs(self.option.quantity)
                     * self.option.right)

    def calc_max_loss(self):
        """
        Calculate then return the max loss value
        :return: float
        """
        return float((self.option.strike_price - self.option.trade_price)
                     * abs(self.option.quantity) * self.option.right)