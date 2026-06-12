import pandas as pd
import numpy as np


class RiskAnalyzer:

    @staticmethod
    def annualized_volatility(returns):
        """
        Annualized Volatility
        """
        return returns.std() * np.sqrt(252)

    @staticmethod
    def sharpe_ratio(returns, risk_free_rate=0.05):
        """
        Annualized Sharpe Ratio
        """

        annual_return = returns.mean() * 252
        annual_vol = returns.std() * np.sqrt(252)

        if annual_vol == 0:
            return 0

        return (annual_return - risk_free_rate) / annual_vol

    @staticmethod
    def sortino_ratio(returns, risk_free_rate=0.05):
        """
        Sortino Ratio
        """

        downside_returns = returns[returns < 0]

        downside_std = (
            downside_returns.std()
            * np.sqrt(252)
        )

        annual_return = returns.mean() * 252

        if downside_std == 0:
            return 0

        return (
            annual_return - risk_free_rate
        ) / downside_std

    @staticmethod
    def max_drawdown(close_prices):
        """
        Maximum Drawdown
        """

        cumulative = (
            close_prices /
            close_prices.iloc[0]
        )

        rolling_max = cumulative.cummax()

        drawdown = (
            cumulative - rolling_max
        ) / rolling_max

        return drawdown.min()

    @staticmethod
    def risk_adjusted_return(returns):
        """
        Return / Volatility
        """

        vol = returns.std()

        if vol == 0:
            return 0

        return returns.mean() / vol

    @staticmethod
    def beta(stock_returns, market_returns):
        """
        Beta Analysis

        Beta > 1:
            More volatile than market

        Beta < 1:
            Less volatile than market
        """

        aligned = pd.concat(
            [stock_returns, market_returns],
            axis=1
        ).dropna()

        aligned.columns = [
            "stock",
            "market"
        ]

        covariance = np.cov(
            aligned["stock"],
            aligned["market"]
        )[0][1]

        market_variance = np.var(
            aligned["market"]
        )

        if market_variance == 0:
            return 0

        return covariance / market_variance

    @staticmethod
    def calculate_all_metrics(
        stock_df,
        market_returns=None
    ):
        """
        Complete Risk Analysis
        """

        returns = (
            stock_df["Close"]
            .pct_change()
            .dropna()
        )
        cumulative = (
                    1 + returns
                        ).cumprod()

        running_max = (
        cumulative.cummax()
)

        drawdown = (
        cumulative - running_max
        ) / running_max

        max_drawdown = drawdown.min()
        metrics = {}

        metrics["Annual_Return"] = (
            returns.mean() * 252
        )

        metrics["Volatility"] = (
            RiskAnalyzer
            .annualized_volatility(
                returns
            )
        )

        metrics["Sharpe_Ratio"] = (
            RiskAnalyzer
            .sharpe_ratio(
                returns
            )
        )

        metrics["Sortino_Ratio"] = (
            RiskAnalyzer
            .sortino_ratio(
                returns
            )
        )

        metrics["Max_Drawdown"] = (
            RiskAnalyzer
            .max_drawdown(
                stock_df["Close"]
            )
        )

        metrics["Risk_Adjusted_Return"] = (
            RiskAnalyzer
            .risk_adjusted_return(
                returns
            )
        )

        if market_returns is not None:

            metrics["Beta"] = (
                RiskAnalyzer.beta(
                    returns,
                    market_returns
                )
            )

        return metrics
    

    