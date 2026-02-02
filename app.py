import pandas as pd
 
 
def load_data():
    trades_df = pd.read_csv("data/trades.csv")
    holdings_df = pd.read_csv("data/holdings.csv")
    return trades_df, holdings_df
 
 
def fund_performance(holdings_df):
    if "PortfolioName" not in holdings_df.columns or "PL_YTD" not in holdings_df.columns:
        return pd.DataFrame()
 
    return (
        holdings_df
        .groupby("PortfolioName")["PL_YTD"]
        .sum()
        .reset_index()
        .sort_values(by="PL_YTD", ascending=False)
    )
 
 
 
def total_fees_by_fund(trades_df, fund):
    if "PortfolioName" not in trades_df.columns or "AllocationFees" not in trades_df.columns:
        return None
 
    return trades_df[trades_df["PortfolioName"] == fund]["AllocationFees"].sum()
 
 
 
def market_value_by_custodian(holdings_df, custodian):
    if "CustodianName" not in holdings_df.columns or "MV_Base" not in holdings_df.columns:
        return None
 
    return holdings_df[holdings_df["CustodianName"] == custodian]["MV_Base"].sum()
 
 
def pl_by_strategy(holdings_df, strategy):
    if "StrategyName" not in holdings_df.columns or "PL_YTD" not in holdings_df.columns:
        return None
 
    return holdings_df[holdings_df["StrategyName"] == strategy]["PL_YTD"].sum()
 