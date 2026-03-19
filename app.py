import streamlit as st
import google.generativeai as genai

# --- 1. AIの設定 (インデントエラーを修正済み) ---
# 先ほど取得したキーをここに設定しています
genai.configure(api_key="AIzaSyDFpXPq6bwT211cqiVz9f-YyEQqIKB5zus") 
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. ページ設定とデザイン ---
st.set_page_config(page_title="シッテムの箱", layout="centered")

st.markdown("""
    <style>
    /* 全体の背景を白に */
    [data-testid="stAppViewContainer"] { background-color: #ffffff; }
    
    /* テキストの色を黒に固定 */
    .main-content, h1, h2, p, span, div { color: #1a1a1a !important; }

    /* ヘッダーのデザイン */
    .top-bar {
        background-color: #ff8fa3;
        color: white !important;
        padding: 10px;
        text-align: center;
        font-weight: bold;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 1000;
    }
    
    /* チャットエリアの余白 */
    .chat-container { padding-top: 60px; padding-bottom: 100px; }

    /* 送信ボタンをピンクに */
    div[data-testid="stForm"] button {
        background-color: #ff8fa3 !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        width: 100%;
    }

    /* デフォルトのヘッダーを非表示 */
    header, [data-testid="stHeader"] { display: none !important; }
    </style>
    <div class="top-bar">メッセージ</div>
    """, unsafe_allow_html=True)

# --- 3. データの管理 ---
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# --- 4. メイン画面 ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
st.write("## アロナ")

# 会話の表示
for msg in st.session_state['messages']:
    align = "right" if msg["role"] == "user" else "left"
    bg = "#e3f2fd" if msg["role"] == "user" else "#f1f3f4"
    st.markdown(f'''
        <div style="text-align: {align}; margin-bottom: 10px;">
            <span style="background-color: {bg}; padding: 10px 15px; border-radius: 15px; display: inline-block; max-width: 80%; color: black;">
                {msg["content"]}
            </span>
        </div>
    ''', unsafe_allow_html=True)

# 入力フォーム
with st.form(key="chat_form", clear_on_submit=True):
    u_input = st.text_input("", placeholder="メッセージを入力してください", label_visibility="collapsed")
    submit = st.form_submit_button("送信")
    
    if submit and u_input:
        # ユーザーのメッセージを追加
        st.session_state['messages'].append({"role": "user", "content": u_input})
        
        # AIに返信させる
        try:
            # アロナとしてのキャラ設定を追加
            prompt = f"あなたは『ブルーアーカイブ』のアロナです。先生（ユーザー）に対して、1~2文で可愛く、親しみやすく返信してください。返信対象: {u_input}"
            response = model.generate_content(prompt)
            st.session_state['messages'].append({"role": "assistant", "content": response.text})
        except Exception:
            st.session_state['messages'].append({"role": "assistant", "content": "（通信エラーです、先生…）"})
        
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)