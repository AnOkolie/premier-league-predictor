import pandas as pd


def merge_datasets():
    appearances = pd.read_csv("../data/appearances.csv")
    player_values = pd.read_csv("../data/player_valuations.csv")
    players = pd.read_csv("../data/players.csv")

    # ---------------------------------------------------------
    # 1. Parse dates
    # ---------------------------------------------------------

    appearances["date"] = pd.to_datetime(appearances["date"])
    player_values["date"] = pd.to_datetime(player_values["date"])
    players["contract_expiration_date"] = pd.to_datetime(
        players["contract_expiration_date"]
    )

    # Remove players without a contract expiration date
    players = players.dropna(
        subset=["contract_expiration_date"]
    )

    # ---------------------------------------------------------
    # 2. Filter Premier League appearances
    # ---------------------------------------------------------

    premier_league_appearances = appearances[
        (appearances["competition_id"] == "GB1")
        & (appearances["date"] >= "2019-07-01")
        & (appearances["date"] <= "2026-05-30")
    ].copy()

    # ---------------------------------------------------------
    # 3. Create season
    # ---------------------------------------------------------

    year = premier_league_appearances["date"].dt.year
    month = premier_league_appearances["date"].dt.month

    start_year = year.where(
        month >= 8,
        year - 1
    )

    premier_league_appearances["season"] = (
        start_year.astype(str)
        + "/"
        + (start_year + 1).astype(str).str[-2:]
    )

    # ---------------------------------------------------------
    # 4. Calculate player performance by season
    # ---------------------------------------------------------

    season_stats = (
        premier_league_appearances
        .groupby(["player_id", "season"])
        .agg(
            minutes=("minutes_played", "sum"),
            goals=("goals", "sum"),
            assists=("assists", "sum")
        )
        .reset_index()
    )

    # ---------------------------------------------------------
    # 5. Calculate maximum valuation for each player/season
    # ---------------------------------------------------------

    player_values["year"] = player_values["date"].dt.year
    player_values["month"] = player_values["date"].dt.month

    value_start_year = player_values["year"].where(
        player_values["month"] >= 8,
        player_values["year"] - 1
    )

    player_values["season"] = (
        value_start_year.astype(str)
        + "/"
        + (value_start_year + 1).astype(str).str[-2:]
    )
    
    # Generate the january stats 
    premier_league_appearances = premier_league_appearances.copy()
    appearance_dates = premier_league_appearances["date"]
    
    start_year = appearance_dates.dt.year
    
    premier_league_appearances["season_start"] = pd.to_datetime(start_year.astype(str) +"-08-01")
    premier_league_appearances["january_cutoff"] = pd.to_datetime((start_year+1).astype(str) +"-01-01")
    season_stats["january_cutoff"] = premier_league_appearances["january_cutoff"]
    midseason_stats = premier_league_appearances[premier_league_appearances["date"].between(
        premier_league_appearances["season_start"],premier_league_appearances["january_cutoff"],inclusive="left"
    )]

    january = midseason_stats.groupby(["player_id", "season", "season_start"]).agg(
                minutes=("minutes_played", "sum"),
                goals=("goals", "sum"),
                assists=("assists", "sum"),
            ).reset_index()
    january.rename(columns={"minutes" : "minutes_played_by_jan", "goals" : "goals_by_jan", "assists" : "assists_by_jan"}, inplace=True)

    season_stats = season_stats.merge(january, on=["player_id","season"], how="inner")
    
    player_values = player_values.copy()
    player_values["season_start"] = pd.to_datetime(value_start_year.astype(str) +"-08-01")
    player_values["january_cutoff"] = pd.to_datetime((value_start_year+1).astype(str) +"-01-01")
    midseason_value = player_values[player_values["date"].between(player_values["season_start"],player_values["january_cutoff"])]
    idx_january_value = midseason_value.groupby(["player_id","season"])["date"].idxmax()
    january_value = player_values.loc[idx_january_value,["player_id", "season",'market_value_in_eur']]
    january_value.rename(columns={"market_value_in_eur":"january_value"}, inplace=True)
    
    idx_start = player_values.groupby(["player_id", "season"])["date"].idxmin()
    idx_end =player_values.groupby(["player_id", "season"])["date"].idxmax()
    start = player_values.loc[idx_start, ["player_id", "season",'market_value_in_eur']]
    end = player_values.loc[idx_end, ["player_id", "season",'market_value_in_eur']]
    player_values = start.merge(end, on=["player_id","season"])
    player_values.rename(columns={"market_value_in_eur_x" : "start_val", "market_value_in_eur_y" : "end_val"}, inplace=True)
    player_values = player_values.merge(january_value)
    player_values.to_csv("../data/january_value.csv", index=False)
    season_values = (
        player_values
        .groupby(["player_id", "season", "start_val","end_val", "january_value"])
        .agg(
            valuation=("end_val", "max"),
        )
        .reset_index()
    )

    # ---------------------------------------------------------
    # 6. Combine performance + valuation
    # ---------------------------------------------------------

    dataset = season_stats.merge(
        season_values,
        on=["player_id", "season"],
        how="inner",
        validate="one_to_one"
    )

    # ---------------------------------------------------------
    # 7. Add player information
    # ---------------------------------------------------------

    dataset = dataset.merge(
        players[
            [
                "player_id",
                "name",
                "position",
                "foot",
                "date_of_birth",
                "contract_expiration_date"
            ]
        ],
        on="player_id",
        how="inner",
        validate="many_to_one"
    )

    # Rename player name
    dataset.rename(
        columns={
            "name": "player_name"
        },
        inplace=True
    )

    # ---------------------------------------------------------
    # 8. Calculate contract expiry
    # ---------------------------------------------------------

    # Calculate contract expiry relative to the beginning
    # of the player's season.
    season_start_year = (
        dataset["season"]
        .str[:4]
        .astype(int)
    )
    print(dataset.head())
    season_start_date = pd.to_datetime(
        season_start_year.astype(str) + "-08-01"
    )

    dataset["contract_expiry"] = (
        dataset["contract_expiration_date"]
        - season_start_date
    ).dt.days

    # ---------------------------------------------------------
    # 9. Calculate age
    # ---------------------------------------------------------

    dataset["date_of_birth"] = pd.to_datetime(
        dataset["date_of_birth"]
    )

    age = (
        season_start_year
        - dataset["date_of_birth"].dt.year
    )

    birthday_passed = (
        (dataset["date_of_birth"].dt.month < 8)
        |
        (
            (dataset["date_of_birth"].dt.month == 8)
            &
            (dataset["date_of_birth"].dt.day <= 1)
        )
    )

    dataset["age"] = age.where(
        birthday_passed,
        age - 1
    )

    # ---------------------------------------------------------
    # 10. Calculate goals + assists
    # ---------------------------------------------------------

    dataset["g/a"] = (
        dataset["goals"]
        + dataset["assists"]
    )

    # ---------------------------------------------------------
    # 11. Select final columns
    # ---------------------------------------------------------

    final_columns = [
        "player_id",
        "season",
        "player_name",
        "position",
        "foot",
        "date_of_birth",
        "valuation",
        "contract_expiry",
        "goals",
        "assists",
        "g/a",
        "age",
        "minutes",
        "start_val",
        "end_val",
        "minutes_played_by_jan",
        "goals_by_jan",
        "assists_by_jan",
        "season_start",
        "january_value"
    ]

    final_dataset = dataset[final_columns].copy()

    # ---------------------------------------------------------
    # 12. Save final CSV
    # ---------------------------------------------------------

    final_dataset.to_csv(
        "../data/player_stats.csv",
        index=False
    )
    return final_dataset



def main():
    merge_datasets()


if __name__ == "__main__":
    main()