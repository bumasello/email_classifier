# tests/test_api_endpoints.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, Mock
from backend.main import app  # Importa a aplicação FastAPI
from backend.services.email_processing_service import EmailProcessingResult

# REMOVA ESTA LINHA: from backend.api.v1.email_router import get_email_processing_service
from backend.api.v1.email_router import (
    get_email_processing_service,
)  # Importar para poder sobrescrever
from typing import cast

client = TestClient(app)


# Fixture para mockar o EmailProcessingService para todos os testes de API
@pytest.fixture
def mock_email_processor_service():
    mock_service = MagicMock()
    # Sobrescreve a dependência get_email_processing_service na aplicação FastAPI
    app.dependency_overrides[get_email_processing_service] = lambda: mock_service
    yield mock_service  # Retorna o mock para que os testes possam configurá-lo
    app.dependency_overrides = {}  # Limpa a sobrescrita após o teste


# Agora, cada teste que precisa do mock pode simplesmente receber a fixture como parâmetro
def test_process_email_text_productive(
    mock_email_processor_service: Mock,
):  # Recebe a fixture
    """
    Testa o endpoint /process-email com texto direto para um e-mail produtivo.
    """
    mock_email_processor_service.process_email.return_value = EmailProcessingResult(
        classification="Produtivo",
        suggested_response="Sua solicitação será processada em breve.",
    )

    email_content = "Preciso de ajuda com meu pedido."
    response = client.post(
        "/api/v1/process-email",
        data={"email_content": email_content},
    )

    assert response.status_code == 200
    assert response.json() == {
        "classification": "Produtivo",
        "suggested_response": "Sua solicitação será processada em breve.",
    }
    mock_email_processor_service.process_email.assert_called_once_with(email_content)


def test_process_email_text_unproductive(mock_email_processor_service: Mock):
    """
    Testa o endpoint /process-email com texto direto para um e-mail improdutivo.
    """
    mock_email_processor_service.process_email.return_value = EmailProcessingResult(
        classification="Improdutivo", suggested_response="Agradecemos sua mensagem."
    )

    email_content = "Feliz aniversário!"
    response = client.post(
        "/api/v1/process-email", data={"email_content": email_content}
    )

    assert response.status_code == 200
    assert response.json() == {
        "classification": "Improdutivo",
        "suggested_response": "Agradecemos sua mensagem.",
    }
    mock_email_processor_service.process_email.assert_called_once_with(email_content)


def test_process_email_file_txt(mock_email_processor_service: Mock):
    """
    Testa o endpoint /process-email com upload de arquivo .txt.
    """
    mock_email_processor_service.process_email.return_value = EmailProcessingResult(
        classification="Produtivo", suggested_response="Arquivo processado com sucesso."
    )

    file_content = "Conteúdo do e-mail do arquivo TXT."
    files = {"email_file": ("email.txt", file_content, "text/plain")}

    response = client.post("/api/v1/process-email", files=files)

    assert response.status_code == 200
    assert response.json() == {
        "classification": "Produtivo",
        "suggested_response": "Arquivo processado com sucesso.",
    }
    mock_email_processor_service.process_email.assert_called_once_with(file_content)


def test_process_email_no_input():  # Este teste não precisa do mock, pois a validação ocorre antes
    """
    Testa o endpoint /process-email sem nenhum input.
    """
    response = client.post("/api/v1/process-email")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "É necessário fornecer o conteúdo do e-mail ou um arquivo."
    }


def test_process_email_empty_content():  # Este teste não precisa do mock
    """
    Testa o endpoint /process-email com conteúdo vazio.
    """
    response = client.post("/api/v1/process-email", data={"email_content": "   "})
    assert response.status_code == 400
    assert response.json() == {"detail": "O conteúdo do e-mail não pode estar vazio."}


def test_process_email_unsupported_file_type():  # Este teste não precisa do mock
    """
    Testa o endpoint /process-email com tipo de arquivo não suportado.
    """
    file_content = "Conteúdo de um arquivo de imagem."
    files = {"email_file": ("image.jpg", file_content, "image/jpeg")}

    response = client.post("/api/v1/process-email", files=files)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Tipo de arquivo não suportado. Apenas .txt ou .pdf."
    }


def test_process_email_pdf_not_implemented():  # Este teste não precisa do mock
    """
    Testa o endpoint /process-email com arquivo PDF (ainda não implementado).
    """
    file_content = "Conteúdo de um PDF simulado."
    files = {"email_file": ("document.pdf", file_content, "application/pdf")}

    response = client.post("/api/v1/process-email", files=files)
    assert response.status_code == 501
    assert response.json() == {
        "detail": "Leitura de arquivos PDF ainda não implementada."
    }


def test_process_email_internal_error(mock_email_processor_service: Mock):
    """
    Testa o tratamento de erro interno no serviço de processamento.
    """
    mock_email_processor_service.process_email.side_effect = Exception(
        "Erro simulado no serviço"
    )

    email_content = "E-mail que causa erro."
    response = client.post(
        "/api/v1/process-email", data={"email_content": email_content}
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "Erro interno ao processar o e-mail."}
    mock_email_processor_service.process_email.assert_called_once_with(email_content)
