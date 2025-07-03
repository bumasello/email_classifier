from fastapi import FastAPI

app = FastAPI(
    title="AutoU Classificador de Emails",
    description="API para classificar emails e sugerir respostas automáticas",
    version="0.1.0",
)


@app.get("/")
async def health_check():
    return {"message": "Bem-vindo à API de Classificação de Emails da AutoU!"}
