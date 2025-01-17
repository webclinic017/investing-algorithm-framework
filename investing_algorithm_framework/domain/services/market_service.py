import logging
from abc import ABC, abstractmethod
from datetime import datetime

logger = logging.getLogger("investing_algorithm_framework")


class MarketService(ABC):

    def __init__(self, market_credential_service):
        self._market_credential_service = market_credential_service

    @abstractmethod
    def pair_exists(
        self,
        market,
        target_symbol: str,
        trading_symbol: str,
    ):
        pass

    @abstractmethod
    def get_ticker(self, symbol, market):
        pass

    @abstractmethod
    def get_tickers(self, symbols, market):
        pass

    @abstractmethod
    def get_order_book(self, symbol, market):
        pass

    @abstractmethod
    def get_order_books(self, symbols, market):
        pass

    @abstractmethod
    def get_order(self, order, market):
        pass

    @abstractmethod
    def get_orders(self, symbol, market, since: datetime = None):
        pass

    @abstractmethod
    def get_balance(self, market):
        pass

    @abstractmethod
    def create_limit_buy_order(
        self,
        target_symbol: str,
        trading_symbol: str,
        amount: float,
        price: float,
        market
    ):
        pass

    @abstractmethod
    def create_limit_sell_order(
        self,
        target_symbol: str,
        trading_symbol: str,
        amount: float,
        price: float,
        market
    ):
        pass

    @abstractmethod
    def create_market_sell_order(
        self,
        target_symbol: str,
        trading_symbol: str,
        amount: float,
        market
    ):
        pass

    @abstractmethod
    def cancel_order(self, order, market):
        pass

    @abstractmethod
    def get_open_orders(
        self, market, target_symbol: str = None, trading_symbol: str = None
    ):
        pass

    @abstractmethod
    def get_closed_orders(
        self, market, target_symbol: str = None, trading_symbol: str = None
    ):
        pass

    @abstractmethod
    def get_ohlcv(
        self, symbol, time_frame, from_timestamp, market, to_timestamp=None
    ):
        pass

    @abstractmethod
    def get_ohlcvs(
        self, symbols, time_frame, from_timestamp, market, to_timestamp=None
    ):
        pass

    @property
    def market_credentials(self):

        if self._market_credential_service is None:
            return []

        return self._market_credential_service.get_all()

    def get_market_credentials(self):
        return self._market_credential_service.get_all()

    def get_market_credential(self, market):

        if self.market_credentials is None:
            return None

        for market_data_credentials in self.market_credentials:
            if market_data_credentials.market.lower() == market.lower():
                return market_data_credentials

        return None
