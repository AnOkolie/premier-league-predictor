import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.metrics import mean_absolute_error, r2_score

FEATURES = ["age","goals_by_jan","assists_by_jan","position_Attack", "position_Defender", "position_Goalkeeper", "position_Midfield","contract_expiry","minutes_played_by_jan","january_value"]
TARGET=["end_val"]
def training(df):
    X = df[FEATURES]
    y=df["end_val"]
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
    model = LinearRegression()

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    results = pd.DataFrame({
    "actual_valuation": y_test,
    "predicted_valuation": predictions})

    print(results.head(10))

def predict_future_valuation(df):
    historical_df = df.dropna(subset=["end_val"]).copy()
    historical_df["season_start"] = pd.to_datetime(historical_df["season_start"])
    train_df = historical_df[
    historical_df["season_start"].dt.year.astype(int) <= 2024].copy()

    test_df = historical_df[
        historical_df["season_start"].dt.year.astype(int) == 2025
    ].copy()
    X_train = train_df[FEATURES]
    y_train = train_df[TARGET]

    X_test = test_df[FEATURES]
    y_test = test_df[TARGET]
    model = LinearRegression()
    
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print(f"MAE: {mae:,.0f}")
    print(f"R²: {r2:.3f}")
    
def predict_player(df,name: str):
    player_df = df[df["player_name"] == name]
    
    
    

def get_one_hot_encoding(df):
    position_columns = pd.get_dummies(
    df["position"],
    prefix="position",
    dtype=int)
    encoded_df = pd.concat([df, position_columns], axis=1)
    return encoded_df
    
def main():
    df = pd.read_csv("../data/player_stats.csv")
    df = get_one_hot_encoding(df)
    training(df)
    predict_future_valuation(df)
    
if __name__ == "__main__":
    main()