import streamlit as st

# --- ページ設定 ---
st.set_page_config(page_title="app", layout="centered")

# --- データの管理 ---
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "ホーム"
if 'partner_name' not in st.session_state:
    st.session_state['partner_name'] = "unknown"
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# URLパラメータでページ切り替え
params = st.query_params
if "p" in params:
    if params["p"] != st.session_state['current_page']:
        st.session_state['current_page'] = params["p"]
        st.rerun()

# --- CSS (UI調整) ---
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-color: #ffffff;
    }}

    /* トップバー */
    .top-bar {{
        background-color: #ff8fa3; 
        color: #ffffff !important; 
        padding-top: 12px;
        font-size: 18px; font-weight: bold; 
        position: fixed; top: 0; left: 0; width: 100%; 
        z-index: 10001; text-align: center; height: 50px;
    }}

    /* メインコンテンツ位置（赤枠の位置に固定） */
    .main-content {{
        position: absolute;
        top: 60px;
        left: 0; width: 100%;
        padding: 0 20px 150px 20px;
        display: block !important;
    }}

    /* 設定項目のスタイル */
    .setting-item {{
        background: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        color: black;
    }}

    /* フッター */
    .custom-footer {{
        position: fixed; bottom: 0; left: 0; width: 100%; height: 80px;
        background-color: #ffffff;
        display: flex; justify-content: space-around; align-items: center;
        border-top: 1px solid #eeeeee;
        z-index: 10000;
        padding-bottom: env(safe-area-inset-bottom);
    }}
    
    .footer-item {{
        text-decoration: none; color: #888888; font-size: 10px;
        display: flex; flex-direction: column; align-items: center; flex: 1;
    }}
    .footer-item.active {{ color: #38bdf8; font-weight: bold; }}
    .footer-icon {{ font-size: 22px; margin-bottom: 2px; }}

    header, [data-testid="stHeader"], [data-testid="stToolbar"] {{ display: none !important; }}
    [data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
    .stButton {{ display: none; }}
    </style>
    """, unsafe_allow_html=True)

# --- 1. トップバー ---
st.markdown(f'<div class="top-bar">{st.session_state["current_page"]}</div>', unsafe_allow_html=True)

# --- 2. メインコンテンツ ---
st.markdown('<div class="main-content">', unsafe_allow_html=True)

if st.session_state['current_page'] == "ホーム":
    st.markdown("<h1 style='color:black; margin-top:10px;'>Home</h1>", unsafe_allow_html=True)
    st.markdown("<div style='background:#fff9c4; padding:15px; border-radius:10px; color:#856404; margin:15px 0;'>COMING SOON...</div>", unsafe_allow_html=True)
    st.write("---")
    st.write("ようこそ！下のメニューから機能を選んでください。")

elif st.session_state['current_page'] == "メッセージ":
    st.markdown(f"<h2 style='color:black; margin-top:10px;'>{st.session_state['partner_name']}</h2>", unsafe_allow_html=True)
    if st.session_state['messages']:
        st.markdown(f'<div style="background:#e3f2fd; color:#0d47a1; padding:15px; border-radius:10px;">{st.session_state["messages"][-1]}</div>', unsafe_allow_html=True)
    
    with st.form(key="chat_ui", clear_on_submit=True):
        u_msg = st.text_input("メッセージを入力", placeholder="ここに入力", label_visibility="collapsed")
        if st.form_submit_button("送信") and u_msg:
            st.session_state['messages'].append(u_msg)
            st.rerun()

elif st.session_state['current_page'] == "ニュース":
    st.markdown("<h1 style='color:black; margin-top:10px;'>News</h1>", unsafe_allow_html=True)
    st.write("最新情報はありません。")

elif st.session_state['current_page'] == "設定":
    st.markdown("<h1 style='color:black; margin-top:10px;'>Settings</h1>", unsafe_allow_html=True)
    
    st.markdown('<div class="setting-item"><b>チャット相手の名前設定</b></div>', unsafe_allow_html=True)
    new_name = st.text_input("相手の名前を変更", value=st.session_state['partner_name'], label_visibility="collapsed")
    if new_name != st.session_state['partner_name']:
        st.session_state['partner_name'] = new_name
        st.rerun()
    
    st.markdown('<div class="setting-item" style="margin-top:20px;"><b>アプリについて</b></div>', unsafe_allow_html=True)
    st.write("Version 1.0.0")

st.markdown('</div>', unsafe_allow_html=True)

# --- 3. フッター ---
h_class = "active" if st.session_state['current_page'] == "ホーム" else ""
m_class = "active" if st.session_state['current_page'] == "メッセージ" else ""
n_class = "active" if st.session_state['current_page'] == "ニュース" else ""
s_class = "active" if st.session_state['current_page'] == "設定" else ""

st.markdown(f"""
    <div class="custom-footer">
        <a href="/?p=ホーム" target="_self" class="footer-item {h_class}">
            <span class="footer-icon">🏠</span><span>ホーム</span>
        </a>
        <a href="/?p=メッセージ" target="_self" class="footer-item {m_class}">
            <span class="footer-icon">💬</span><span>メッセージ</span>
        </a>
        <a href="/?p=ニュース" target="_self" class="footer-item {n_class}">
            <span class="footer-icon">📰</span><span>ニュース</span>
        </a>
        <div class="footer-item" style="opacity: 0.2;">
            <span class="footer-icon">🚫</span><span>Nothing</span>
        </div>
        <a href="/?p=設定" target="_self" class="footer-item {s_class}">
            <span class="footer-icon">⚙️</span><span>設定</span>
        </a>
    </div>
    """, unsafe_allow_html=True)