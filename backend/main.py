from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import email_router

app = FastAPI(
    title="AutoU Classificador de Emails",
    description="API para classificar emails e sugerir respostas automáticas",
    version="0.1.0",
)

origins = ["http://localhost:5173", "https://email-classifier-sand-chi.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc. )
    allow_headers=["*"],  # Permite todos os cabeçalhos)
)

app.include_router(email_router.router, prefix="/api/v1", tags=["Email Processing"])


@app.get("/")
async def welcome():
    return {"message": "Bem-vindo à API de Classificação de Emails da AutoU!"}


@app.get("/healthcheck")
async def health_check():
    return {"message": "OK"}
