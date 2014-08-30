from spreads.identify.test_identify import TestReadyUp
import spreads
from pms_app import models

from stock_only import StockContext, StockLong, StockShort


class TestStockOnly(TestReadyUp):
    def test_stock_context(self):
        """
        Test stock context in functions is working
        """
        self.ready_all(key=1)

        for key, position in enumerate(models.Position.objects.all()):
            stock = models.PositionStock.objects.filter(position=position).first()

            if stock.quantity > 0:
                stock_pos = StockLong(stock=stock)
            else:
                stock_pos = StockShort(stock=stock)

            print stock_pos

            self.assertEqual(type(stock_pos.max_profit), spreads.MaxProfit)
            self.assertEqual(type(stock_pos.start_profit), spreads.StartProfit)
            self.assertEqual(type(stock_pos.max_loss), spreads.MaxLoss)
            self.assertEqual(type(stock_pos.start_loss), spreads.StartLoss)
            self.assertEqual(type(stock_pos.break_even), spreads.BreakEven)

    def test_is_profit_is_loss(self):
        """
        Test is profit and is loss condition for stock
        """
        start_prices = [24.3, 55.97, 115.65, 73, 248.60]
        profit_conditions = ['>', '>', '<', '<', '>']
        loss_conditions = ['<', '<', '>', '>', '<']
        current_prices = [31.35, 40.98, 100, 155, 265.5]

        tests = zip(start_prices, profit_conditions, loss_conditions, current_prices)

        for start_price, profit_cond, loss_cond, current_price in tests:
            stock_context = StockContext()

            stock_context.start_profit.price = start_price
            stock_context.start_profit.condition = profit_cond

            stock_context.start_loss.price = start_price
            stock_context.start_loss.condition = loss_cond

            profit_result = stock_context.is_profit(price=current_price)
            loss_result = stock_context.is_loss(price=current_price)

            print 'Current Price: %s, Condition: %s, Start Price: %s' \
                  % (current_price, profit_cond, start_price)

            print 'Profit Result: %s' % profit_result
            print 'Loss Result: %s\n' % loss_result

            self.assertEqual(type(profit_result), bool)
            self.assertEqual(type(loss_result), bool)

            self.assertNotEqual(profit_result, loss_result)

    def test_is_even(self):
        """
        Test is even condition for stock
        """
        start_prices = [24.3, 55.97, 115.65, 73, 248.6]
        conditions = ['==', '==', '==', '==', '==']
        current_prices = [31.35, 55.97, 100, 73, 248.6]

        tests = zip(start_prices, conditions, current_prices)

        for start_price, condition, current_price in tests:
            stock_context = StockContext()

            stock_context.break_even.price = start_price
            stock_context.break_even.condition = condition

            result = stock_context.is_even(price=current_price)

            print 'Current Price: %s, Condition: %s, Start Price: %s' \
                  % (current_price, condition, start_price)

            print 'Break-even Result: %s\n' % result

    def test_current_status(self):
        """
        Test current status for stock position
        """
        start_prices = [24.3, 55.97, 66.6, 99.8, 73, 173, 248.60]
        profit_conditions = ['>', '>', '<', '>', '<', '>', '>']
        loss_conditions = ['<', '<', '>', '<', '>', '<', '<']
        current_prices = [31.35, 40.98, 66.6, 100, 155, 173, 265.5]

        tests = zip(start_prices, profit_conditions, loss_conditions, current_prices)

        for start_price, profit_cond, loss_cond, current_price in tests:
            stock_context = StockContext()

            stock_context.start_profit.price = start_price
            stock_context.start_profit.condition = profit_cond

            stock_context.start_loss.price = start_price
            stock_context.start_loss.condition = loss_cond

            stock_context.break_even.price = start_price
            stock_context.break_even.condition = '=='

            status = stock_context.current_status(price=current_price)

            print 'Current Price: %s, Cond P: %s, Cond L: %s, Start Price: %s' \
                  % (current_price, profit_cond, loss_cond, start_price)

            print 'Current Status: %s\n' % status

            self.assertEqual(type(status), str)
            self.assertIn(status, ('Even', 'Profit', 'Loss'))

    def test_stock_long(self):
        """
        Test long stock position that have correct format and values
        """
        self.ready_all(key=1)

        for key, position in enumerate(models.Position.objects.all()):
            stock = models.PositionStock.objects.filter(position=position).first()
            """:type: PositionStock"""

            if stock.quantity > 0:
                print 'Symbol: %s' % position.symbol
                stock_long = StockLong(stock=stock)

                print stock_long

                self.assertEqual(stock_long.start_profit.price, stock_long.break_even.price)
                self.assertEqual(stock_long.start_profit.condition, '>')

                self.assertEqual(stock_long.max_profit.profit, 0)
                self.assertEqual(stock_long.max_profit.limit, False)
                self.assertEqual(stock_long.max_profit.price, float('inf'))
                self.assertEqual(stock_long.max_profit.condition, '==')

                self.assertEqual(stock_long.start_loss.price, stock_long.break_even.price)
                self.assertEqual(stock_long.start_loss.condition, '<')

                self.assertLess(stock_long.max_loss.loss, 0)
                self.assertEqual(stock_long.max_loss.limit, True)
                self.assertLess(stock_long.max_loss.price, stock_long.break_even.price)
                self.assertEqual(stock_long.max_loss.condition, '==')

                self.assertEqual(stock_long.break_even.price, float(stock.trade_price))
                self.assertEqual(stock_long.break_even.condition, '==')

    def test_stock_short(self):
        """
        Test long stock position that have correct format and values
        """
        self.ready_all(key=1)

        for key, position in enumerate(models.Position.objects.all()):
            stock = models.PositionStock.objects.filter(position=position).first()
            """:type: PositionStock"""

            if stock.quantity < 0:
                print 'Symbol: %s' % position.symbol
                stock_short = StockShort(stock=stock)

                print stock_short

                self.assertEqual(stock_short.start_profit.price, stock_short.break_even.price)
                self.assertEqual(stock_short.start_profit.condition, '<')

                self.assertEqual(stock_short.max_profit.profit, stock.trade_price * stock.quantity)
                self.assertEqual(stock_short.max_profit.limit, True)
                self.assertLess(stock_short.max_profit.price, stock_short.break_even.price)
                self.assertEqual(stock_short.max_profit.condition, '==')

                self.assertEqual(stock_short.start_loss.price, stock_short.break_even.price)
                self.assertEqual(stock_short.start_loss.condition, '>')

                self.assertEqual(stock_short.max_loss.loss, float('inf'))
                self.assertEqual(stock_short.max_loss.limit, False)
                self.assertGreater(stock_short.max_loss.price, stock_short.break_even.price)
                self.assertEqual(stock_short.max_loss.condition, '==')

                self.assertEqual(stock_short.break_even.price, float(stock.trade_price))
                self.assertEqual(stock_short.break_even.condition, '==')
