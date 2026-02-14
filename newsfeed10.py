import os
import requests
import streamlit as st

st.set_page_config(page_title="Top News", layout="centered")
st.title("🗞️ Top 10 News")

API_KEY = os.getenv("NEWSDATA_API_KEY")
if not API_KEY:
    st.error("Missing API key. In Terminal run:\nexport NEWSDATA_API_KEY='YOUR_KEY'")
    st.stop()

# Build URL in the style you like
url = f"https://newsdata.io/api/1/latest?apikey={API_KEY}&language=en"
# Optional: uncomment if you want only “top” category
# url += "&category=top"

@st.cache_data(ttl=900)  # cache 15 minutes so you don't burn API calls
def fetch_news(u):
    r = requests.get(u, timeout=30)
    return r.json()

data = fetch_news(url)

if data.get("status") != "success":
    st.error("API error")
    st.write(data)
    st.stop()

articles = (data.get("results") or [])[:10]

for a in articles:
    title = a.get("title", "Untitled")
    link = a.get("link", "")
    source = a.get("source_id", "")
    pub = a.get("pubDate", "")

    st.markdown(f"**{title}**")
    st.caption(f"{pub} | {source}")
    if link:
        st.markdown(f"[Open article]({link})")
    st.divider()

