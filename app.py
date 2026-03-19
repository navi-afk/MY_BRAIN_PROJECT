import streamlit as st

# 1. ページ基本設定
st.set_page_config(page_title="MomoTalk", page_icon="💬")

# 2. UIの見た目調整（CSS）
st.markdown("""
    <style>
    /* 右下のツールバーなどを非表示 */
    [data-testid="stToolbar"], .viewerBadge_container__1QSob, div[data-testid="stStatusWidget"] {
        display: none !important;
    }
    header { visibility: hidden; }
    
    /* 背景をブルアカ風の薄い水色に */
    .stApp { background-color: #F4F7F9; }

    /* タブの文字をアイコンっぽく大きく見せる設定 */
    .stTabs [data-baseweb="tab"] {
        font-size: 14px;
        font-weight: bold;
        color: #5DDEC9;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 合言葉機能
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    # 認証画面も少しオシャレに
    st.markdown("<h2 style='text-align: center; color: #FF69B4;'>Authentication</h2>", unsafe_allow_html=True)
    password = st.text_input("合言葉を入力してください", type="password")
    if password == "1234":
        st.session_state["password_correct"] = True
        st.rerun()
    else:
        st.stop()

# 4. メイン画面（タブメニュー）
# 絵文字の代わりに、少し特殊な記号を使って「アイコン感」を出します
tab1, tab2, tab3 = st.tabs(["⌂ Home", "✉ Message", "⚙ Settings"])

with tab1:
    st.markdown("<h3 style='color: #FF69B4;'>おかえりなさい、先生！</h3>", unsafe_allow_html=True)
    st.write("今日のスケジュールを確認しますか？")

with tab2:
    st.markdown("<h3 style='color: #5DDEC9;'>Messages</h3>", unsafe_allow_html=True)
    
    # チャットの入り口を作成
    c1, c2 = st.columns([1, 4])
    with c1:
        # ここはとりあえず標準の記号で代用
        st.markdown("<div style='font-size: 40px;'>👤</div>", unsafe_allow_html=True)
    with c2:
        st.write("**アロナ**")
        st.write("先生、お疲れ様です！新着メッセージがあります。")
    
    st.divider()
    # 送信フォームのテスト
    st.chat_input("アロナに返信する...")

with tab3:
    st.title("Settings")
    st.write("アプリの設定を変更できます。")