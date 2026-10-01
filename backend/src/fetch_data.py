import requests
import os
from dotenv import load_dotenv
import time
import pandas as pd

load_dotenv()

BASE_URL = "https://v3.football.api-sports.io/"
headers = {
    "x-apisports-key": os.getenv("API_KEY_FOOTBALL_DATA")
}

def make_request(endpoint, query_params):
    request_url = BASE_URL+endpoint
    response = requests.get(request_url,params=query_params, headers=headers)
    payload = response.json()
    return payload

def get_players():
    query_params = {
            "league" : 39,
            "season" : 2024,
            "page": 1
        }
    
    player_list = []
    while(True):
        data = make_request("players",query_params)
        print(data)
        data_frame_cols = [
            "id","First Name","Last Name", "Age", "Team Name", "Team Id", "Appearances", "Rating", "Goals", "Assists"
        ]
        players = data.get("response")
        print(players)
        for player in players:
            info = player.get("player")
            stats = player.get("statistics")
            player_id = info.get("id")
            player_firstName = info.get("firstname"),
            player_lastName = info.get("lastname")
            age = info.get("age")
            for stat in stats:
                team_name = stat.get("team").get("name"),
                team_id = stat.get("team").get("name"),
                appearances = stat.get("games").get("appearances"),
                average_rating = stat.get("games").get("rating"),
                goals = stat.get("goals").get("goals"),
                assists = stat.get("goals").get("assists"),
            player_list.append({
                "id": player_id,
                "First Name" : player_firstName,
                "Last Name": player_lastName,
                "Age" : age,
                "Team Name" : team_name,
                "Team Id": team_id,
                "Appearances" : appearances,
                "Rating" : average_rating,
                "Goals" : goals,
                "Assists" : assists
            })
        current_page = data["paging"]["current"]
        total_pages = data["paging"]["total"]

        print(f"Fetched page {current_page}/{total_pages}")

        # Stop when we've reached the final page
        if current_page >= total_pages:
            break

        query_params["page"] += 1
    df = pd.DataFrame(player_list, columns=data_frame_cols)
    df.to_csv("players.csv", index=False)
    

def get_team_players(tables):
    counter = 0
    players = []
    for entry in tables:
        team = entry.get("team")
        team_id = team.get("id")
        team_name = team.get("name")
        if(team_id is None): 
            continue
        if(counter == 10):
            time.sleep(60)
        data = make_request(f"teams/{team_id}")
        print(f"fetching team {team_name}'s players...")
        squad = data.get("squad")
        counter += 1
        if(squad is None):
            continue
        for player in squad:
            player_id = player.get("id")
            player_name = player.get("name")
            player_position = player.get("position")
            player_Dob = player.get("dateOfBirth")
            player_nationality = player.get("nationality")
            players.append({
                "id": player_id,
                "Name": player_name,
                "Position" : player_position,
                "DOB" : player_Dob,
                "Nationality" :player_nationality,
                "Team Id" :team_id,
                "Team Name" : team_name
            })
    data_columns = [
        "id", "Name","Position","DOB","Nationality","Team Id","Team Name"
    ]
    df = pd.DataFrame(players,columns=data_columns)
    df['DOB'] = pd.to_datetime(df['DOB'])
    df.to_csv("players.csv",index=False)
            
def main():
    # data = make_request("competitions/PL/standings")
    # stand = data.get("standings")
    # tables = stand[0].get("table")
    # get_team_players()
    get_players()
    
if __name__ == "__main__":
    main()