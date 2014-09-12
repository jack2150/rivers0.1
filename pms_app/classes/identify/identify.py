from pms_app.models import PositionStock, PositionOption
from pms_app.classes.identify.stock import StockIdentify
from pms_app.classes.identify.hedge import HedgeIdentify
from pms_app.classes.identify.leg_one import LegOneIdentify


class Identify(object):
    def __init__(self, position):
        """
        Set stock and options at init
        :param position: models.Position
        """
        self.stock = PositionStock.objects.filter(position=position).first()
        """:type: PositionStock"""

        self.options = list()
        """:type: list of PositionOption"""

        options = PositionOption.objects.filter(position=position)
        for option in options.exclude(quantity=0).all():
            self.options.append(option)

        self.__spread = None

    def get_spread(self):
        """
        Return string for identify spreads type
        :return: str
        """
        if self.__spread is None:
            self.identify()

        return self.__spread

    def set_spread(self, x):
        """
        Set string into spreads type name
        :param x: str
        """
        self.__spread = x

    spread = property(fget=get_spread, fset=set_spread)

    def get_first_option(self):
        """
        Return first item in options list
        :return: PositionOption
        """
        # todo: no test yet
        return self.options[0]

    def identify(self):
        """
        Check how many legs, quantity, strike and etc...
        1. find which type and legs
        2. go to deep identify then decide strategy
        3. then go to strategy to define pl and etc
        """
        if self.is_closed():
            #self.__spread = 'Position Closed'
            self.__spread = None

        elif self.is_stock():
            #self.__name = 'Stock Position'
            cls = StockIdentify(self.stock).get_cls()
            self.__spread = cls(self.stock)

        elif self.is_hedge():
            #self.__name = 'Hedge Position'
            cls = HedgeIdentify(self.stock, self.get_first_option()).get_cls()
            self.__spread = cls(self.stock, self.get_first_option())

        elif self.is_one_leg_option():
            #self.__name = 'One Leg Options'
            cls = LegOneIdentify(self.get_first_option()).get_cls()
            self.__spread = cls(self.get_first_option())

        elif self.is_two_legs_options():
            #self.__spread = 'Two Legs Options'
            self.__spread = None

        elif self.is_three_legs_options():
            #self.__spread = 'Three Legs Options'
            self.__spread = None

        elif self.is_four_legs_options():
            #self.__spread = 'Four Legs Options'
            self.__spread = None

        else:
            #self.__spread = 'Custom Options'
            self.__spread = None

    def is_closed(self):
        """
        Return true if positions is closed and false if not
        :return: bool
        """
        return bool(not self.stock.quantity and not len(self.options))

    def is_stock(self):
        """
        Return true if positions is stock and if not false
        :rtype : bool
        """
        return bool(self.stock.quantity and not len(self.options))

    def is_hedge(self):
        """
        Return true if hedge positions (stock + options) and false if not
        :return: bool
        """
        return bool(self.stock.quantity and len(self.options))

    def is_one_leg_option(self):
        """
        Return true if one leg option only positions and false if not
        :return: bool
        """
        return bool(not self.stock.quantity and len(self.options) == 1)

    def is_two_legs_options(self):
        """
        Return true if two legs option positions and false if not
        :return: bool
        """
        return bool(not self.stock.quantity and len(self.options) == 2)

    def is_three_legs_options(self):
        """
        Return true if three legs option positions and false if not
        :return: bool
        """
        return bool(not self.stock.quantity and len(self.options) == 3)

    def is_four_legs_options(self):
        """
        Return true if two legs option positions and false if not
        :return: bool
        """
        return bool(not self.stock.quantity and len(self.options) == 4)







