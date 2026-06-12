import pandas as pd
import numpy as np


class DataUtils:

    @staticmethod
    def clean_data(df):

        df = df.copy()

        df = df.drop_duplicates()

        df = df.fillna(
            method="ffill"
        )

        return df

    @staticmethod
    def calculate_returns(df):

        df = df.copy()

        df["Return"] = (
            df["Close"]
            .pct_change()
        )

        return df

    @staticmethod
    def add_basic_indicators(df):

        df = df.copy()

        df["MA20"] = (
            df["Close"]
            .rolling(20)
            .mean()
        )

        df["MA50"] = (
            df["Close"]
            .rolling(50)
            .mean()
        )

        df["Volatility"] = (
            df["Close"]
            .pct_change()
            .rolling(20)
            .std()
        )

        return df

    @staticmethod
    def normalize(series):

        return (
            series - series.min()
        ) / (
            series.max() - series.min()
        )