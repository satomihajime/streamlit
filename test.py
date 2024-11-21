import streamlit as st
import requests

# Streamlit アプリの設定
st.title("業者一覧管理アプリ")
st.markdown("以下の表で業者データを表示します。")

# APIの設定
BASE_URL = "https://kdwapi.kendweb.cloud/v1/api/MstGyosya"
HEADERS = {
    "accept": "*/*",
    "X-API-KEY": st.secrets["api"]["key"], 
    "X-API-USERKEY": st.secrets["api"]["userkey"], 
    "X-DB": st.secrets["api"]["db"] 
}

# デバッグ出力用関数
def log_debug_response(response):
    st.write("### デバッグ情報")
    st.text("Request Headers:")
    st.json(dict(response.request.headers))
    st.text("Response Headers:")
    st.json(dict(response.headers))
    st.text("Response Content:")
    st.text(response.text)

def log_debug_info(text):
    st.write("### デバッグ情報")
    st.text(text)

# データ取得関数
@st.cache_data
def fetch_gyosha_list(fields=None):
    try:
        # パラメータの動的生成
        params = ""
        if fields:
            params = "&".join([f"fields={field}" for field in fields])

        # APIリクエスト送信
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        response.raise_for_status()  # ステータスコードが200以外の場合例外を発生
        #log_debug_response(response)  # デバッグ情報を出力
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"データの取得に失敗しました: {e}")
        log_debug_response(response)  # デバッグ情報を表示
        return {}

# データ取得
fields = ["mgyID", "Shiirecd", "mgyRyakuName"]  # 必要なフィールドを指定
data = fetch_gyosha_list(fields)

# データ表示
if data:
    st.write("### 取得データ")
    st.json(data)
else:
    st.info("業者データが見つかりませんでした。")
