from backend.services.nlp_service import preprocess_text
from backend.services.openai_service import OpenAIService
from typing import TypedDict


class EmailProcessingResult(TypedDict):
    classification: str
    suggested_response: str


class EmailProcessingService:
    def __init__(self) -> None:
        self.openai_service = OpenAIService()

    def process_email(self, email_content: str) -> EmailProcessingResult:
        """
        Processa um e-mail: pré-processa o texto, classifica e gera uma resposta
        """

        # etapa 1
        processed_text = preprocess_text(email_content)

        # etapa 2
        classification = self.openai_service.classify_email(processed_text)

        # etapa 3
        suggested_response = self.openai_service.generate_response(
            email_content, classification
        )

        return {
            "classification": classification,
            "suggested_response": suggested_response,
        }
