<a href=https://investing-algorithm-framework.com><img src="https://img.shields.io/badge/docs-website-brightgreen"></a>
[![Build](https://github.com/coding-kitties/investing-algorithm-framework/actions/workflows/build.yml/badge.svg)](https://github.com/coding-kitties/investing-algorithm-framework/actions/workflows/build.yml)
[![Tests](https://github.com/coding-kitties/investing-algorithm-framework/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/coding-kitties/investing-algorithm-framework/actions/workflows/test.yml)
[![Downloads](https://pepy.tech/badge/investing-algorithm-framework)](https://pepy.tech/badge/investing-algorithm-framework)
[![Current Version](https://img.shields.io/pypi/v/investing_algorithm_framework.svg)](https://img.shields.io/pypi/v/investing_algorithm_framework.svg)
<a href="https://www.reddit.com/r/InvestingBots/"><img src="https://img.shields.io/reddit/subreddit-subscribers/investingbots?style=social"></a> <br/>
[![GitHub stars](https://img.shields.io/github/stars/coding-kitties/investing-algorithm-framework.svg?style=social&label=Star&maxAge=1)](https://github.com/SeaQL/sea-orm/stargazers/) If you like what we do, consider starring, sharing and contributing!

###### Sponsors
<p align="left">
<a href="https://finterion.com">
  <img alt="Finterion" src="https://logicfunds-web-app-images.s3.eu-central-1.amazonaws.com/finterion.png" width="200px" />
</a>
</p>


# [Investing Algorithm Framework](https://github.com/coding-kitties/investing-algorithm-framework)

The Investing Algorithm Framework is a Python tool that enables swift and 
elegant development of trading bots. It comes with all the necessary 
components for creating algorithms, including data provisioning, 
portfolio management, and order execution.

Features: 
* Order execution
* Broker and exchange connections through [ccxt](https://github.com/ccxt/ccxt)
* Backtesting and performance analysis reports
* Portfolio management
* Web API for interacting with your deployed trading bot
* Data persistence through sqlite db or an in-memory db
* Stateless running for cloud function deployments
* Polars dataframes support out of the box for fast data processing [pola.rs](https://pola.rs/)



## Example implementation
The following algorithm connects to binance and buys BTC every 5 seconds. 
It also exposes an REST API that allows you to interact with the algorithm.
```python
import pathlib
from datetime import datetime, timedelta
from investing_algorithm_framework import create_app, PortfolioConfiguration, \
    RESOURCE_DIRECTORY, TimeUnit, CCXTOHLCVMarketDataSource, Algorithm, \
    CCXTTickerMarketDataSource, MarketCredential

# Define market data sources
bitvavo_btc_eur_ohlcv_2h = CCXTOHLCVMarketDataSource(
    identifier="BTC-ohlcv",
    market="BITVAVO",
    symbol="BTC/EUR",
    timeframe="2h",
    window_size=200
)
# Ticker data for orders, trades and positions
bitvavo_btc_eur_ticker = CCXTTickerMarketDataSource(
    identifier="BTC-ticker",
    market="BITVAVO",
    symbol="BTC/EUR",
)
app = create_app({RESOURCE_DIRECTORY: pathlib.Path(__file__).parent.resolve()})
app.add_market_data_source(bitvavo_btc_eur_ohlcv_2h)
app.add_market_data_source(bitvavo_btc_eur_ticker)
app.add_market_credential(MarketCredential(
    market="bitvavo",
    api_key="<your api key>",
    secret_key="<your secret key>",
))
app.add_portfolio_configuration(
    PortfolioConfiguration(
        market="bitvavo",
        trading_symbol="EUR",
        initial_balance=400
    )
)

@app.strategy(
    # Run every two hours
    time_unit=TimeUnit.HOUR, 
    interval=2, 
    # Specify market data sources that need to be passed to the strategy
    market_data_sources=["BTC-ticker", "BTC-ohlcv"]
)
def perform_strategy(algorithm: Algorithm, market_data: dict):
    # By default data is passed as polars dataframe https://pola.rs/
    df = market_data["BTC-ohlcv"].to_pandas()
    ticker_data = market_data["BTC-ticker"]
    algorithm.create_limit_order(
        target_symbol="BTC/EUR",
        order_side="buy",
        amount=0.01,
        price=ticker_data["ask"],
    )
    
if __name__ == "__main__":
    app.run()
```

> You can find more examples [here](./examples) folder.

## Backtesting
The framework also supports backtesting. You can use the same code as above,
but instead of running the algorithm, you can run a backtest.

```python
import pathlib
from datetime import datetime, timedelta
from investing_algorithm_framework import create_app, RESOURCE_DIRECTORY, \
    TimeUnit, CCXTOHLCVMarketDataSource, Algorithm, pretty_print_backtest, \
    CCXTTickerMarketDataSource, PortfolioConfiguration

# Define market data sources
bitvavo_btc_eur_ohlcv_2h = CCXTOHLCVMarketDataSource(
    identifier="BTC-ohlcv",
    market="bitvavo",
    symbol="BTC/EUR",
    timeframe="2h", 
    window_size=200
)
bitvavo_btc_eur_ticker = CCXTTickerMarketDataSource(
    identifier="BTC-ticker",
    market="bitvavo",
    symbol="BTC/EUR",
    backtest_timeframe="2h" # We want the ticker data to 
    # be sampled every 2 hours, inline with the strategy interval
)
app = create_app({RESOURCE_DIRECTORY: pathlib.Path(__file__).parent.resolve()})
app.add_market_data_source(bitvavo_btc_eur_ohlcv_2h)
app.add_market_data_source(bitvavo_btc_eur_ticker)
app.add_portfolio_configuration(PortfolioConfiguration(
    initial_balance=400,
    market="bitvavo",
    trading_symbol="EUR",
))


@app.strategy(
    time_unit=TimeUnit.HOUR, 
    interval=2, 
    market_data_sources=["BTC-ticker", "BTC-ohlcv"]
)
def perform_strategy(algorithm: Algorithm, market_data: dict):
    print(
        f"Performing trading strategy on market " +
        f"data {market_data['BTC-ohlcv'] and market_data['BTC-ticker']}"
    )

if __name__ == "__main__":
    backtest_report = app.backtest(
        start_date=datetime(2023, 11, 12) - timedelta(days=10),
        end_date=datetime(2023, 11, 12),
    )
    pretty_print_backtest(backtest_report)
```
For more examples, check out the [examples](./examples/backtesting) folder.

### Backtesting report
You can use the ```pretty_print_backtest``` function to print a backtest report.
For example if you run the [moving average example trading bot](./examples/crossover_moving_average_trading_bot)
you will get the following backtesting report:
 
```bash
====================Backtest report===============================
* Start date: 2023-08-24 00:00:00
* End date: 2023-12-02 00:00:00
* Number of days: 100
* Number of runs: 1201
====================Portfolio overview============================
* Number of orders: 40
* Initial balance: 400.0000 EUR
* Final balance: 428.2434 EUR
* Total net gain: 28.2434 EUR
* Total net gain percentage: 7.0609%
* Growth rate: 7.0609%
* Growth 28.2434 EUR
====================Positions overview========================
╭────────────┬──────────┬──────────────────┬──────────────┬───────────────┬───────────────────────────┬────────────────┬───────────────╮
│ Position   │   Amount │   Pending amount │   Cost (EUR) │   Value (EUR) │ Percentage of portfolio   │   Growth (EUR) │ Growth_rate   │
├────────────┼──────────┼──────────────────┼──────────────┼───────────────┼───────────────────────────┼────────────────┼───────────────┤
│ EUR        │  428.243 │                0 │      428.243 │       428.243 │ 100.0000%                 │              0 │ 0.0000%       │
╰────────────┴──────────┴──────────────────┴──────────────┴───────────────┴───────────────────────────┴────────────────┴───────────────╯
====================Trades overview===========================
* Number of trades closed: 20
* Number of trades open: 0
* Percentage of positive trades: 30.0%
* Percentage of negative trades: 70.0%
* Average trade size: 100.9692 EUR
* Average trade duration: 83.6 hours
╭─────────┬─────────────────────┬─────────────────────┬────────────────────┬──────────────┬──────────────────┬───────────────────────┬────────────────────┬─────────────────────╮
│ Pair    │ Open date           │ Close date          │   Duration (hours) │   Size (EUR) │   Net gain (EUR) │ Net gain percentage   │   Open price (EUR) │   Close price (EUR) │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ DOT-EUR │ 2023-11-24 12:00:00 │ 2023-11-27 14:00:00 │                 74 │     107.55   │          -1.9587 │ -1.8212%              │             4.777  │              4.69   │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ DOT-EUR │ 2023-11-20 00:00:00 │ 2023-11-21 08:00:00 │                 32 │     109.39   │          -4.5949 │ -4.2005%              │             4.9875 │              4.778  │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ BTC-EUR │ 2023-11-19 22:00:00 │ 2023-11-22 00:00:00 │                 50 │     109.309  │          -2.7624 │ -2.5272%              │         34159.1    │          33295.9    │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ BTC-EUR │ 2023-11-06 12:00:00 │ 2023-11-13 14:00:00 │                170 │     107.864  │           6.1015 │ 5.6567%               │         32685.9    │          34534.9    │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ DOT-EUR │ 2023-10-20 12:00:00 │ 2023-10-27 08:00:00 │                164 │      99.085  │          10.9799 │ 11.0813%              │             3.5465 │              3.9395 │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ BTC-EUR │ 2023-10-14 04:00:00 │ 2023-10-27 22:00:00 │                330 │      97.4278 │          24.137  │ 24.7742%              │         25638.9    │          31990.7    │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ DOT-EUR │ 2023-10-14 04:00:00 │ 2023-10-17 14:00:00 │                 82 │      99.5572 │          -1.8877 │ -1.8961%              │             3.56   │              3.4925 │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ DOT-EUR │ 2023-10-07 08:00:00 │ 2023-10-08 08:00:00 │                 24 │      99.9498 │          -1.5708 │ -1.5716%              │             3.8815 │              3.8205 │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ BTC-EUR │ 2023-09-27 10:00:00 │ 2023-10-05 20:00:00 │                202 │      98.2888 │           3.433  │ 3.4927%               │         25202.2    │          26082.5    │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ DOT-EUR │ 2023-09-27 10:00:00 │ 2023-10-03 20:00:00 │                154 │      98.7893 │           1.2085 │ 1.2233%               │             3.842  │              3.889  │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ DOT-EUR │ 2023-09-25 12:00:00 │ 2023-09-27 04:00:00 │                 40 │      98.9193 │          -0.5194 │ -0.5251%              │             3.809  │              3.789  │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ DOT-EUR │ 2023-09-14 16:00:00 │ 2023-09-18 02:00:00 │                 82 │      98.9419 │          -0.0912 │ -0.0921%              │             3.799  │              3.7955 │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ BTC-EUR │ 2023-09-07 06:00:00 │ 2023-09-10 16:00:00 │                 82 │      98.6093 │           0.3412 │ 0.3460%               │         24051      │          24134.3    │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ DOT-EUR │ 2023-09-07 00:00:00 │ 2023-09-09 02:00:00 │                 50 │      98.9158 │          -0.2358 │ -0.2383%              │             3.986  │              3.9765 │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ DOT-EUR │ 2023-09-05 14:00:00 │ 2023-09-06 12:00:00 │                 22 │      99.2132 │          -1.1909 │ -1.2003%              │             3.999  │              3.951  │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ DOT-EUR │ 2023-09-04 16:00:00 │ 2023-09-04 22:00:00 │                  6 │      99.355  │          -0.5671 │ -0.5708%              │             3.942  │              3.9195 │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ DOT-EUR │ 2023-09-04 10:00:00 │ 2023-09-04 14:00:00 │                  4 │      99.4774 │          -0.4889 │ -0.4914%              │             3.968  │              3.9485 │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ BTC-EUR │ 2023-08-26 10:00:00 │ 2023-08-26 18:00:00 │                  8 │      99.0829 │          -0.03   │ -0.0302%              │         24166.6    │          24159.3    │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ DOT-EUR │ 2023-08-25 10:00:00 │ 2023-08-28 10:00:00 │                 72 │      99.659  │          -0.6975 │ -0.6999%              │             4.1435 │              4.1145 │
├─────────┼─────────────────────┼─────────────────────┼────────────────────┼──────────────┼──────────────────┼───────────────────────┼────────────────────┼─────────────────────┤
│ DOT-EUR │ 2023-08-24 00:00:00 │ 2023-08-25 00:00:00 │                 24 │      99.9999 │          -1.3626 │ -1.3626%              │             4.1465 │              4.09   │
╰─────────┴─────────────────────┴─────────────────────┴────────────────────┴──────────────┴──────────────────┴───────────────────────┴────────────────────┴─────────────────────╯
==================================================================
```

## Broker/Exchange configuration
The framework has by default support for [ccxt](https://github.com/ccxt/ccxt).
This should allow you to connect to a lot of brokers/exchanges.

```python
from investing_algorithm_framework import PortfolioConfiguration, \
    MarketCredential, create_app
app = create_app()
app.add_market_credential(
    MarketCredential(
        market="<your market>", 
        api_key="<your api key>",
        secret_key="<your secret key>",
    )
)
app.add_portfolio_configuration(
    PortfolioConfiguration(
        market="<your market>", 
        initial_balance=400,
        track_from="01/01/2022",
        trading_symbol="EUR"
    )
)
```

## Performance
We continiously are working on improving the performance of the framework.

## Download
You can download the framework with pypi.

```bash
pip install investing-algorithm-framework
```

## Disclaimer
If you use this framework for your investments, do not risk money 
which you are afraid to lose, until you have clear understanding how 
the framework works. We can't stress this enough:

BEFORE YOU START USING MONEY WITH THE FRAMEWORK, MAKE SURE THAT YOU TESTED 
YOUR COMPONENTS THOROUGHLY. USE THE SOFTWARE AT YOUR OWN RISK. 
THE AUTHORS AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR INVESTMENT RESULTS.

Also, make sure that you read the source code of any plugin you use or 
implementation of an algorithm made with this framework.

## Documentation

All the documentation can be found online 
at the [documentation webstie](https://investing-algorithm-framework.com)

In most cases, you'll probably never have to change code on this repo directly 
if you are building your algorithm/bot. But if you do, check out the 
contributing page at the website.

If you'd like to chat with investing-algorithm-framework users 
and developers, [join us on Slack](https://inv-algo-framework.slack.com) or [join us on reddit](https://www.reddit.com/r/InvestingBots/)

## Acknowledgements
We want to thank all contributors to this project. A full list of all 
the people that contributed to the project can be
found [here](https://github.com/investing-algorithms/investing-algorithm-framework/blob/master/AUTHORS.md)

### [Bugs / Issues](https://github.com/investing-algorithms/investing-algorithm-framework/issues?q=is%3Aissue)

If you discover a bug in the framework, please [search our issue tracker](https://github.com/investing-algorithms/investing-algorithm-framework/issues?q=is%3Aissue)
first. If it hasn't been reported, please [create a new issue](https://github.com/investing-algorithms/investing-algorithm-framework/issues/new).

### Contributing
The investing algorithm framework is a community driven project. 
We welcome you to participate, contribute and together help build 
the future trading bots developed in pyhton.

Feel like the framework is missing a feature? We welcome your pull requests!
If you want to contribute to the project roadmap, please take a look at the [project board](https://github.com/coding-kitties/investing-algorithm-framework/projects?query=is%3Aopen).
You can pick up a task by assigning yourself to it. 

**Note** before starting any major new feature work, *please open an issue describing what you are planning to do*.
This will ensure that interested parties can give valuable feedback on the feature, and let others know that you are working on it.

**Important:** Always create your feature or hotfix against the `develop` branch, not `master`.
