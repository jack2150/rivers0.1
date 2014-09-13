from pms_app.classes import spreads
from pms_app import models


class LegOneContext(spreads.Spread):
    def __init__(self, pos_set):
        # parent init
        spreads.Spread.__init__(self, pos_set)

        # set context
        self.context = 'leg_one'

        # remove pls
        self.pls = None

    def json(self):
        """
        Return stock data in json format
        :return: str
        """
        json = '{'
        json += '"context": "%s", ' % self.context
        json += '"name": "%s", ' % self.name
        json += '"start_profit": %s, ' % self.pl.start_profit.json()
        json += '"start_loss": %s, ' % self.pl.start_loss.json()
        json += '"max_profit": %s, ' % self.pl.max_profit.json()
        json += '"max_loss": %s, ' % self.pl.max_loss.json()
        json += '"break_even": %s' % self.pl.break_even.json()
        json += '}'

        return json

    def __unicode__(self):
        """
        Describe hedge position
        :return: str
        """
        output = '%s Position:\n' % self.name
        output += '%s\n' % self.pl.start_profit
        output += '%s\n' % self.pl.max_profit
        output += '%s\n' % self.pl.start_loss
        output += '%s\n' % self.pl.max_loss
        output += '%s\n' % self.pl.break_even

        return output

    __str__ = __repr__ = __unicode__


