from spreads import StartProfit, MaxProfit, StartLoss, MaxLoss, BreakEven


class StockContext(object):
    def __init__(self):
        """
        Prepare all classes
        """
        self.name = ''

        self.start_profit = StartProfit()
        self.max_profit = MaxProfit()
        self.start_loss = StartLoss()
        self.max_loss = MaxLoss()
        self.break_even = BreakEven()

    def is_profit(self, price):
        """
        Return true if position is profit and false if not
        :return: bool
        """
        return eval('%s %s %s' % (
            price,
            self.start_profit.condition,
            self.start_profit.price
        ))

    def is_loss(self, price):
        """
        Return true if position is losing and false if not
        :return: bool
        """
        return eval('%s %s %s' % (
            price,
            self.start_loss.condition,
            self.start_loss.price
        ))

    def is_even(self, price):
        """
        Return true if position is even and false if not
        :return: bool
        """
        return eval('%s %s %s' % (
            price,
            self.break_even.condition,
            self.break_even.price
        ))

    def current_status(self, price):
        """
        Return true if price is already profit
        """
        if self.is_even(price):
            return 'Even'
        elif self.is_profit(price):
            return 'Profit'
        elif self.is_loss(price):
            return 'Loss'
        else:
            raise ValueError('Stock conditions are missing!')

    def __unicode__(self):
        """
        Describe long stock position
        :return: str
        """
        output = '%s Stock Position:\n' % self.name
        output += '%s\n' % self.start_profit
        output += '%s\n' % self.max_profit
        output += '%s\n' % self.start_loss
        output += '%s\n' % self.max_loss
        output += '%s\n' % self.break_even

        return output

    __str__ = __repr__ = __unicode__


class StockLong(StockContext):
    """
    A spread position for long stock only
    """
    def __init__(self, stock):
        """
        :param stock: PositionStock
        """
        StockContext.__init__(self)

        self.__stock = stock
        """:type: PositionStock"""

        self.name = 'Long'

        # start profit section
        self.start_profit.price = float(self.__stock.trade_price)
        self.start_profit.condition = '>'

        # max profit section
        self.max_profit.profit = 0
        self.max_profit.limit = False
        self.max_profit.price = float('inf')
        self.max_profit.condition = '=='

        # start loss section
        self.start_loss.price = float(self.__stock.trade_price)
        self.start_loss.condition = '<'

        # max loss section
        self.max_loss.loss = float(-self.__stock.trade_price * self.__stock.quantity)
        self.max_loss.limit = True
        self.max_loss.price = 0
        self.max_loss.condition = '=='

        # break even section
        self.break_even.price = float(self.__stock.trade_price)
        self.break_even.condition = '=='


class StockShort(StockContext):
    """
    A spread position for long stock only
    """
    def __init__(self, stock):
        """
        :param stock: PositionStock
        """
        StockContext.__init__(self)

        self.__stock = stock
        """:type: PositionStock"""

        self.name = 'Short'

        # start profit section
        self.start_profit.price = float(self.__stock.trade_price)
        self.start_profit.condition = '<'

        # max profit section
        self.max_profit.profit = float(self.__stock.trade_price * self.__stock.quantity)
        self.max_profit.limit = True
        self.max_profit.price = 0
        self.max_profit.condition = '=='

        # start loss section
        self.start_loss.price = float(self.__stock.trade_price)
        self.start_loss.condition = '>'

        # max loss section
        self.max_loss.loss = float('inf')
        self.max_loss.limit = False
        self.max_loss.price = float('inf')
        self.max_loss.condition = '=='

        # break even section
        self.break_even.price = float(self.__stock.trade_price)
        self.break_even.condition = '=='

