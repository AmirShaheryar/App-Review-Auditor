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
