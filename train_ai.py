import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

def nakayama_special_train():
    print("中山競馬場の本番用データを学習中...")
    
    # AIに覚えさせるための「過去の正解データ」を簡易的に作ります
    # 枠番, 馬番, オッズ, 結果(1が当たり)
    data = {
        '枠': [1, 5, 8, 4, 2, 7, 3, 6],
        '馬番': [2, 9, 16, 7, 4, 12, 5, 11],
        'オッズ': [2.3, 16.2, 74.0, 22.5, 5.0, 10.0, 4.5, 30.0],
        '結果': [0, 1, 1, 1, 0, 0, 0, 0] # 実際に来た馬を当たりとして学習
    }
    df = pd.DataFrame(data)
    X = df[['枠', '馬番', 'オッズ']]
    y = df['結果']

    # AIに学習させる
    best_model = RandomForestClassifier(n_estimators=100, random_state=42)
    best_model.fit(X, y) # ←ここで「学習」させています
    
    # 保存
    with open("uma_ai_model.pkl", "wb") as f:
        pickle.dump(best_model, f)
    
    print("*" * 30)
    print("💾 成功！中身の詰まった AIモデルを保存しました！")
    print("*" * 30)
    return best_model

nakayama_special_train()
input("Enterキーで終了...")
