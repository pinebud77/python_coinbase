import logging
from .stock import Stock, Quote


class Account:
    def __init__(self, client, id):
        self.id = id
        self.client = client
        self.net_value = None
        self.cash_to_trade = None
        self.stock_dict = {}
        self.mode = 'setup'
        self.payment_method='deadbeef'

        payment_methods = self.client.get_payment_methods()
        for payment_method in payment_methods.data:
            if payment_method.name == 'Cash (USD)':
                self.payment_method = payment_method.id
                break

    def update(self):
        accounts = self.client.get_accounts()

        self.stock_dict = {}
        self.net_value = 0
        self.cash_to_trade = 0
        for cur in accounts.data:
            amount = float(cur.balance.amount)
            if amount == 0:
                continue
            if cur.balance.currency == 'USD':
                self.cash_to_trade += amount
                continue

            symbol = cur.balance.currency
            amount = amount
            value = float(cur.native_balance.amount) / amount
            self.net_value += value

            stock = Stock(self.client, symbol, self)
            stock.count = amount
            stock.value = value
            stock.id = cur.id
            stock.payment_method = self.payment_method

            self.stock_dict[symbol] = stock

        self.net_value += self.cash_to_trade

        return True

    def get_stock(self, symbol):
        try:
            return self.stock_dict[symbol]
        except KeyError:
            return None

    def new_stock(self, symbol):
        stock = Stock(self.client, symbol, self)
        quote = Quote(self.client, symbol)
        if not quote.update():
            logging.error('getting quote returned error')
            return None

        stock.value = float(quote.spot.amount)
        stock.count = 0
        stock.id = stock.symbol
        stock.payment_method = self.payment_method

        self.stock_dict[symbol] = stock

        return stock



