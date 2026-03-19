import streamlit as st

# --- 1. ページ基本設定 ---
st.set_page_config(page_title="app", layout="centered")

# --- 2. データの管理（UIの土台を維持） ---
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "ホーム"
if 'partner_name' not in st.session_state:
    st.session_state['partner_name'] = "アロナ"
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# URLパラメータでページ切り替え
params = st.query_params
if "p" in params:
    if params["p"] != st.session_state['current_page']:
        st.session_state['current_page'] = params["p"]
        st.rerun()

# --- 3. CSS (あなたのデザインを維持) ---
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{ background-color: #ffffff; }}
    .top-bar {{
        background-color: #ff8fa3; color: #ffffff !important; 
        padding-top: 12px; font-size: 18px; font-weight: bold; 
        position: fixed; top: 0; left: 0; width: 100%; 
        z-index: 10001; text-align: center; height: 50px;
    }}
    .main-content {{
        position: absolute; top: 60px; left: 0; width: 100%;
        padding: 0 20px 150px 20px; display: block !important;
    }}
    .custom-footer {{
        position: fixed; bottom: 0; left: 0; width: 100%; height: 80px;
        background-color: #ffffff; display: flex; justify-content: space-around; 
        align-items: center; border-top: 1px solid #eeeeee; z-index: 10000;
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

# --- 4. トップバー表示 ---
st.markdown(f'<div class="top-bar">{st.session_state["current_page"]}</div>', unsafe_allow_html=True)

# --- 5. メインコンテンツ ---
st.markdown('<div class="main-content">', unsafe_allow_html=True)

if st.session_state['current_page'] == "ホーム":
    st.markdown("<h1 style='color:black; margin-top:10px;'>Home</h1>", unsafe_allow_html=True)
    st.write("おかえりなさい、先生！")

elif st.session_state['current_page'] == "メッセージ":
    st.markdown(f"<h2 style='color:black; margin-top:10px;'>{st.session_state['partner_name']}</h2>", unsafe_allow_html=True)
    
    for msg in st.session_state['messages']:
        bg = "#e3f2fd" if msg["role"] == "user" else "#f0f2f6"
        align = "right" if msg["role"] == "user" else "left"
        margin = "margin-left: 15%;" if msg["role"] == "user" else "margin-right: 15%;"
        st.markdown(f'<div style="background:{bg}; color:black; padding:12px; border-radius:15px; margin-bottom:8px; text-align:{align}; {margin}">{msg["content"]}</div>', unsafe_allow_html=True)

    with st.form(key="chat_ui", clear_on_submit=True):
        u_msg = st.text_input("メッセージを入力", placeholder="ここに入力", label_visibility="collapsed")
        if st.form_submit_button("送信") and u_msg:
            st.session_state['messages'].append({"role": "user", "content": u_msg})
            # 簡易返信（一旦AIなし）
            st.session_state['messages'].append({"role": "assistant", "content": f"{u_msg}ですね！"})
            st.rerun()

elif st.session_state['current_page'] == "設定":
    st.markdown("<h1 style='color:black; margin-top:10px;'>Settings</h1>", unsafe_allow_html=True)
    new_name = st.text_input("相手の名前を変更", value=st.session_state['partner_name'])
    if new_name != st.session_state['partner_name']:
        st.session_state['partner_name'] = new_name
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# --- 6. フッター ---
h_class = "active" if st.session_state['current_page'] == "ホーム" else ""
m_class = "active" if st.session_state['current_page'] == "メッセージ" else ""
s_class = "active" if st.session_state['current_page'] == "設定" else ""

st.markdown(f"""
    <div class="custom-footer">
        <a href="/?p=ホーム" target="_self" class="footer-item {h_class}">
            <span class="footer-icon">🏠</span><span>ホーム</span>
        </a>
        <a href="/?p=メッセージ" target="_self" class="footer-item {m_class}">
            <span class="footer-icon">💬</span><span>メッセージ</span>
        </a>
        <a href="/?p=設定" target="_self" class="footer-item {s_class}">
            <span class="footer-icon">⚙️</span><span>設定</span>
        </a>
    </div>
    """, unsafe_allow_html=True)