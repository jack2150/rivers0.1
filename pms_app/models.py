from django.db import models


class Pos(models.Model):
    """
    A position contains 1 instrument, 1 stock and multiple options
    """
    symbol = models.CharField(max_length=10)
    company = models.CharField(max_length=100)
    date = models.DateField()

    #noinspection PyClassHasNoInit
    class Meta:
        """
        Unique row using symbol and date
        """
        unique_together = ('symbol', 'date')

    def __unicode__(self):
        """
        Using all property inside class and return json format string
        :return: str
        """
        output = '{'
        output += 'symbol: "%s", ' % self.symbol
        output += 'company: "%s", ' % self.company
        output += 'date: "%s"' % self.date
        output += '}'

        return output


class PosIns(models.Model):
    position = models.ForeignKey(Pos)

    delta = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    gamma = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    theta = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    vega = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    pct_change = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    pl_open = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    pl_day = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    bp_effect = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    def set_dict(self, items):
        """
        using raw dict, set related column into property only
        :type items: dict
        """
        properties = vars(self)

        for key, item in items.items():
            if key in properties.keys():
                setattr(self, key, item)

    def __unicode__(self):
        """
        Using all property inside class and return json format string
        :return: str
        """
        output = '{'
        output += 'name: "%s", ' % self.position.company
        output += 'quantity: 0, '
        output += 'days: 0, '
        output += 'trade_price: 0, '
        output += 'mark: 0, '
        output += 'mark_change: 0, '
        output += 'delta: %.2f, ' % self.delta
        output += 'gamma: %.2f, ' % self.gamma
        output += 'theta: %.2f, ' % self.theta
        output += 'vega: %.2f, ' % self.vega
        output += 'pct_change: %.2f, ' % self.pct_change
        output += 'pl_open: %.2f, ' % self.pl_open
        output += 'pl_day: %.2f, ' % self.pl_day
        output += 'bp_effect: %.2f' % self.bp_effect
        output += '}'

        return output
    

class PosStock(models.Model):
    position = models.ForeignKey(Pos)

    quantity = models.IntegerField(default=0)
    trade_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    mark = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    mark_change = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    pct_change = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    pl_open = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    pl_day = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    bp_effect = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def set_dict(self, items):
        """
        using raw dict, set related column into property only
        :type items: dict
        """
        properties = vars(self)

        for key, item in items.items():
            if key in properties.keys():
                setattr(self, key, item)

    def __unicode__(self):
        output = '{'
        output += 'name: "%s", ' % self.position.symbol
        output += 'quantity: %+d, ' % self.quantity
        output += 'days: 0, '
        output += 'trade_price: %.2f, ' % self.trade_price
        output += 'mark: %.2f, ' % self.mark
        output += 'mark_change: %.2f, ' % self.mark_change
        output += 'delta: 0, '
        output += 'gamma: 0, '
        output += 'theta: 0, '
        output += 'vega: 0, '
        output += 'pct_change: %.2f, ' % self.pct_change
        output += 'pl_open: %.2f, ' % self.pl_open
        output += 'pl_day: %.2f, ' % self.pl_day
        output += 'bp_effect: %.2f' % self.bp_effect
        output += '}'

        return output


class PosOption(models.Model):
    position = models.ForeignKey(Pos)

    # option contract name
    right = models.IntegerField(default=100)
    special = models.CharField(max_length=100)
    ex_month = models.CharField(max_length=10)
    ex_year = models.IntegerField()
    strike_price = models.DecimalField(max_digits=8, decimal_places=2)
    contract = models.CharField(max_length=10)

    # position details
    quantity = models.IntegerField(default=0)
    days = models.IntegerField(default=0)
    trade_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    mark = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    mark_change = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    delta = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    gamma = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    theta = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    vega = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    pct_change = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    pl_open = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    pl_day = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    bp_effect = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    def set_dict(self, items):
        """
        using raw dict, set related column into property only
        :type items: dict
        """
        properties = vars(self)

        for key, item in items.items():
            if key in properties.keys():
                setattr(self, key, item)

            if key == 'name':
                # assign options name
                for sub_key, sub_item in item.items():
                    if sub_key in properties.keys():
                        setattr(self, sub_key, sub_item)

    def __unicode__(self):
        """
        use all property and output json format string
        """
        # prepare pct change
        if self.trade_price:
            pct_change = float(self.mark_change / self.trade_price * 100)
        else:
            pct_change = 0

        # prepare options name
        options = '%s %s %s %s %s %s' % (
            self.right,
            self.special,
            self.ex_month,
            self.ex_year,
            self.strike_price,
            self.contract
        )

        # ready output
        output = '{'
        output += 'name: "%s", ' % options
        output += 'quantity: %d, ' % self.quantity
        output += 'days: %d, ' % self.days
        output += 'trade_price: %.2f, ' % self.trade_price
        output += 'mark: %.2f, ' % self.mark
        output += 'mark_change: %.2f, ' % self.mark_change
        output += 'delta: %.2f, ' % self.delta
        output += 'gamma: %.2f, ' % self.gamma
        output += 'theta: %.2f, ' % self.theta
        output += 'vega: %.2f, ' % self.vega
        output += 'pct_change: %.2f, ' % pct_change
        output += 'pl_open: %.2f, ' % self.pl_open
        output += 'pl_day: %.2f, ' % self.pl_day
        output += 'bp_effect: 0'
        output += '}'

        return output
