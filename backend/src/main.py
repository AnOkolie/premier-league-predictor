from fastapi import FastAPI
import requests 
import os
import datetime
app = FastAPI()


BASE_URL = "https://v3.football.api-sports.io/"
headers = {
    "x-apisports-key": os.getenv("API_KEY_FOOTBALL_DATA")
}
PREMIER_LEAGUE_CODE = 39
SEASON=datetime.date.year

@app.get("/")
def health_check():
    return {"message": "Welcome to my Data Science fast api"}

@app.get("/actuator/health")
def health_check():
    return {"message": "Status is 200"}

@app.get("/player/")
def get_player_predictions(name:str):
    query_params = f"players?league={PREMIER_LEAGUE_CODE}&search={name}&season={SEASON}"
    response = requests.get(BASE_URL+query_params,headers=headers)
    print("respo",response)
    return {"response": response}