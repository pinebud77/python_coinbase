#!/usr/bin/env python3

# Owen Kwon, hereby disclaims all copyright interest in the program "myetrade_django" written by Owen (Ohkeun) Kwon.
#
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
from coinbase.wallet.client import Client as CoinbaseClient
from .account import Account
from .stock import Quote


class Client:
    def __init__(self):
        self.client = None

    def login(self, api_key, api_secret):
        self.client = CoinbaseClient(api_key, api_secret)
        if not self.client:
            return False

        return True

    def logout(self):
        if not self.client:
            logging.error('no session')
            raise BrokenPipeError

        del self.client
        self.client = None

        return True

    def get_account(self, account_id):
        if not self.client:
            logging.error('no session')
            raise BrokenPipeError

        account = Account(self.client, 0)
        if not account.update():
            logging.error('update of account failed')
            return None

        return account


    def get_quote(self, symbol):
        if not self.client:
            logging.error('no session')
            raise BrokenPipeError

        quote = Quote(self.client, symbol)
        quote.update()

        return quote