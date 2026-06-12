import pandas as pd
import numpy as np


class TechnicalIndicators:

    @staticmethod
    def add_returns(df):
        """
        Daily percentage returns
        """
        df["Return"] = df["Close"].pct_change()
        return df

    @staticmethod
    def add_log_returns(df):
        """
        Log returns
        """
        df["Log_Return"] = np.log(df["Close"] / df["Close"].shift(1))
        return df

    @staticmethod
    def add_sma(df, window=20):
        """
        Simple Moving Average
        """
        df[f"SMA_{window}"] = (
            df["Close"]
            .rolling(window=window)
            .mean()
        )
        return df

    @staticmethod
    def add_ema(df, window=20):
        """
        Exponential Moving Average
        """
        df[f"EMA_{window}"] = (
            df["Close"]
            .ewm(span=window, adjust=False)
            .mean()
        )
        return df

    @staticmethod
    def add_rsi(df, period=14):
        """
        Relative Strength Index
        """

        delta = df["Close"].diff()

        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()

        rs = avg_gain / avg_loss

        df["RSI"] = 100 - (100 / (1 + rs))

        return df

    @staticmethod
    def add_macd(df):
        """
        MACD Indicator
        """

        ema12 = df["Close"].ewm(
            span=12,
            adjust=False
        ).mean()

        ema26 = df["Close"].ewm(
            span=26,
            adjust=False
        ).mean()

        df["MACD"] = ema12 - ema26

        df["MACD_Signal"] = (
            df["MACD"]
            .ewm(span=9, adjust=False)
            .mean()
        )

        return df

    @staticmethod
    def add_bollinger_bands(
        df,
        window=20
    ):
        """
        Bollinger Bands
        """

        sma = (
            df["Close"]
            .rolling(window)
            .mean()
        )

        std = (
            df["Close"]
            .rolling(window)
            .std()
        )

        df["BB_Middle"] = sma
        df["BB_Upper"] = sma + (2 * std)
        df["BB_Lower"] = sma - (2 * std)

        return df

    @staticmethod
    def add_volatility(
        df,
        window=20
    ):
        """
        Rolling Volatility
        """

        df["Volatility"] = (
            df["Return"]
            .rolling(window)
            .std()
        )

        return df

    @staticmethod
    def add_momentum(
        df,
        period=10
    ):
        """
        Price Momentum
        """

        df["Momentum"] = (
            df["Close"] -
            df["Close"].shift(period)
        )

        return df

    @staticmethod
    def add_all_indicators(df):
        """
        Master function
        """

        df = df.copy()

        df = TechnicalIndicators.add_returns(df)

        df = TechnicalIndicators.add_log_returns(df)

        df = TechnicalIndicators.add_sma(df, 20)
        df = TechnicalIndicators.add_sma(df, 50)

        df = TechnicalIndicators.add_ema(df, 20)
        df = TechnicalIndicators.add_ema(df, 50)

        df = TechnicalIndicators.add_rsi(df)

        df = TechnicalIndicators.add_macd(df)

        df = TechnicalIndicators.add_bollinger_bands(df)

        df = TechnicalIndicators.add_volatility(df)

        df = TechnicalIndicators.add_momentum(df)

        return df