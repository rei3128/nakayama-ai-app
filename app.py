import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# --- アプリの設定 ---
st.set_page_config(page_title="JRA特化型予想AI", layout="wide")

st.title("🐎 中央競馬特化型予想AI")
st.caption("Phase 1.1: リアルタイム・スクレイピング実装中")

# --- サイドバー：設定 ---
st.sidebar.header("設定")
target_url = st.sidebar.text_input("netkeibaのレースURLを入力", placeholder="https://race.netkeiba.com/race/result.html?race_id=...")

# --- メインコンテンツ ---
col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. データ取得")
    if st.button("データを自動収集する"):
        if not target_url:
            st.error("URLを入力してください")
        elif "netkeiba.com" not in target_url:
            st.error("現在はnetkeibaのURLのみ対応しています")
        else:
            with st.spinner('netkeibaからデータを解析中...'):
                try:
                    # WEBページを取得
                    response = requests.get(target_url)
                    response.encoding = response.apparent_encoding # 文字化け防止
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # レース名を取得してみる
                    race_name = soup.find("div", class_="RaceName")
                    if race_name:
                        st.success(f"取得成功：{race_name.text.strip()}")
                    else:
                        st.warning("レース名が見つかりませんでした。URLが正しいか確認してください。")

                    # ここに将来的に馬名やオッズを抽出するロジックを追加していきます
                    st.info("次のステップで、この下の表に全頭データを自動展開させます！")

                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")

# --- フッター ---
st.markdown("---")
st.write("長期開発ロードマップ：現在は「1. レース情報の自動取得」を構築中")
