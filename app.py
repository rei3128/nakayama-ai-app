import streamlit as st
import pandas as pd
import pickle
import os

# アプリのタイトル
st.title("🏇 中山特化型 AI予想アプリ")
st.write("枠番やオッズを入れると、AIが的中確率を計算します。")

# 1. 保存したAIモデルを読み込む
model_path = "uma_ai_model.pkl"
if os.path.exists(model_path):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
else:
    st.error("AIモデルが見つかりません。先に学習させて保存してください。")
    st.stop()

# 2. 入力フォーム（スマホで押しやすいスライダーと数値入力）
with st.container():
    st.subheader("📊 レース情報を入力")
    waku = st.number_input("枠番", min_value=1, max_value=8, value=1)
    umaban = st.number_input("馬番", min_value=1, max_value=18, value=1)
    odds = st.number_input("単勝オッズ", min_value=1.0, max_value=100.0, value=5.0, step=0.1)
    
    # コースなどの詳細（これらもAIの学習に合わせて選択）
    course = st.selectbox("コース", ["芝", "ダート"])
    course_val = 0 if course == "芝" else 1
    
    baba = st.selectbox("馬場状態", ["良", "稍重", "重", "不良"])
    baba_map = {"良": 0, "稍重": 1, "重": 2, "不良": 3}

# 3. 予測実行ボタン
if st.button("🚀 AI予測を実行する"):
    # 入力データをAIが読み込める形式に整える
    # [枠番, 馬番, 単勝, コース, 距離, 馬場] の順（前回の学習に合わせる）
    # 一旦、距離は中山に多い1600mで固定
    input_data = [[waku, umaban, odds, course_val, 1600, baba_map[baba]]]
    
    prob = model.predict_proba(input_data)[0][1] * 100
    
    # 結果表示
    st.write("---")
    st.metric(label="的中期待度", value=f"{prob:.1f} %")
    
    if prob >= 70:
        st.success("🔥 激アツ！お宝馬の可能性があります！")
    elif prob >= 40:
        st.info("✅ 狙い目です。期待値は高いでしょう。")
    else:
        st.warning("⚠️ 慎重に。AIの評価は低めです。")

st.caption("※このアプリは過去のデータに基づいた予測であり、的中を保証するものではありません。")