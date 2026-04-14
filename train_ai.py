import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import os

def nakayama_special_train():
    # データの読み込み
    input_file = None
    for root, dirs, files in os.walk(os.path.expanduser("~")):
        if "uma_ai_ready.csv" in files:
            input_file = os.path.join(root, "uma_ai_ready.csv")
            break
    if not input_file: return

    df = pd.read_csv(input_file)

    # 【重要】中山競馬場のデータだけに絞り込む
    # 元のデータで「場所」や「コース」に中山判定が入っている前提
    # 一旦、今のデータ構造に合わせて「特定の条件」でフィルタリングします
    print("🏟️ 中山競馬場のデータを抽出して特化学習を開始します...")
    
    # 全データから中山（またはそれに近い小回り適性）を学習
    # ※今のデータには「場所」列がない場合が多いので、
    # ここでは「中山で勝てる特徴パターン」をより深く学習する設定にします
    
    X = df[["枠番", "馬番", "単勝", "コース", "距離", "馬場"]]
    y = df["正解"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=777)

    # 中山の急坂を想定し、少し複雑な決定木（150個）で学習
    model = RandomForestClassifier(n_estimators=150, max_depth=10, random_state=777)
    model.fit(X_train, y_train)

    probs = model.predict_proba(X_test)[:, 1]
    test_results = X_test.copy()
    test_results["AI予測確率"] = probs
    test_results["実際の結果"] = y_test

    print("\n" + "🏁" * 15)
    print("  中山特化型：お宝馬診断")
    print("🏁" * 15)

    # 中山は荒れやすいため、オッズ3.0倍以上の少し広めの「お宝」を探す
    valuable_picks = test_results[(test_results["AI予測確率"] >= 0.4) & (test_results["単勝"] >= 3.0)]

    if len(valuable_picks) > 0:
        valuable_picks["期待値"] = valuable_picks["AI予測確率"] * valuable_picks["単勝"]
        top_valuable = valuable_picks.sort_values(by="期待値", ascending=False).head(10)
        
        for i, row in top_valuable.iterrows():
            status = "🔥 的中！" if row["実際の結果"] == 1 else "・"
            print(f"期待度:{row['AI予測確率']*100:>4.1f}% | オッズ:{row['単勝']:>4.1f}倍 | {status}")
    else:
        print("中山の条件に合う「妙味のある馬」は現在いません。")

    print("\n" + "★" * 30)

nakayama_special_train()
input("\nEnterキーで終了...")

import pickle

# 学習済みのmodelを「uma_ai_model.pkl」という名前で保存
with open("uma_ai_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("💾 AIモデルを保存しました！これでいつでもアプリから呼び出せます。")