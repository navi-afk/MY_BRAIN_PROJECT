import streamlit as st

# ここで正しく読み込めるか再試行します
try:
    import google.generativeai as genai
    AI_READY = True
except ImportError:
    AI_READY = False

# --- 基本設定 ---
st.set_page_config(page_title="app", layout="centered")

if AI_READY:
    # あなたのAPIキーをセット
    genai.configure(api_key="AIzaSyBX62e_iQY6JKuYIZ9vgm_yd9_cruBoBc0")
    model = genai.GenerativeModel('gemini-1.5-flash')

# データの初期化
if 'partner_name' not in st.session_state: st.session_state['partner_name'] = "アロナ"
if 'messages' not in st.session_state: st.session_state['messages'] = []

# --- デザイン (文字色修正) ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #ffffff; }
    .main-content, h1, h2, p, span, div { color: #1a1a1a !important; }
    .top-bar {
        background-color: #ff8fa3; color: white !important;
        position: fixed; top: 0; left: 0; width: 100%; height: 50px;
        text-align: center; line-height: 50px; font-weight: bold; z-index: 1000;
    }
    .main-content { padding-top: 60px; padding-bottom: 100px; }
    div[data-testid="stForm"] button {
        background-color: #ff8fa3 !important; color: white !important;
        border-radius: 20px; width: 100%; border: none;
    }
    header, [data-testid="stHeader"] { display: none !important; }
    </style>
    <div class="top-bar">メッセージ</div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-content">', unsafe_allow_html=True)
st.markdown(f"## {st.session_state['partner_name']}")

# 履歴表示
for msg in st.session_state['messages']:
    bg = "#e3f2fd" if msg["role"] == "user" else "#f0f2f6"
    align = "right" if msg["role"] == "user" else "left"
    st.markdown(f'<div style="background:{bg}; padding:12px; border-radius:15px; margin-bottom:8px; text-align:{align};">{msg["content"]}</div>', unsafe_allow_html=True)

# 入力欄
with st.form(key="chat", clear_on_submit=True):
    u_msg = st.text_input("", placeholder="メッセージを入力", label_visibility="collapsed")
    if st.form_submit_button("送信") and u_msg:
        st.session_state['messages'].append({"role": "user", "content": u_msg})
        if AI_READY:
            try:
                prompt = f"あなたは『ブルーアーカイブ』の{st.session_state['partner_name']}です。先生に可愛く返信して。メッセージ: {u_msg}"
                res = model.generate_content(prompt)
                ai_text = res.text
            except: ai_text = "（通信エラーです…）"
        else:
            ai_text = "（ライブラリの読み込みに失敗しています。インタープリターを確認してください）"
        st.session_state['messages'].append({"role": "assistant", "content": ai_text})
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)