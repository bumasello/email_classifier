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
            message = response.choices[0].message
            if message.content is None:
                return "Erro: resposta sem conteúdo"
            classification = message.content.strip()

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

    def generate_response(self, email_content: str, classification: str) -> str:
        """
        Gera uma reposta automática para o e-mail com base na sua classificação usando a API do OpenAI.
        """
        prompt = ""
        if classification == "Produtivo":
            prompt = f"""
                    O e-mail a seguir foi classificado como 'Produtivo'.
                    Gere uma resposta automática profissional e concisa para este e-mail,
                    indicando que a solicitação será processada e que o remetente será contatado em breve. Para dados de contato: Meu nome: Bruno Masello, cargo: Analista Júnior.
                    E-mail: {email_content}
                    """
        elif classification == "Improdutivo":
            prompt = f"""O e-mail a seguir foi classificado como 'Improdutivo'.
                        Gere uma resposta automática educada e breve, agradecendo a mensagem
                        e informando que nenhuma ação adicional é necessária. Para dados de contato: Meu nome: Bruno Masello, cargo: Analista Júnior.
                        E-mail: {email_content}"""
        else:
            return "Não foi possível gerar uma resposta para esta classificação."

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Ou outro modelo de sua preferência
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um assistente que gera respostas automáticas para e-mails.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=150,
                temperature=0.7,
            )  # Permite um pouco mais de criatividade na resposta)

            message = response.choices[0].message
            if message.content is None:
                return "Erro: resposta sem conteúdo"
            classification = message.content.strip()
            return classification
        except Exception as e:
            print(f"Erro ao gerar resposta com OpenAI: {e}")
            return "Erro na Geração de Resposta"
