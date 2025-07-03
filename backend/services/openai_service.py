import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class OpenAIService:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.getenv("OPENAPI_APIKEY"))
        if not self.client.api_key:
            raise ValueError("OPENAPI_APIKEY não encontrada nas variáveis de ambiente.")

    def classify_email(self, email_content: str) -> str:
        """
        Classifica o conteúdo de um email como 'Produtivo' ou 'Improdutivo' usando a API do OpenAI
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um assistente que classifica e-mails.",
                    },
                    {
                        "role": "user",
                        "content": f"""Classifique o seguinte e-mail em uma das categorias: 'Produtivo' ou 'Improdutivo'.
                    Responda apenas com a categoria.
                    
                    E-mail: {email_content}""",
                    },
                ],
                max_tokens=10,  # Limita a reposta
                temperature=0.1,  # Torna a resposta mais determinística
            )
            classification = response.choices[0].message.content.strip()

            if classification not in ["Produtivo", "Improdutivo"]:
                if "Produtivo" in classification:
                    return "Produtivo"
                elif "Improdutivo" in classification:
                    return "Improdutivo"
                else:
                    return "Desconhecido"
            return classification
        except Exception as e:
            print(f"Erro ao classificar e-mail com OpenAI: {e}")
            return "Erro na Classificação"

            ## implementei somente a primeira função
