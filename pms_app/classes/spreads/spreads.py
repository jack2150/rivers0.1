class Spread(object):
    def __init__(self):
        pass

    def first(self):
        pass


class StartProfit(object):
    """
    Start profit use for greater or less
    """
    def __init__(self, price=0.0, condition=''):
        """
        Set the parameters for max profit class
        :param price: float
        :param condition: str
        """
        self.price = price
        self.condition = condition

    def __unicode__(self):
        """
        Describe the detail of break even
        :return: str
        """
        output = '%-40s: %s %.2f' % ('Start profit when price is',
                                     self.condition, self.price)

        return output

    __str__ = __repr__ = __unicode__


class StartLoss(object):
    """
    Start loss use for greater or less
    """
    def __init__(self, price=0.0, condition=''):
        """
        Set the parameters for max profit class
        :param price: float
        :param condition: str
        """
        self.price = price
        self.condition = condition

    def __unicode__(self):
        """
        Describe the detail of break even
        :return: str
        """
        output = '%-40s: %s %.2f' % ('Start loss when price is',
                                     self.condition, self.price)

        return output

    __str__ = __repr__ = __unicode__


class MaxProfit(object):
    """
    Max profit can be use for single (trend) or double (range)
    """
    def __init__(self, profit=0.0, limit=None, price=0.0, condition=''):
        """
        Set the parameters for max profit class
        :param profit: float
        :param limit: bool
        :param price: float
        :param condition: str
        """
        self.limit = limit

        if self.limit:
            self.profit = profit
        else:
            self.profit = float("inf")

        self.price = price
        self.condition = condition

    def __unicode__(self):
        """
        Describe the detail of max profit
        :return: str
        """
        limit = 'LIMITED' if self.limit else 'UNLIMITED'

        output = '%-40s: %+.2f (%s)\n' % ('Max profit for this trade', self.profit, limit)
        output += '%-40s: %s %.2f' % ('when price move until', self.condition, self.price)

        return output

    __str__ = __repr__ = __unicode__


class MaxLoss(object):
    """
    Max loss can be use for single (trend) or double (range)
    """
    def __init__(self, loss=0.0, limit=None, price=0.0, condition=''):
        """
        Set the parameters for max profit class
        :param loss: float
        :param limit: bool
        :param price: float
        :param condition: str
        """
        self.limit = limit

        if self.limit:
            self.loss = loss
        else:
            self.loss = float("inf")

        self.price = price
        self.condition = condition

    def __unicode__(self):
        """
        Describe the detail of max loss
        :return: str
        """
        limit = 'LIMITED' if self.limit else 'UNLIMITED'

        output = '%-40s: %+.2f (%s)\n' % ('Max loss for this trade', self.loss, limit)
        output += '%-40s: %s %.2f' % ('when price move until', self.condition, self.price)

        return output

    __str__ = __repr__ = __unicode__


class BreakEven(object):
    """
    Break-even can be use for single (trend) or double (range)
    """
    def __init__(self, price=0.0, condition=''):
        """
        :param price: float
        :param condition: str
        :return:
        """
        self.price = price
        self.condition = condition

    def __unicode__(self):
        """
        Describe the detail of break even
        :return: str
        """
        output = '%-40s: %s %.2f' % ('Break-even when price is', self.condition, self.price)

        return output

    __str__ = __repr__ = __unicode__





























