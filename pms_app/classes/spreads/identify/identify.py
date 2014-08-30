from pms_app.models import PositionStock, PositionOption


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

        self.name = None

    def identify(self):
        """
        Check how many legs, quantity, strike and etc...
        1. find which type and legs
        2. go to deep identify then decide strategy
        3. then go to strategy to define pl and etc
        """
        if self.is_closed():
            self.name = 'Position Closed'
        elif self.is_stock():
            self.name = 'Stock Position'
        elif self.is_hedge():
            self.name = 'Hedge Position'
        elif self.is_one_leg_option():
            self.name = 'One Leg Options'
        elif self.is_two_legs_options():
            self.name = 'Two Legs Options'
        elif self.is_three_legs_options():
            self.name = 'Three Legs Options'
        elif self.is_four_legs_options():
            self.name = 'Four Legs Options'
        else:
            self.name = 'Custom Options'

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







