import pandas as pd


class ExplainabilityEngine:

    @staticmethod
    def trend_explanation(stock_df):

        ma20 = (
            stock_df["Close"]
            .rolling(20)
            .mean()
            .iloc[-1]
        )

        ma50 = (
            stock_df["Close"]
            .rolling(50)
            .mean()
            .iloc[-1]
        )

        if ma20 > ma50:

            return (
                "Bullish trend detected because "
                "20-day Moving Average is above "
                "50-day Moving Average."
            )

        return (
            "Bearish trend detected because "
            "20-day Moving Average is below "
            "50-day Moving Average."
        )

    @staticmethod
    def risk_explanation(risk_metrics):

        beta = risk_metrics["Beta"]

        if beta > 1:

            return (
                "Higher market sensitivity "
                "(Beta > 1)."
            )

        return (
            "Lower market sensitivity "
            "(Beta < 1)."
        )

    @staticmethod
    def prediction_explanation(prediction):

        if prediction["Prediction"] == "UP":

            return (
                "Model expects positive "
                "price movement."
            )

        return (
            "Model expects negative "
            "price movement."
        )