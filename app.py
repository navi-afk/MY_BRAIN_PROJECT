import streamlit as st

# --- ページ設定 ---
st.set_page_config(page_title="bluearchive", layout="centered")

st.markdown("""
    <style>
    /* 1. 右上の GitHub メニュー一式を消す */
    .stAppToolbar {
        display: none !important;
    }

    /* 2. 右下の赤い王冠とカニのバーを消す */
    div[data-testid="stStatusWidget"], .viewerBadge_container__1QSob {
        display: none !important;
    }

    /* 3. 上部の余計なヘッダー（白い帯）を消す */
    header {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. パスワード認証機能 ---
def check_password():
    """合言葉が正しいかチェックする関数"""
    def password_entered():
        # ここの "1234" を好きな合言葉に変えてね！
        if st.session_state["password"] == "1234":
            st.session_state["password_correct"] = True
            del st.session_state["password"] 
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # 初回：パスワード入力画面を表示
        st.markdown("<h2 style='text-align: center; color: black; margin-top: 50px;'>認証が必要です</h2>", unsafe_allow_html=True)
        st.text_input("合言葉を入力してください", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # 失敗時：再入力
        st.text_input("合言葉が違います。もう一度入力してください", type="password", on_change=password_entered, key="password")
        st.error("😕 パスワードが正しくありません")
        return False
    else:
        # 成功
        return True

# パスワードが正解のときだけ以下のメイン処理を動かす
if check_password():

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

    # --- CSS (アプリ化に特化したUI) ---
    st.markdown(f"""
        <style>
        /* 背景固定 */
        html, body, [data-testid="stAppViewContainer"] {{
            background-color: #ffffff;
            overscroll-behavior: none;
        }}

        /* トップバー */
        .top-bar {{
            background-color: #ff8fa3; color: #ffffff; 
            padding-top: 15px; font-size: 18px; font-weight: bold; 
            position: fixed; top: 0; left: 0; width: 100%; 
            z-index: 10001; text-align: center; height: 50px;
        }}

        /* メインコンテンツ */
        .main-content {{
            position: absolute; top: 60px; left: 0; width: 100%;
            padding: 0 20px 150px 20px; display: block !important;
        }}

        /* 自作フッターメニュー */
        .custom-footer {{
            position: fixed; bottom: 0; left: 0; width: 100%; height: 85px;
            background-color: #ffffff; border-top: 1px solid #eeeeee;
            display: flex; justify-content: space-around; align-items: center;
            z-index: 10000;
            padding-bottom: env(safe-area-inset-bottom);
        }}
        
        .footer-item {{
            text-decoration: none; color: #888888; font-size: 10px;
            display: flex; flex-direction: column; align-items: center; flex: 1;
        }}
        .footer-item.active {{ color: #38bdf8; font-weight: bold; }}
        .footer-icon {{ font-size: 24px; margin-bottom: 2px; }}

        /* --- 不要な標準要素を消す（メニュー復活対策版） --- */
        header, [data-testid="stHeader"], [data-testid="stToolbar"] {{ display: none !important; }}
        /* 右下の赤いバッジ（ラベル）だけをピンポイントで隠す */
        div[data-testid="stStatusWidget"] {{ visibility: hidden; }}
        /* デフォルトのフッターを非表示にするが、自作メニューは消さないようにする */
        footer {{ display: none !important; }}
        
        /* 送信ボタンの枠線を消す（任意） */
        .stButton {{ display: block; }} /* ボタン自体はフォーム内で必要なので戻しました */
        </style>
        """, unsafe_allow_html=True)

    # --- 1. トップバー ---
    st.markdown(f'<div class="top-bar">{st.session_state["current_page"]}</div>', unsafe_allow_html=True)

    # --- 2. メインコンテンツ ---
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    if st.session_state['current_page'] == "ホーム":
        st.markdown("<h1 style='color:black; margin-top:0;'>Home</h1>", unsafe_allow_html=True)
        st.markdown("<div style='background:#fff9c4; padding:15px; border-radius:10px; color:#856404; margin:15px 0;'>COMING SOON...</div>", unsafe_allow_html=True)
        st.write("---")
        st.write("アプリ化に成功しました！ホーム画面から起動できます。")

    elif st.session_state['current_page'] == "メッセージ":
        st.markdown(f"<h2 style='color:black; margin-top:0;'>{st.session_state['partner_name']}</h2>", unsafe_allow_html=True)
        
        # チャット履歴の表示
        for msg in st.session_state['messages']:
            st.markdown(f'<div style="background:#e3f2fd; color:#0d47a1; padding:15px; border-radius:10px; margin-bottom:10px;">{msg}</div>', unsafe_allow_html=True)
        
        with st.form(key="chat_ui", clear_on_submit=True):
            u_msg = st.text_input("msg", placeholder="ここに入力", label_visibility="collapsed")
            if st.form_submit_button("送信") and u_msg:
                st.session_state['messages'].append(u_msg)
                st.rerun()

    elif st.session_state['current_page'] == "設定":
        st.markdown("<h1 style='color:black; margin-top:0;'>Settings</h1>", unsafe_allow_html=True)
        st.markdown("<b>相手の名前</b>", unsafe_allow_html=True)
        new_name = st.text_input("nm", value=st.session_state['partner_name'], label_visibility="collapsed")
        if new_name != st.session_state['partner_name']:
            st.session_state['partner_name'] = new_name
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # --- 3. フッター ---
    h_c = "active" if st.session_state['current_page'] == "ホーム" else ""
    m_c = "active" if st.session_state['current_page'] == "メッセージ" else ""
    s_c = "active" if st.session_state['current_page'] == "設定" else ""

    st.markdown(f"""
        <div class="custom-footer">
            <a href="/?p=ホーム" target="_self" class="footer-item {h_c}">
                <span class="footer-icon">🏠</span><span>ホーム</span>
            </a>
            <a href="/?p=メッセージ" target="_self" class="footer-item {m_c}">
                <span class="footer-icon">💬</span><span>メッセージ</span>
            </a>
            <a href="/?p=設定" target="_self" class="footer-item {s_c}">
                <span class="footer-icon">⚙️</span><span>設定</span>
            </a>
        </div>
        """, unsafe_allow_html=True)