from fastapi import FastAPI
from auth import router as auth_router
from users import router as users_router
from analyse import router as analyse_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="IA Empresarial Premium")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(users_router, prefix="/users")
app.include_router(analyse_router, prefix="/analyse")

@app.get("/")
def root():
    return {"status": "ONLINE", "message": "IA Premium rodando."}

