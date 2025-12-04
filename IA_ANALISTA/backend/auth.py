from fastapi import APIRouter
import json

router = APIRouter()

def load_db():
    return json.load(open("backend/database.json"))

@router.post("/login")
def login(data: dict):
    email = data["email"]
    senha = data["senha"]

    db = load_db()

    for user in db["usuarios"]:
        if user["email"] == email and user["senha"] == senha:
            return {"status": "ok", "nivel": user["nivel"]}

    return {"status": "erro", "msg": "Credenciais incorretas"}
