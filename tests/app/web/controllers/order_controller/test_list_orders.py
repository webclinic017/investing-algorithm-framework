import json

from investing_algorithm_framework import TradingStrategy, \
    TimeUnit, PortfolioConfiguration
from tests.resources import FlaskTestBase


class StrategyOne(TradingStrategy):
    time_unit = TimeUnit.SECOND
    interval = 1

    def apply_strategy(
        self,
        algorithm,
        market_data,
    ):
        algorithm.create_order(
            target_symbol="BTC",
            amount=1,
            price=10,
            order_side="BUY",
            order_type="LIMIT",
        )


class Test(FlaskTestBase):
    portfolio_configurations = [
        PortfolioConfiguration(
            market="BITVAVO",
            trading_symbol="USDT"
        )
    ]

    def setUp(self) -> None:
        super(Test, self).setUp()
        self.iaf_app.add_strategy(StrategyOne)

    def test_list_portfolios(self):
        order_repository = self.iaf_app.container.order_repository()
        self.iaf_app.run(number_of_iterations=1, sync=False)
        self.assertEqual(1, order_repository.count())
        response = self.client.get("/api/orders")
        data = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(data["items"]))
