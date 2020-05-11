#!/usr/bin/env python3

# Owen Kwon, hereby disclaims all copyright interest in the program "myetrade_django" written by Owen (Ohkeun) Kwon.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

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
        self.in_algorithm = 0
        self.in_stance = 1
        self.out_algorithm = 0
        self.out_stance = 1
        self.float_trade = True

    def market_order(self, count, order_id):
        print('order = %f' % count)

        if count > 0:
            self.client.buy(self.id, amount='%s'%count, currency=self.symbol,
                commit=True, payment_method=self.payment_method)
        else:
            self.client.sell(self.id, amount='%s'%(-count), currency=self.symbol,
                commit=True, payment_method=self.payment_method)

        return True

    def get_failure_reason(self):
        return 'success'

    def get_total_value(self):
        if self.count is None:
            return None
        if self.value is None:
            return None

        return self.count * self.value
