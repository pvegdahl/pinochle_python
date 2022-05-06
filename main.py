from typing import Tuple, Dict

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Game(BaseModel):
    players: Tuple[str, str, str, str]


games: Dict[int, Game] = {}


@app.get("/games/{game_id}")
def get_game(game_id: int):
    return games[game_id]


@app.post("/games/")
def new_game(game: Game):
    game_id = len(games)
    games[game_id] = game
    return {"game_id": game_id}
