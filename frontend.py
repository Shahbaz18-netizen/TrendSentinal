import streamlit as st
import requests
import json

# Set page title and icon
st.set_page_config(page_title="TrendSentinel AI", page_icon="🚀", layout="wide")

st.title("🚀 TrendSentinel: 24/7 YouTube Strategist")
st.markdown("---")

# Sidebar for configuration
st.sidebar.header("Settings")
backend_url = st.sidebar.text_input("Backend API URL", "http://127.0.0.1:8000/analyze/")

# Main Input
channel_url = st.text_input("Enter your YouTube Channel URL:", placeholder="https://www.youtube.com/@campusx-official")

if st.button("Generate Strategy Report"):
    if channel_url:
        # Placeholders: Inke andar hum data "fill" karenge jaise-jaise woh aayega
        status_text = st.empty()
        niche_container = st.empty()
        market_container = st.empty()
        
        st.header("📝 Daily AI Strategy Report")
        strategy_container = st.empty() # Typewriter effect yahan dikhega
        
        full_strategy = ""
        
        try:
            # 1. Use stream=True to keep the connection open
            with requests.post(backend_url, params={"channel_url": channel_url}, stream=True) as r:
                if r.status_code != 200:
                    st.error("Backend Engine Error!")
                    st.stop()

                # 2. Iterate over lines (chunks) from FastAPI
                for line in r.iter_lines():
                    if line:
                        # SSE format 'data: {...}' se JSON nikaalna
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith("data: "):
                            content = decoded_line.replace("data: ", "")
                            msg = json.loads(content)

                            # LOGIC: Check karke update karo UI ko
                            step = msg.get('step')

                            if step == 'context_found':
                                status_text.success(f"✅ Found: {msg['data']['title']}")
                            
                            elif step == 'niche_defined':
                                niche_container.info(f"🎯 **Identified Niche:** {msg['niche']}")
                            
                            elif step == 'market_data':
                                with market_container.expander("📊 Market Intelligence (Competitors Found)", expanded=False):
                                    for trend in msg['trends']:
                                        st.write(f"**Channel:** {trend['channel']}")
                                        for vid in trend['videos']:
                                            st.write(f"- [{vid['title']}]({vid['url']}) (`{vid['outperformance_score']}x`)")
                            
                            elif step == 'strategy_chunk':
                                # YAHAN HOTI HAI ASLI STREAMING 🚀
                                full_strategy += msg['content']
                                strategy_container.markdown(full_strategy + "▌") # Cursor effect

                # Final touch: Remove cursor once finished
                strategy_container.markdown(full_strategy)
                st.balloons()

        except Exception as e:
            st.error(f"Could not connect to backend: {e}")
    else:
        st.warning("Please enter a valid YouTube URL.")