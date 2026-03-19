import streamlit as st

# 1. ページ基本設定（エラー回避のためシンプルに）
st.set_page_config(page_title="MomoTalk", page_icon="💬")

# 2. UIの見た目（極力シンプルにしてエラーを防ぐ）
st.markdown("""
    <style>
    /* 右下の王冠とメニューを消す */
    [data-testid="stToolbar"], .viewerBadge_container__1QSob, div[data-testid="stStatusWidget"] {
        display: none !important;
    }
    header { visibility: hidden; }
    
    /* 背景を白くして清潔感を出す */
    .stApp { background-color: #FFFFFF; }
    </style>
    """, unsafe_allow_html=True)

# 3. 合言葉機能（ここがバグると真っ白になります）
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    # ログイン画面のデザイン
    st.markdown("### 認証が必要です")
    password = st.text_input("合言葉を入力してください", type="password")
    if st.button("ログイン"):
        if password == "1234":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("合言葉が違います")
    st.stop()

# 4. メイン画面（画像を使わず、まずは文字だけで表示）
tab1, tab2, tab3 = st.tabs(["ホーム", "メッセージ", "設定"])

with tab1:
    st.header("Home")
    st.write("おかえりなさい、先生！")

with tab2:
    st.header("Message")
    st.write("アロナ：先生、お疲れ様です！")

with tab3:
    st.header("Settings")
    st.write("設定画面です。")