import random
from pms_app.classes.identify.tests import TestReadyUp
from pms_app import models

from pms_app.classes.identify.leg_one import LegOneIdentify
from pms_app.classes.spreads.leg_one import leg_one2


class TestLegOneIdentify(TestReadyUp):
    def test_long_call(self):
        """
        Test option is a long call position
        """
        for quantity in [-1, 0, 1]:
            for contract in ['CALL', 'PUT']:
                option = models.PositionOption(
                    quantity=quantity, contract=contract
                )

                leg_one_identify = LegOneIdentify(option)

                result = leg_one_identify.long_call()

                print 'quantity: %d, contract: %s' % (quantity, contract)
                print 'long call result: %s\n' % result

                if contract == 'CALL' and quantity > 0:
                    self.assertTrue(result)
                else:
                    self.assertFalse(result)

    def test_short_call(self):
        """
        Test option is a short (naked) call position
        """
        for quantity in [-1, 0, 1]:
            for contract in ['CALL', 'PUT']:
                option = models.PositionOption(
                    quantity=quantity, contract=contract
                )

                leg_one_identify = LegOneIdentify(option)

                result = leg_one_identify.short_call()

                print 'quantity: %d, contract: %s' % (quantity, contract)
                print 'long call result: %s\n' % result

                if contract == 'CALL' and quantity < 0:
                    self.assertTrue(result)
                else:
                    self.assertFalse(result)

    def test_long_put(self):
        """
        Test option is a long put position
        """
        for quantity in [-1, 0, 1]:
            for contract in ['CALL', 'PUT']:
                option = models.PositionOption(
                    quantity=quantity, contract=contract
                )

                leg_one_identify = LegOneIdentify(option)

                result = leg_one_identify.long_put()

                print 'quantity: %d, contract: %s' % (quantity, contract)
                print 'long call result: %s\n' % result

                if contract == 'PUT' and quantity > 0:
                    self.assertTrue(result)
                else:
                    self.assertFalse(result)

    def test_short_put(self):
        """
        Test option is a short (naked) put position
        """
        for quantity in [-1, 0, 1]:
            for contract in ['CALL', 'PUT']:
                option = models.PositionOption(
                    quantity=quantity, contract=contract
                )

                leg_one_identify = LegOneIdentify(option)

                result = leg_one_identify.short_put()

                print 'quantity: %d, contract: %s' % (quantity, contract)
                print 'long call result: %s\n' % result

                if contract == 'PUT' and quantity < 0:
                    self.assertTrue(result)
                else:
                    self.assertFalse(result)

    def test_get_cls(self):
        """
        Test get name using stock identify class
        """
        self.ready_all(key=3)

        for position in models.Position.objects.all():
            option = models.PositionOption.objects.filter(position=position).first()
            """:type: PositionOption"""

            leg_one_identify = LegOneIdentify(option)

            cls = leg_one_identify.get_cls()

            print 'class name: %s' % cls.__name__

            self.assertIn(
                cls,
                [leg_one2.CallLong, leg_one2.CallNaked,
                 leg_one2.PutLong, leg_one2.PutNaked,
                 None]
            )

            if cls:
                print 'current class: %s' % cls.__name__

                inst = cls(option)

                print inst

                for x in random.sample(xrange(-10, 10), 5):
                    price = inst.break_even.price + x
                    print 'price: %s, current status: %s' \
                          % (price, inst.current_status(price))

                print ''
