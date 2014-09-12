from pms_app.classes.spreads import StartProfit, MaxProfit, StartLoss, MaxLoss, BreakEven


class LegOneContext(object):
    def __init__(self):
        """
        Prepare all classes
        """
        self.name = ''
        self.context = 'leg_one'

        self.start_profit = StartProfit()
        self.max_profit = MaxProfit()
        self.start_loss = StartLoss()
        self.max_loss = MaxLoss()
        self.break_even = BreakEven()

    def is_max_profit(self, price):
        """
        Return true if position is in max profit and false if not
        :return: bool
        """
        return eval('%s %s float("%s")' % (
            price,
            self.max_profit.condition,
            self.max_profit.price
        ))

    def is_profit(self, price):
        """
        Return true if position is profit and false if not
        :return: bool
        """
        return eval('%s %s float("%s")' % (
            price,
            self.start_profit.condition,
            self.start_profit.price
        ))

    def is_max_loss(self, price):
        """
        Return true if position is in max loss and false if not
        :return: bool
        """
        return eval('%s %s float("%s")' % (
            price,
            self.max_loss.condition,
            self.max_loss.price
        ))

    def is_loss(self, price):
        """
        Return true if position is losing and false if not
        :return: bool
        """
        return eval('%s %s float("%s")' % (
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
        :return: str
        """
        if self.is_even(price):
            result = 'even'
        elif self.is_max_profit(price):
            result = 'max_profit'
        elif self.is_profit(price):
            result = 'profit'
        elif self.is_max_loss(price):
            result = 'max_loss'
        elif self.is_loss(price):
            result = 'loss'
        else:
            raise ValueError('Stock conditions are missing!')

        return result

    def json(self):
        """
        Return stock data in json format
        :return: str
        """
        json = '{'
        json += '"context": "%s", ' % self.context
        json += '"name": "%s", ' % self.name
        json += '"start_profit": %s, ' % self.start_profit.json()
        json += '"start_loss": %s, ' % self.start_loss.json()
        json += '"max_profit": %s, ' % self.max_profit.json()
        json += '"max_loss": %s, ' % self.max_loss.json()
        json += '"break_even": %s' % self.break_even.json()
        json += '}'

        return json

    def __unicode__(self):
        """
        Describe one leg option position
        :return: str
        """
        output = '%s Position:\n' % self.name
        output += '%s\n' % self.start_profit
        output += '%s\n' % self.max_profit
        output += '%s\n' % self.start_loss
        output += '%s\n' % self.max_loss
        output += '%s\n' % self.break_even

        return output

    __str__ = __repr__ = __unicode__


class CallLong(LegOneContext):
    """
    Long Call positions
    """
    def __init__(self, option):
        LegOneContext.__init__(self)

        self.__option = option
        """:type: PositionOption"""

        # set name
        self.name = 'Long Call'

        # start profit
        self.start_profit.price = self.calc_break_even()
        self.start_profit.condition = '>'

        # start loss
        self.start_loss.price = self.calc_break_even()
        self.start_loss.condition = '<'

        # break even
        self.break_even.price = self.calc_break_even()
        self.break_even.condition = '=='

        # max profit
        self.max_profit.amount = float('inf')
        self.max_profit.limit = False
        self.max_profit.price = float('inf')
        self.max_profit.condition = '=='

        # max loss
        self.max_loss.amount = self.calc_max_loss()
        self.max_loss.limit = True
        self.max_loss.price = float(self.__option.strike_price)
        self.max_loss.condition = '<='

    def calc_break_even(self):
        """
        Calculate then return the break even value
        :return: float
        """
        return float(self.__option.strike_price + self.__option.trade_price)

    def calc_max_loss(self):
        """
        Calculate then return the max loss value
        :return: float
        """
        return float(self.__option.trade_price * self.__option.quantity
                     * self.__option.right)


class CallNaked(LegOneContext):
    """
    Sell naked call positions
    """
    def __init__(self, option):
        LegOneContext.__init__(self)

        self.__option = option
        """:type: PositionOption"""

        # set name
        self.name = 'Naked Call'

        # start profit
        self.start_profit.price = self.calc_break_even()
        self.start_profit.condition = '<'

        # start loss
        self.start_loss.price = self.calc_break_even()
        self.start_loss.condition = '>'

        # break even
        self.break_even.price = self.calc_break_even()
        self.break_even.condition = '=='

        # max profit
        self.max_profit.amount = self.calc_max_profit()
        self.max_profit.limit = True
        self.max_profit.price = float(self.__option.strike_price)
        self.max_profit.condition = '<='

        # max loss
        self.max_loss.amount = float('inf')
        self.max_loss.limit = False
        self.max_loss.price = float('inf')
        self.max_loss.condition = '=='

    def calc_break_even(self):
        """
        Calculate then return the break even value
        :return: float
        """
        return float(self.__option.strike_price + self.__option.trade_price)

    def calc_max_profit(self):
        """
        Calculate then return the break even value
        :return: float
        """
        return float(self.__option.trade_price * abs(self.__option.quantity)
                     * self.__option.right)


class PutLong(LegOneContext):
    """
    Long Put Positions
    """
    def __init__(self, option):
        LegOneContext.__init__(self)

        self.__option = option
        """:type: PositionOption"""

        # set name
        self.name = 'Long Put'

        # start profit
        self.start_profit.price = self.calc_break_even()
        self.start_profit.condition = '<'

        # start loss
        self.start_loss.price = self.calc_break_even()
        self.start_loss.condition = '>'

        # break even
        self.break_even.price = self.calc_break_even()
        self.break_even.condition = '=='

        # max profit
        self.max_profit.amount = self.calc_max_profit()
        self.max_profit.limit = True
        self.max_profit.price = 0.0
        self.max_profit.condition = '=='

        # max loss
        self.max_loss.amount = self.calc_max_loss()
        self.max_loss.limit = True
        self.max_loss.price = float(self.__option.strike_price)
        self.max_loss.condition = '>='

    def calc_break_even(self):
        """
        Calculate then return the break even value
        :return: float
        """
        return float(self.__option.strike_price - self.__option.trade_price)

    def calc_max_profit(self):
        """
        Calculate then return the max profit value
        :return: float
        """
        return float((self.__option.strike_price - self.__option.trade_price)
                     * self.__option.quantity * self.__option.right)

    def calc_max_loss(self):
        """
        Calculate then return the max loss value
        :return: float
        """
        return float(self.__option.trade_price * self.__option.quantity
                     * self.__option.right)


class PutNaked(LegOneContext):
    """
    Sell naked put positions
    """
    def __init__(self, option):
        LegOneContext.__init__(self)

        self.__option = option
        """:type: PositionOption"""

        # set name
        self.name = 'Naked Put'

        # start profit
        self.start_profit.price = self.calc_break_even()
        self.start_profit.condition = '>'

        # start loss
        self.start_loss.price = self.calc_break_even()
        self.start_loss.condition = '<'

        # break even
        self.break_even.price = self.calc_break_even()
        self.break_even.condition = '=='

        # max profit
        self.max_profit.amount = self.calc_max_profit()
        self.max_profit.limit = True
        self.max_profit.price = float(self.__option.strike_price)
        self.max_profit.condition = '>='

        # max loss
        self.max_loss.amount = self.calc_max_loss()
        self.max_loss.limit = True
        self.max_loss.price = 0.0
        self.max_loss.condition = '<='

    def calc_break_even(self):
        """
        Calculate then return the break even value
        :return: float
        """
        return float(self.__option.strike_price - self.__option.trade_price)

    def calc_max_profit(self):
        """
        Calculate then return the max profit value
        :return: float
        """
        return float(self.__option.trade_price * abs(self.__option.quantity)
                     * self.__option.right)

    def calc_max_loss(self):
        """
        Calculate then return the max loss value
        :return: float
        """
        return float((self.__option.strike_price - self.__option.trade_price)
                     * abs(self.__option.quantity) * self.__option.right)