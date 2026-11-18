import streamlit as st
import yfinance as yf
from groq import Groq

st.set_page_config(page_title="Predicta AI", page_icon="⚽")
st.title("⚽📈 Predicta AI")
st.caption("Football + Stock + Crypto - Free AI")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    ok = True
except:
    st.error("Add your Groq key in Streamlit Secrets!")
    ok = False

if ok:
    match = st.text_input("Football Match (e.g. Man City vs Arsenal)")
    ticker = st.text_input("Stock/Crypto (e.g. AAPL, BTC-USD, NVDA)", value="AAPL")

    if st.button("PREDICT NOW", type="primary"):
        if match:
            r = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role":"user","content":f"Predict football: {match}. Give score prediction, winner, confidence %, and brief analysis."}],
                temperature=0.7
            )
            st.success("⚽ FOOTBALL PREDICTION")
            st.write(r.choices[0].message.content)
        
        if ticker:
            data = yf.Ticker(ticker).history(period="1mo")
            st.line_chart(data['Close'])
            r2 = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role":"user","content":f"Stock/crypto analysis for {ticker}. Current price trend from chart. Give prediction for next 7 days, buy/sell/hold, and risk."}],
                temperature=0.7
            )
            st.success(f"📈 {ticker} ANALYSIS")
            st.write(r2.choices[0].message.content)
