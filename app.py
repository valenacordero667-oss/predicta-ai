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
    st.error("Add your Groq key in Streamlit Secrets as GROQ_API_KEY")
    ok = False

if ok:
    match = st.text_input("Football Match (e.g. Man City vs Arsenal):")
    ticker = st.text_input("Stock/Crypto (e.g. AAPL, BTC-USD):", value="AAPL")
    
    if st.button("PREDICT NOW", type="primary"):
        if match:
            r = client.chat.completions.create(model="llama3-70b-8192", messages=[{"role":"user","content":f"Predict {match}. Give win %, score, confidence 0-100, risk"}])
            st.write(r.choices[0].message.content)
        if ticker:
            data = yf.Ticker(ticker).history(period="1mo")
            st.line_chart(data['Close'])
            r2 = client.chat.completions.create(model="llama3-70b-8192", messages=[{"role":"user","content":f"Analyze {ticker}. Recent: {data.tail().to_string()}. Give BUY/SELL/HOLD and confidence"}])
            st.write(r2.choices[0].message.content)
