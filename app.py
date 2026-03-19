import streamlit as st

# 脳みそ（AI）が準備できているか確認
try:
    import google.generativeai as genai
    AI_READY = True
except:
    AI_READY = False

# ページ設定
st.set_page_config(page_title="MomoTalk", layout="centered")

# AIの初期設定
if AI_READY:
    genai.configure(api_key="AIzaSyBX62e_iQY6JKuYIZ9vgm_yd9_cruBoBc0")
    model = genai.GenerativeModel('gemini-1.5-flash')

# データの保存
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'partner' not in st.session_state:
    st.session_state['partner'] = "アロナ"

# URLパラメータ
params = st.query_params
page = params.get("p", "メッセージ")

# --- デザイン（CSS） ---
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{ background-color: #ffffff; }}
    
    /* トップバーをピンクに */
    .top-bar {{
        background-color: #ff8fa3; color: white !important;
        position: fixed; top: 0; left: 0; width: 100%; height: 50px;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; z-index: 10001;
    }}

    /* メイン画面の余白 */
    .chat-container {{
        padding: 60px 10px 120px 10px;
    }}

    /* メッセージの見た目（モモトーク風） */
    .bubble {{
        padding: 10px 15px; border-radius: 15px; margin-bottom: 10px;
        max-width: 80%; font-size: 14px; line-height: 1.4; color: black !important;
    }}
    .user-bubble {{
        background-color: #e3f2fd; margin-left: auto; border-bottom-right-radius: 2px;
    }}
    .ai-bubble {{
        background-color: #f0f2f6; margin-right: auto; border-bottom-left-radius: 2px;
    }}

    /* 入力フォームとボタンの修正 */
    div[data-testid="stForm"] {{
        border: none !important; padding: 0 !important;
    }}
    input {{
        color: black !important; background-color: #f9f9f9 !important;
    }}
    .stButton > button {{
        width: 100%; background-color: #ff8fa3 !important; color: white !important;
        border-radius: 10px; border: none; height: 45px; font-weight: bold;
    }}

    /* 下のメニュー */
    .footer {{
        position: fixed; bottom: 0; left: 0; width: 100%; height: 70px;
        background: white; border-top: 1px solid #eee;
        display: flex; justify-content: space-around; align-items: center; z-index: 10000;
    }}
    .footer a {{ text-decoration: none; color: #888; font-size: 11px; text-align: center; }}
    .footer a.active {{ color: #ff8fa3; font-weight: bold; }}

    header, [data-testid="stHeader"], [data-testid="stToolbar"] {{ display: none !important; }}
    </style>
    """, unsafe_allow_html=True)

# 1. トップバー
st.markdown(f'<div class="top-bar">{st.session_state["partner"]}</div>', unsafe_allow_html=True)

# 2. チャット表示エリア
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state['messages']:
    type_class = "user-bubble" if msg["role"] == "user" else "ai-bubble"
    st.markdown(f'<div class="bubble {type_class}">{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 3. 入力エリア
with st.container():
    st.markdown('<div style="position: fixed; bottom: 80px; left: 0; width: 100%; background: white; padding: 10px; z-index: 9999;">', unsafe_allow_html=True)
    with st.form(key="chat_form", clear_on_submit=True):
        u_input = st.text_input("メッセージを送信", placeholder="先生、お疲れ様です！", label_visibility="collapsed")
        submit = st.form_submit_button("送信")
        
        if submit and u_input:
            st.session_state['messages'].append({"role": "user", "content": u_input})
            
            # AI返信
            if AI_READY:
                try:
                    prompt = f"あなたは『ブルーアーカイブ』の{st.session_state['partner']}です。先生（ユーザー）に可愛く、短く1~2文で返信してください。返信対象: {u_input}"
                    response = model.generate_content(prompt)
                    st.session_state['messages'].append({"role": "assistant", "content": response.text})
                except:
                    st.session_state['messages'].append({"role": "assistant", "content": "（電波が悪いみたいです…）"})
            else:
                st.session_state['messages'].append({"role": "assistant", "content": "（AIをインストール中です…）"})
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 4. フッター
st.markdown(f"""
    <div class="footer">
        <a href="/?p=ホーム">🏠<br>ホーム</a>
        <a href="/?p=メッセージ" class="active">💬<br>メッセージ</a>
        <a href="/?p=設定">⚙️<br>設定</a>
    </div>
    """, unsafe_allow_html=True)