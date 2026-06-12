import streamlit as st
import pandas as pd
import plotly.express as px

from src.predictor import StockPredictor
from src.portfolio import PortfolioBuilder
from src.risk import RiskAnalyzer
from src.utils import DataUtils
from src.explainability import ExplainabilityEngine


st.set_page_config(
    page_title="InvestIQ",
    layout="wide"
)

st.title("InvestIQ")
st.subheader("AI-Powered Investment Intelligence Platform")


@st.cache_data
def load_data():
    df = pd.read_csv("data/15/NIFTY50_all.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df


df = DataUtils.clean_data(
    load_data()
)


stocks = sorted(df["Symbol"].unique())

selected_stock = st.sidebar.selectbox(
    "Select Stock",
    stocks
)

stock_df = (
    df[df["Symbol"] == selected_stock]
    .sort_values("Date")
)

stock_df = DataUtils.clean_data(stock_df)


st.header("Stock Overview")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Latest Close",
        round(stock_df["Close"].iloc[-1], 2)
    )

with col2:
    st.metric(
        "Records",
        len(stock_df)
    )

st.line_chart(stock_df.set_index("Date")[["Close"]])


st.header("Stock Predictor Engine")

model, metrics = StockPredictor.train(stock_df)

prediction = StockPredictor.predict_next_day(model, stock_df)

c1, c2 = st.columns(2)

with c1:
    st.success(f"Prediction: {prediction['Prediction']}")

with c2:
    st.info(f"Confidence: {prediction['Confidence']}%")

st.subheader("Model Performance")
st.write(metrics)

#
st.header("Risk Assessment")

market = df.groupby("Date")["Close"].mean()
market_returns = market.pct_change().dropna()

risk_metrics = RiskAnalyzer.calculate_all_metrics(stock_df, market_returns)

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric("Volatility", round(risk_metrics["Volatility"], 3))
c2.metric("Sharpe", round(risk_metrics["Sharpe_Ratio"], 3))
c3.metric("Sortino", round(risk_metrics["Sortino_Ratio"], 3))
c4.metric("Beta", round(risk_metrics["Beta"], 3))
c5.metric(
    "Max Drawdown",
    round(
        risk_metrics[
            "Max_Drawdown"
        ],
        3
    )
)

st.header(
    "Market Anomaly Detection"
)

returns = (
    stock_df["Close"]
    .pct_change()
    .dropna()
)

anomalies = returns[
    abs(
        returns -
        returns.mean()
    ) > (
        3 * returns.std()
    )
]

st.metric(
    "Anomalies Detected",
    len(anomalies)
)

if len(anomalies) > 0:

    anomaly_df = pd.DataFrame({
        "Date": anomalies.index,
        "Return": anomalies.values
    })

    st.dataframe(
        anomaly_df.tail(10)
    )

    st.warning(
        "Extreme market movements detected."
    )

else:

    st.success(
        "No major anomalies detected."
    )


st.header("Portfolio Construction")

profile = st.selectbox(
    "Investor Profile",
    ["conservative", "balanced", "aggressive"]
)

price_matrix = df.pivot_table(
    index="Date",
    columns="Symbol",
    values="Close"
)

portfolio = PortfolioBuilder.generate_profile_portfolio(price_matrix, profile)

st.subheader("Recommended Portfolio")
st.dataframe(portfolio)

fig = px.pie(
    portfolio,
    names="Stock",
    values="Weight",
    title="Portfolio Allocation"
)

st.plotly_chart(fig, use_container_width=True)

summary = PortfolioBuilder.portfolio_summary(portfolio, price_matrix)

st.subheader("Portfolio Summary")
st.write(summary)


st.header("Investment Insights")



volatility = risk_metrics["Volatility"]
sharpe = risk_metrics["Sharpe_Ratio"]
beta = risk_metrics["Beta"]

if sharpe > 1:
    st.success("Strong risk-adjusted performance.")
elif sharpe > 0.5:
    st.info("Moderate risk-adjusted performance.")
else:
    st.warning("Weak risk-adjusted performance.")

if beta > 1:
    st.warning("Stock is more volatile than market.")
else:
    st.success("Stock is less volatile than market.")

if volatility > 0.4:
    st.warning("High historical risk detected.")
else:
    st.success("Risk level appears manageable.")

st.subheader("Investment Recommendation")

if risk_metrics["Sharpe_Ratio"] > 1 and prediction["Prediction"] == "UP":
    st.success("BUY: Strong risk-adjusted performance with positive forecast.")
elif risk_metrics["Sharpe_Ratio"] > 0.5:
    st.info("HOLD: Moderate return potential.")
else:
    st.warning("AVOID: Weak historical performance and risk profile.")
st.header("Explainable AI")

trend_exp = ExplainabilityEngine.trend_explanation(
    stock_df
)

risk_exp = ExplainabilityEngine.risk_explanation(
    risk_metrics
)

st.subheader("Trend Explanation")
st.write(trend_exp)

st.subheader("Risk Explanation")
st.write(risk_exp)

prediction_reason = (
    ExplainabilityEngine.prediction_explanation(
        prediction
    )
)

st.info(prediction_reason)

st.header("Portfolio Risk Profile")

portfolio_volatility = summary["Annual Volatility"]

if portfolio_volatility < 0.15:
    st.success("Low Risk Portfolio")
elif portfolio_volatility < 0.25:
    st.info("Moderate Risk Portfolio")
else:
    st.warning("High Risk Portfolio")