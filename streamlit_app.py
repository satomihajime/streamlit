import streamlit as st
import requests
import pandas as pd

# Streamlit アプリの設定
st.title("業者一覧管理アプリ")
st.markdown("以下の表で業者データを表示します。")

# APIの設定
BASE_URL = "https://kdwapi.kendweb.cloud/v1/api/MstGyosya"
HEADERS = {
    "accept": "*/*",
    "X-API-KEY": st.secrets["api"]["key"],       # secrets.toml から読み込み
    "X-API-USERKEY": st.secrets["api"]["userkey"],  # secrets.toml から読み込み
    "X-DB": st.secrets["api"]["db"]             # secrets.toml から読み込み
}

# デバッグ出力用関数
def log_debug_response(response):
    st.write("### デバッグ情報")
    st.text("Request URL:")
    st.text(response.url)  # 実際のリクエストURL
    st.text("Request Headers:")
    st.json(dict(response.request.headers))
    st.text("Response Headers:")
    st.json(dict(response.headers))
    st.text("Response Content:")
    st.text(response.text)

# データ取得関数
@st.cache_data
def fetch_gyosha_list(fields=None):
    try:
        # パラメータの動的生成
        params = {}
        if fields:
            params = {"fields": fields}

        # APIリクエスト送信
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        response.raise_for_status()  # ステータスコードが200以外の場合例外を発生
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTPエラーが発生しました: {e.response.status_code}")
        log_debug_response(response)
        return {}
    except requests.exceptions.ConnectionError:
        st.error("APIサーバーへの接続に失敗しました。")
        return {}
    except requests.exceptions.Timeout:
        st.error("APIリクエストがタイムアウトしました。")
        return {}
    except requests.exceptions.RequestException as e:
        st.error(f"予期しないエラーが発生しました: {e}")
        return {}

# サンプルデータ（最初の20項目を取得）
SAMPLE_JSON = {
    "mgyID": "2",
    "Shiirecd": "1",
    "mgyShiiresaki1": "社内原価",
    "mgyShiiresaki2": "",
    "mgyRyakuName": "社内原価",
    "mgyKeisyou": "御中",
    "mgyFurigana": "ｼｬﾅｲ",
    "mgyYubin": "",
    "mgyJusyo1": "",
    "mgyJusyo2": "",
    "mgyEmail": "",
    "mgyTel": "",
    "mgyFax": "",
    "mgyGyosyaKb": "9",
    "mgyGyosyaKbName": "その他",
    "mgyBusyo": "",
    "mgyTanto": "",
    "mgyDaihyo": "",
    "mgyMyNumber": ""
}

# JSONデータの最初の20項目を選択肢に追加
additional_fields = list(SAMPLE_JSON.keys())[:20]

# フィールド選択UIを追加
available_fields = ["mgyID", "Shiirecd", "mgyRyakuName", "mgyTel", "mgyFax"]
available_fields.extend([field for field in additional_fields if field not in available_fields])  # 重複を避けて追加

fields = st.multiselect(
    "取得するフィールドを選択してください",
    options=available_fields,
    default=["mgyID", "Shiirecd", "mgyRyakuName"]
)

# データ取得
with st.spinner("データを取得中..."):
    data = fetch_gyosha_list(fields)

# データ表示
if data and "data" in data:
    st.write("### 取得データ")
    # データをテーブル形式で表示
    df = pd.DataFrame(data.get("data", []))
    st.dataframe(df)
else:
    st.info("業者データが見つかりませんでした。")
