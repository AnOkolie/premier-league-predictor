import matplotlib.pyplot as plt
import pandas as pd

def goal_assists_against_value(df,season:str):
    plt.figure(figsize=(10, 6))
    plt.scatter(
        df["g/a"],
        df["valuation"]
    )
    plt.xlabel("Goal Contributions (km)")
    plt.ylabel("Valuation (Euros)")
    plt.title(f"Relationship Between Goal contributions and Valuation {season} season")

    plt.tight_layout()
    for i, row in df.iterrows():
        plt.text(row["g/a"], row["valuation"], row["player_name"])

    file_path = "../charts/goals_&_assists_vs_valuation_"+season.replace("/","-")+".png"
    print(f"saving to file path: {file_path}")
    plt.savefig(file_path)
    
def main():
    df = pd.read_csv("../data/player_stats.csv")
    seasons = df["season"].unique()
    for season in seasons:
        plot = df.where(df["season"] == season)
        print(f"missing names in {season} {plot["player_name"].isna().sum()}")
        print(season)
        goal_assists_against_value(plot,season)
    
    
if __name__ == "__main__":
    main()