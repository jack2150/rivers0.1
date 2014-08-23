from pms_app.models import PositionStock, PositionOption


class Spreads(object):
    def __init__(self, position):
        """
        Set stock and options at init
        :param position: models.Position
        """
        self.stock = PositionStock.objects.filter(position=position).first()
        """:type: PositionStock"""

        self.options = list()
        """:type: list of PositionOption"""
        for option in PositionOption.objects.filter(position=position).all():
            self.options.append(option)

    def identity(self):
        """
        Check how many legs, quantity, strike and etc...
        """
        print self.stock
        print self.options

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

    def is_two_leg_options(self):
        """
        Return true if two legs option positions and false if not
        :return: bool
        """
        return bool(not self.stock.quantity and len(self.options) == 2)









