import streamlit as st
from datetime import datetime, timedelta
from google_play_scraper import Sort, reviews, search
from langchain_ollama import OllamaLLM

st.set_page_config(page_title='Verified AI Auditor', page_icon='🕵️', layout='wide')
st.title('🕵️ App Review Auditor (with Verification)')
st.markdown('Analyze real-world user frustrations using **Llama 3** with evidence tracking.')

llm = OllamaLLM(model='llama3')

KNOWN_APPS = {
    'whatsapp': 'com.whatsapp',
    'instagram': 'com.instagram.android',
    'facebook': 'com.facebook.katana',
    'tiktok': 'com.zhiliaoapp.musically',
    'youtube': 'com.google.android.youtube',
    'snapchat': 'com.snapchat.android',
    'twitter': 'com.twitter.android',
    'x': 'com.twitter.android',
    'spotify': 'com.spotify.music',
    'netflix': 'com.netflix.mediaclient',
    'uber': 'com.ubercabs',
    'gmail': 'com.google.android.gm',
}
def fetch_app_info(user_query):
    query_clean = user_query.strip().lower()
    if '.' in user_query and ' ' not in user_query:
        return user_query.strip(), user_query.strip()
    if query_clean in KNOWN_APPS:
        return KNOWN_APPS[query_clean], user_query.title()
    try:
        results = search(query_clean, n_hits=1, lang='en', country='us')
        if results:
            return results[0]['appId'], results[0]['title']
    except Exception as e:
        st.error(f'Search failed: {e}')
    return None, None
