from pms_app.classes.spreads.leg_one import leg_one2


class LegOneIdentify(object):
    def __init__(self, option):
        self.option = option
        """:type: PositionOption"""

        self.cls_name = None

    def long_call(self):
        """
        Return true if long call, false if not
        :return: bool
        """
        return self.option.contract == 'CALL' and self.option.quantity > 0

    def short_call(self):
        """
        Return true if short call, false if not
        :return: bool
        """
        return self.option.contract == 'CALL' and self.option.quantity < 0

    def long_put(self):
        """
        Return true if long put, false if not
        :return: bool
        """
        return self.option.contract == 'PUT' and self.option.quantity > 0

    def short_put(self):
        """
        Return true if short put, false if not
        :return: bool
        """
        return self.option.contract == 'PUT' and self.option.quantity < 0

    def get_cls(self):
        """
        Return the class name use for analysis PL and etc
        :return: type
        """
        if self.long_call():
            self.cls_name = leg_one2.CallLong
        elif self.short_call():
            self.cls_name = leg_one2.CallNaked
        elif self.long_put():
            self.cls_name = leg_one2.PutLong
        elif self.short_put():
            self.cls_name = leg_one2.PutNaked
        else:
            self.cls_name = None

        return self.cls_name
