from fastapi import FastAPI
from api.v1 import email_router

app = FastAPI(
    title="AutoU Classificador de Emails",
    description="API para classificar emails e sugerir respostas automáticas",
    version="0.1.0",
)

app.include_router(email_router.router, prefix="/api/v1", tags=["Email Processing"])


@app.get("/")
async def health_check():
    return {"message": "Bem-vindo à API de Classificação de Emails da AutoU!"}
