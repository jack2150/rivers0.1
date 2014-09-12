from pms_app.classes.spreads.hedge import CoveredCall, ProtectiveCall, CoveredPut, ProtectivePut


class HedgeIdentify(object):
    def __init__(self, stock, option):
        self.stock = stock
        """:type: PositionStock"""

        self.option = option
        """:type: PositionOption"""

        self.cls_name = None

    def long_stock(self):
        """
        Return true if long stock, false if not
        :rtype : bool
        """
        return self.stock.quantity > 0

    def short_stock(self):
        """
        Return true if short stock, false if not
        :rtype : bool
        """
        return self.stock.quantity < 0

    def buy_call_option(self):
        """
        Return true if buy call option
        :return: bool
        """
        return self.option.contract == 'CALL' and self.option.quantity > 0

    def sell_call_option(self):
        """
        Return true if sell call option
        :return: bool
        """
        return self.option.contract == 'CALL' and self.option.quantity < 0

    def buy_put_option(self):
        """
        Return true if buy put option
        :return: bool
        """
        return self.option.contract == 'PUT' and self.option.quantity > 0

    def sell_put_option(self):
        """
        Return true if sell put option
        :return: bool
        """
        return self.option.contract == 'PUT' and self.option.quantity < 0

    def is_balance(self):
        """
        Return true if stock and option are balance 1 option = 100 shares
        :return: bool
        """
        return abs(self.stock.quantity) == abs(self.option.quantity * 100)

    def get_cls(self):
        """
        Return the class name use for analysis PL and etc
        :return: type
        """
        if self.long_stock() and self.sell_call_option() and self.is_balance():
            # covered call
            self.cls_name = CoveredCall
        elif self.long_stock() and self.buy_put_option() and self.is_balance():
            # protective put
            self.cls_name = ProtectivePut
        elif self.short_stock() and self.buy_call_option() and self.is_balance():
            # protective call
            self.cls_name = ProtectiveCall
        elif self.short_stock() and self.sell_put_option() and self.is_balance():
            # covered put
            self.cls_name = CoveredPut
        else:
            self.cls_name = None

        return self.cls_name



