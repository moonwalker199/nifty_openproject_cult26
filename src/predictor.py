import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


class StockPredictor:

    @staticmethod
    def compute_rsi(series, window=14):

        delta = series.diff()

        gain = delta.where(
            delta > 0,
            0
        )

        loss = -delta.where(
            delta < 0,
            0
        )

        avg_gain = (
            gain.rolling(window)
            .mean()
        )

        avg_loss = (
            loss.rolling(window)
            .mean()
        )

        rs = avg_gain / avg_loss

        rsi = (
            100 -
            (
                100 / (1 + rs)
            )
        )

        return rsi

    @staticmethod
    def create_features(df):

        data = df.copy()

        data["Return"] = (
            data["Close"]
            .pct_change()
        )

        data["MA_10"] = (
            data["Close"]
            .rolling(10)
            .mean()
        )

        data["MA_20"] = (
            data["Close"]
            .rolling(20)
            .mean()
        )

        data["Volatility"] = (
            data["Return"]
            .rolling(20)
            .std()
        )

        data["RSI"] = (
            StockPredictor
            .compute_rsi(
                data["Close"]
            )
        )

        data["Lag_1"] = (
            data["Close"]
            .shift(1)
        )

        data["Lag_2"] = (
            data["Close"]
            .shift(2)
        )

        data["Lag_3"] = (
            data["Close"]
            .shift(3)
        )

        data["Target"] = np.where(
            data["Close"].shift(-1)
            >
            data["Close"],
            1,
            0
        )

        data = data.dropna()

        return data

    @staticmethod
    def train(df):

        data = (
            StockPredictor
            .create_features(df)
        )

        features = [
            "Return",
            "MA_10",
            "MA_20",
            "Volatility",
            "RSI",
            "Lag_1",
            "Lag_2",
            "Lag_3"
        ]

        X = data[features]
        y = data["Target"]

        split = int(
            len(data) * 0.8
        )

        X_train = X[:split]
        X_test = X[split:]

        y_train = y[:split]
        y_test = y[split:]

        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            random_state=42
        )

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(
            X_test
        )

        metrics = {

            "Accuracy":
            accuracy_score(
                y_test,
                predictions
            ),

            "Precision":
            precision_score(
                y_test,
                predictions
            ),

            "Recall":
            recall_score(
                y_test,
                predictions
            ),

            "F1":
            f1_score(
                y_test,
                predictions
            )
        }

        return (
            model,
            metrics
        )

    @staticmethod
    def predict_next_day(
        model,
        df
    ):

        data = (
            StockPredictor
            .create_features(df)
        )

        latest = data.iloc[-1:]

        features = [
            "Return",
            "MA_10",
            "MA_20",
            "Volatility",
            "RSI",
            "Lag_1",
            "Lag_2",
            "Lag_3"
        ]

        prediction = model.predict(
            latest[features]
        )[0]

        probability = (
            model.predict_proba(
                latest[features]
            )[0]
        )

        return {
            "Prediction":
            "UP"
            if prediction == 1
            else "DOWN",

            "Confidence":
            round(
                max(probability)
                * 100,
                2
            )
        }