import streamlit as st
import pandas as pd
import time

# --- アプリの設定 ---
st.set_page_config(page_title="JRA特化型予想AI - Phase 1", layout="wide")

st.title("🐎 中央競馬特化型予想AI")
st.caption("Phase 1: リアルタイム・データ解析基盤")

# --- サイドバー：設定 ---
st.sidebar.header("設定")
target_url = st.sidebar.text_input("レースURL（netkeiba等）を入力", placeholder="https://race.netkeiba.com/...")

# --- メインコンテンツ ---
col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. データ取得")
    if st.button("データを自動収集する"):
        if not target_url:
            st.error("URLを入力してください")
        else:
            with st.spinner('データを解析中...'):
                # ここに将来スクレイピングコードを実装します
                time.sleep(2) 
                st.success("データの取得に成功しました（デモ表示）")
                
                # サンプルデータ（ここにスクレイピングしたデータが入る）
                demo_data = {
                    "馬番": [9, 16, 7, 2],
                    "馬名": ["クラスペディア", "モズナナスター", "ウインモナーク", "ソーダーンライト"],
                    "オッズ": [16.2, 74.0, 22.5, 2.3],
                    "脚質": ["先行", "追込", "先行", "差し"]
                }
                df = pd.DataFrame(demo_data)
                st.session_state['race_data'] = df

    if 'race_data' in st.session_state:
        st.write("### 取得した馬名・オッズ一覧")
        st.dataframe(st.session_state['race_data'], use_container_width=True)

with col2:
    st.header("2. AI分析（14項目評価）")
    if 'race_data' in st.session_state:
        # ここで将来的に「14項目」を評価するロジックを回します
        st.info("現在は「枠順・オッズ・脚質」をベースに暫定評価中...")
        
        df = st.session_state['race_data'].copy()
        # 暫定的な期待度計算（仮）
        df['期待度'] = [85, 78, 72, 60] 
        
        st.write("### AI解析結果")
        st.table(df[["馬名", "期待度"]])
        
        st.warning("※Phase 2で『血統・展開・調教』の自動反映を実装予定です。")
    else:
        st.write("左側でデータを取得してください。")

# --- フッター：14項目のチェックリスト ---
st.markdown("---")
with st.expander("将来的に組み込む14項目のロードマップを確認"):
    st.write("""
    1. レース条件 / 2. 馬能力 / 3. 展開 / 4. 枠順 / 5. 騎手 / 6. 調教 / 7. 馬体 / 8. 血統 / 
    9. オッズ / 10. 過去傾向 / 11. 馬場状態 / 12. ローテ / 13. 厩舎 / 14. 資金配分
    """)