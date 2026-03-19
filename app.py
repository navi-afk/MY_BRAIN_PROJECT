import streamlit as st

# 1. ページ基本設定
st.set_page_config(page_title="MomoTalk", page_icon="💬", layout="centered")

# 2. UIの見た目（以前のピンクヘッダーとアイコン設定を復活）
st.markdown("""
    <style>
    /* 右下のツールバーなどを徹底的に隠す */
    [data-testid="stToolbar"], .viewerBadge_container__1QSob, div[data-testid="stStatusWidget"] {
        display: none !important;
    }
    header { visibility: hidden; }

    /* 背景色（薄い水色） */
    .stApp {
        background-color: #F4F7F9;
    }

    /* 上のピンクヘッダー */
    .custom-header {
        background-color: #FF69B4;
        padding: 10px;
        text-align: center;
        border-radius: 0 0 20px 20px;
        margin: -60px -20px 20px -20px;
    }
    .header-title {
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 20px;
    }

    /* 下のタブメニューのアイコンサイズ調整 */
    .nav-icon {
        width: 22px;
        height: 22px;
        margin-bottom: 2px;
    }
    
    /* タブの文字とアイコンを中央寄せ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        justify-content: center;
    }
    </style>
    
    <div class="custom-header">
        <div class="header-title">MomoTalk</div>
    </div>
    """, unsafe_allow_html=True)

# 3. 合言葉機能
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    password = st.text_input("合言葉を入力してください", type="password")
    if password == "1234":
        st.session_state["password_correct"] = True
        st.rerun()
    else:
        st.stop()

# 会話の記憶用
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. アイコン画像のURL
icon_home = "https://img.icons8.com/material-outlined/48/5DDEC9/home--v1.png"
icon_msg = "https://img.icons8.com/material-outlined/48/5DDEC9/filled-chat.png"
icon_settings = "https://img.icons8.com/material-outlined/48/5DDEC9/settings--v1.png"

# 5. タブメニュー（画像アイコン復活！）
tab1, tab2, tab3 = st.tabs([
    f'<div><img src="{icon_home}" class="nav-icon"><br>ホーム</div>',
    f'<div><img src="{icon_msg}" class="nav-icon"><br>メッセージ</div>',
    f'<div><img src="{icon_settings}" class="nav-icon"><br>設定</div>'
])

with tab1:
    st.markdown("<h4 style='color: #FF69B4;'>おかえりなさい、先生！</h4>", unsafe_allow_html=True)
    st.write("今日のシャーレも平和ですね。")

with tab2:
    # チャット画面
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("アロナにメッセージを送る"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # アロナの返答（アイコン付き）
        response = f"先生！『{prompt}』ですね。了解しました！"
        with st.chat_message("assistant", avatar="https://raw.githubusercontent.com/Arisaka-H/MomoTalk-Resource/main/arona_icon.png"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

with tab3:
    st.subheader("設定")
    st.write("開発中の設定項目です。")