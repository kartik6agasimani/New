import streamlit as st
import pandas as pd
import re
from chatbot import (
    load_data,
    fund_performance,
    total_fees_by_fund,
    market_value_by_custodian,
    pl_by_strategy
)
 
st.set_page_config(page_title="Fund Data Chatbot")
st.title("Fund Data Chatbot")
 
trades_df, holdings_df = load_data()
 
 
ALL_COLUMNS = set(trades_df.columns.str.lower()) | set(holdings_df.columns.str.lower())
 
VALID_INTENTS = {
    "total", "count", "number",
    "sum", "fees", "market", "value",
    "profit", "loss", "pl", "perform",
    "trade", "holding", "strategy",
    "custodian", "fund", "show", "list"
}
 
def is_relevant(question):
    words = re.findall(r"\w+", question.lower())
    return any(word in ALL_COLUMNS or word in VALID_INTENTS for word in words)
 
 
question = st.text_input("Ask your question")
 
if question:
 
    q = question.lower()
 
 
    if not is_relevant(q):
        st.error("Sorry can not find the answer")
 
 
    elif "total number of holdings" in q:
        st.table(pd.DataFrame({"Total Holdings": [len(holdings_df)]}))
 
    elif "total number of trades" in q:
        st.table(pd.DataFrame({"Total Trades": [len(trades_df)]}))
 
    elif "show all trades" in q:
        st.dataframe(trades_df)
 
    elif "list holdings" in q:
        st.dataframe(holdings_df)
 
    elif "first 20 trades" in q:
        st.dataframe(trades_df.head(20))
 
    elif "first 20 holdings" in q:
        st.dataframe(holdings_df.head(20))
 
 
    elif "performed better" in q or "yearly profit and loss" in q:
        result = fund_performance(holdings_df)
        if result.empty:
            st.error("Sorry can not find the answer")
        else:
            st.dataframe(result)
 
 
    elif "total amount of fees" in q:
        fund = trades_df["PortfolioName"].iloc[0]
        fees = total_fees_by_fund(trades_df, fund)
        st.table(pd.DataFrame({"Total Fees": [fees]}))
 
  
    elif "market value" in q and "custodian" in q:
        custodian = holdings_df["CustodianName"].iloc[0]
        mv = market_value_by_custodian(holdings_df, custodian)
        st.table(pd.DataFrame({"Total Market Value": [mv]}))
 
 
    elif "sum of all profit and loss" in q and "strategy" in q:
        strategy = holdings_df["StrategyName"].iloc[0]
        total_pl = pl_by_strategy(holdings_df, strategy)
        st.table(pd.DataFrame({"Total P&L": [total_pl]}))
 
    else:
        st.error("Sorry can not find the answer")