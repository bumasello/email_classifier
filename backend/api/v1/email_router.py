# backend/api/v1/email_router.py

from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    File,
    Form,
    Depends,
)  # Importar Depends
from backend.services.email_processing_service import (
    EmailProcessingService,
    EmailProcessingResult,
)
from typing import Union

router = APIRouter()

# REMOVA ESTA LINHA: email_processor = EmailProcessingService()


# Define uma função de dependência para obter o EmailProcessingService
# Isso permite que o FastAPI gerencie a instância e facilita o mocking em testes
def get_email_processing_service() -> EmailProcessingService:
    return EmailProcessingService()


@router.post("/process-email", response_model=EmailProcessingResult)
async def process_email_endpoint(
    email_content: Union[str, None] = Form(None),  # Para texto direto via formulário
    email_file: Union[UploadFile, None] = File(None),  # Para upload de arquivo
    # INJETAR AQUI:
    email_processor: EmailProcessingService = Depends(get_email_processing_service),
):
    """
    Processa um e-mail, classificando-o e sugerindo uma resposta automática.
    Pode receber o conteúdo do e-mail como texto direto ou via upload de arquivo (.txt ou .pdf).
    """
    if email_content is None and email_file is None:
        raise HTTPException(
            status_code=400,
            detail="É necessário fornecer o conteúdo do e-mail ou um arquivo.",
        )

    content_to_process = ""
    if email_file:
        if email_file.content_type == "text/plain":
            content_to_process = (await email_file.read()).decode("utf-8")
        elif email_file.content_type == "application/pdf":
            raise HTTPException(
                status_code=501,
                detail="Leitura de arquivos PDF ainda não implementada.",
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Tipo de arquivo não suportado. Apenas .txt ou .pdf.",
            )
    elif email_content:
        content_to_process = email_content

    if not content_to_process.strip():
        raise HTTPException(
            status_code=400, detail="O conteúdo do e-mail não pode estar vazio."
        )

    try:
        result = email_processor.process_email(content_to_process)
        return result
    except Exception as e:
        print(f"Erro interno ao processar e-mail: {e}")
        raise HTTPException(
            status_code=500, detail="Erro interno ao processar o e-mail."
        )
