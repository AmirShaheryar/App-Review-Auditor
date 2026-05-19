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
def run_audit(app_id, app_name, count, time_filter):
    cutoff = None
    if time_filter == 'Last 7 Days':
        cutoff = datetime.now() - timedelta(days=7)
    elif time_filter == 'Last 30 Days':
        cutoff = datetime.now() - timedelta(days=30)
    elif time_filter == 'Last 90 Days':
        cutoff = datetime.now() - timedelta(days=90)

    with st.status(f'Auditing {app_name}...', expanded=True) as status:
        st.write('📡 Accessing Play Store...')
        all_data = []
        for score in [1, 2]:
            data, _ = reviews(app_id, lang='en', country='us', sort=Sort.NEWEST, count=count // 2, filter_score_with=score)
            all_data.extend(data)
        if cutoff:
            all_data = [r for r in all_data if r['at'] >= cutoff]
        all_data = sorted(all_data, key=lambda x: x['at'], reverse=True)[:count]
        if not all_data:
            status.update(label='No reviews found!', state='complete')
            return 'No reviews found.', []
        st.write(f'🧠 Llama 3 analyzing {len(all_data)} reviews...')
        review_text = '\n'.join([f'[ID:{i}] {r["content"]}' for i, r in enumerate(all_data)])
        prompt = f'Identify the 3 most frequent failures in these reviews for {app_name}. For each, provide a Direct Quote as evidence. Reviews: {review_text}'
        analysis = llm.invoke(prompt)
        status.update(label='Audit Complete!', state='complete')
        return analysis, all_data
with st.sidebar:
    st.header('Settings')
    sample_size = st.slider('Max Reviews', 10, 100, 50)
    time_filter = st.selectbox('Timeframe', ['All Time', 'Last 7 Days', 'Last 30 Days', 'Last 90 Days'])

query = st.text_input('Enter App Name or Package ID:')
if st.button('Generate Verified Audit'):
    if query:
        app_id, official_name = fetch_app_info(query)
        if app_id:
            report, raw_reviews = run_audit(app_id, official_name, sample_size, time_filter)
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader('🚩 AI Audit Findings')
                st.markdown(report)
            with col2:
                st.subheader('🔍 Source Truth')
                with st.expander('View Raw Data'):
                    for r in raw_reviews:
                        st.caption(f'{r["score"]}⭐')
                        st.write(r['content'])
                        st.divider()
            st.download_button('Download Report', report, file_name=f'{official_name}_audit.md')
        else:
            st.error('App not found.')
