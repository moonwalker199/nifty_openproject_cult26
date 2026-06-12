from src.indicators import TechnicalIndicators
import pandas as pd

df = pd.read_csv("data/15/NIFTY50_all.csv")

stock = df[df["Symbol"] == "INFY"].copy()

stock = TechnicalIndicators.add_all_indicators(stock)

print(stock.tail())