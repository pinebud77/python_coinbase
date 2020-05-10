#!/usr/bin/env python3

import logging


class Quote:
    def __init__(self, client, symbol):
        self.symbol = symbol
        self.client = client
        self.currency_pair = '%s-USD' % self.symbol
        self.ask = None
        self.bid = None
        self.spot = None

    def update(self):
        self.bid = self.client.get_sell_price(currency_pair=self.currency_pair).amount
        self.ask = self.client.get_buy_price(currency_pair=self.currency_pair).amount
        self.spot = self.client.get_spot_price(currency_pair=self.currency_pair).amount
        return True


class Stock:
    def __init__(self, client, symbol, account):
        self.symbol = symbol
        self.account = account
        self.client = client

        self.count = None
        self.value = None
        self.id = None
        self.payment_method = None
        self.last_value = 0.0
        self.budget = 0.0
        self.algorithm = 0
        self.stance = 1

    def market_order(self, count, order_id):
        print('order = %f' % count)

        if count > 0:
            print(self.id)
            print(count)
            print(self.symbol)
            print(self.payment_method)

            buy = self.client.buy(self.id, amount='%s'%count, currency=self.symbol,
                commit=False, payment_method=self.payment_method)
            print(buy)
        else:
            buy = self.client.sell(self.id, amount='%s'%(-count), currency=self.symbol,
                commit=False, payment_method=self.payment_method)
            print(buy)

        return True

    def get_failure_reason(self):
        return 'success'

    def get_total_value(self):
        if self.count is None:
            return None
        if self.value is None:
            return None

        return self.count * self.value
