import pandas as pd
import numpy as np


class PortfolioBuilder:

    @staticmethod
    def calculate_returns(price_df):
        """
        Daily returns matrix
        """

        returns = (
            price_df
            .pct_change()
            .dropna()
        )

        return returns

    @staticmethod
    def annual_return(returns):
        return returns.mean() * 252

    @staticmethod
    def annual_covariance(returns):
        return returns.cov() * 252

    @staticmethod
    def portfolio_performance(
        weights,
        mean_returns,
        cov_matrix
    ):

        expected_return = np.sum(
            mean_returns * weights
        )

        volatility = np.sqrt(
            np.dot(
                weights.T,
                np.dot(
                    cov_matrix,
                    weights
                )
            )
        )

        return (
            expected_return,
            volatility
        )

    @staticmethod
    def sharpe_score(
        expected_return,
        volatility,
        risk_free_rate=0.05
    ):

        if volatility == 0:
            return 0

        return (
            expected_return
            - risk_free_rate
        ) / volatility

    @staticmethod
    def generate_profile_portfolio(
        price_df,
        profile="balanced"
    ):

        returns = (
            PortfolioBuilder
            .calculate_returns(
                price_df
            )
        )

        mean_returns = (
            PortfolioBuilder
            .annual_return(
                returns
            )
        )

        volatility = (
            returns.std()
            * np.sqrt(252)
        )

        stock_scores = pd.DataFrame({
            "Return": mean_returns,
            "Volatility": volatility
        })

        # Conservative
        if profile.lower() == "conservative":

            selected = (
                stock_scores
                .sort_values(
                    "Volatility"
                )
                .head(5)
            )

        # Aggressive
        elif profile.lower() == "aggressive":

            selected = (
                stock_scores
                .sort_values(
                    "Return",
                    ascending=False
                )
                .head(5)
            )

        # Balanced
        else:

            stock_scores["Score"] = (
                stock_scores["Return"]
                /
                stock_scores["Volatility"]
            )

            selected = (
                stock_scores
                .sort_values(
                    "Score",
                    ascending=False
                )
                .head(5)
            )

        weights = np.repeat(
            1 / len(selected),
            len(selected)
        )

        portfolio = pd.DataFrame({
            "Stock":
            selected.index,
            "Weight":
            weights,
            "Expected_Return":
            selected["Return"].values,
            "Volatility":
            selected["Volatility"].values
        })

        return portfolio

    @staticmethod
    def portfolio_summary(
        portfolio,
        price_df
    ):

        selected_stocks = (
            portfolio["Stock"]
            .tolist()
        )

        weights = (
            portfolio["Weight"]
            .values
        )

        returns = (
            price_df[selected_stocks]
            .pct_change()
            .dropna()
        )

        mean_returns = (
            returns.mean()
            * 252
        )

        cov_matrix = (
            returns.cov()
            * 252
        )

        exp_return, vol = (
            PortfolioBuilder
            .portfolio_performance(
                weights,
                mean_returns,
                cov_matrix
            )
        )

        sharpe = (
            PortfolioBuilder
            .sharpe_score(
                exp_return,
                vol
            )
        )

        return {
            "Expected Annual Return":
            round(exp_return, 4),

            "Annual Volatility":
            round(vol, 4),

            "Sharpe Ratio":
            round(sharpe, 4)
        }