#!/usr/bin/env python3

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