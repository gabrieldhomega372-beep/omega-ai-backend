# painel_backend.py (ou adicionar no main.py)
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uuid

app = FastAPI()

# --- fake db (trocar pra DB real depois) ---
USERS = {
  "admin@empresa.com": {"senha":"senha123","role":"admin"}
}
TOKENS = {}
STATS = {"conteudos":0,"analises":0,"users":len(USERS)}

class LoginReq(BaseModel):
  email: str
  senha: str

@app.post("/login")
def login(req: LoginReq):
  user = USERS.get(req.email)
  if not user or user.get("senha") != req.senha:
    return {"sucesso":False, "msg":"Credenciais inválidas"}
  token = str(uuid.uuid4())
  TOKENS[token] = req.email
  return {"sucesso":True, "token":token}

@app.get("/stats")
def stats(request: Request):
  auth = request.headers.get("authorization")
  if not auth or auth not in TOKENS: raise HTTPException(401, "não autorizado")
  return STATS

class ConteudoReq(BaseModel):
  tema: str = ""
  prompt: str

@app.post("/gerar_conteudo")
def gerar_conteudo(req: ConteudoReq, request: Request):
  auth = request.headers.get("authorization")
  if not auth or auth not in TOKENS: raise HTTPException(401, "não autorizado")
  # chama sua IA real aqui — por enquanto devolve dummy
  STATS["conteudos"] += 1
  resultado = f"Gerado (tema:{req.tema}): Resposta exemplo -> {req.prompt[:180]}"
  return {"resultado": resultado}

class AnaliseReq(BaseModel):
  texto: str

@app.post("/analisar_texto")
def analisar_texto(req: AnaliseReq, request: Request):
  auth = request.headers.get("authorization")
  if not auth or auth not in TOKENS: raise HTTPException(401, "não autorizado")
  STATS["analises"] += 1
  # por enquanto análise fake
  resumo = req.texto[:300]
  return {"resultado": f"Análise rápida (resumo): {resumo}"}

@app.get("/users")
def get_users(request: Request):
  auth = request.headers.get("authorization")
  if not auth or auth not in TOKENS: raise HTTPException(401, "não autorizado")
  arr = [{"email":e,"role":d.get("role","user")} for e,d in USERS.items()]
  return {"users":arr}

@app.post("/config")
def set_config(payload: dict, request: Request):
  auth = request.headers.get("authorization")
  if not auth or auth not in TOKENS: raise HTTPException(401, "não autorizado")
  # salvar config (aqui apenas ecoa)
  return {"msg": "Config salva (temporário)"}
