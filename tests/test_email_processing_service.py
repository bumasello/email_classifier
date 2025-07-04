from unittest.mock import patch, MagicMock, Mock
from backend.services.email_processing_service import EmailProcessingService
from typing import cast


@patch("backend.services.email_processing_service.preprocess_text")
@patch("backend.services.email_processing_service.OpenAIService")
def test_process_email_productive(
    mock_openai_service_class: Mock,
    mock_preprocess_text: Mock,
):
    """
    Testa o processamento completo de um e-mail produtivo.
    """
    mock_preprocess_text.return_value = "texto pre-processado"

    mock_openai_instance = cast(MagicMock, mock_openai_service_class.return_value)
    mock_openai_instance.classify_email.return_value = "Produtivo"
    mock_openai_instance.generate_response.return_value = "Resposta produtiva gerada."

    service = EmailProcessingService()
    email_content = "Conteúdo do e-mail produtivo."
    result = service.process_email(email_content)

    mock_preprocess_text.assert_called_once_with(email_content)
    mock_openai_instance.classify_email.assert_called_once_with("texto pre-processado")
    mock_openai_instance.generate_response.assert_called_once_with(
        email_content, "Produtivo"
    )

    assert result == {
        "classification": "Produtivo",
        "suggested_response": "Resposta produtiva gerada.",
    }


@patch("backend.services.email_processing_service.preprocess_text")
@patch("backend.services.email_processing_service.OpenAIService")
def test_process_email_unproductive(
    mock_openai_service_class: Mock, mock_preprocess_text: Mock
):
    """
    Testa o processamento completo de um e-mail improdutivo.
    """
    mock_preprocess_text.return_value = "texto pre-processado"

    mock_openai_instance = cast(MagicMock, mock_openai_service_class.return_value)
    mock_openai_instance.classify_email.return_value = "Improdutivo"
    mock_openai_instance.generate_response.return_value = "Resposta improdutiva gerada."

    service = EmailProcessingService()
    email_content = "Conteúdo do e-mail improdutivo."
    result = service.process_email(email_content)

    mock_preprocess_text.assert_called_once_with(email_content)
    mock_openai_instance.classify_email.assert_called_once_with("texto pre-processado")
    mock_openai_instance.generate_response.assert_called_once_with(
        email_content, "Improdutivo"
    )

    assert result == {
        "classification": "Improdutivo",
        "suggested_response": "Resposta improdutiva gerada.",
    }


@patch("backend.services.email_processing_service.preprocess_text")
@patch("backend.services.email_processing_service.OpenAIService")
def test_process_email_error_in_classification(
    mock_openai_service_class: Mock, mock_preprocess_text: Mock
):
    """
    Testa o tratamento de erro se a classificação falhar.
    """
    mock_preprocess_text.return_value = "texto pre-processado"

    mock_openai_instance = cast(MagicMock, mock_openai_service_class.return_value)
    mock_openai_instance.classify_email.return_value = "Erro na Classificação"
    mock_openai_instance.generate_response.return_value = "Erro na Geração de Resposta"

    service = EmailProcessingService()
    email_content = "Conteúdo do e-mail com erro de classificação."
    result = service.process_email(email_content)

    mock_preprocess_text.assert_called_once_with(email_content)
    mock_openai_instance.classify_email.assert_called_once_with("texto pre-processado")
    mock_openai_instance.generate_response.assert_called_once_with(
        email_content, "Erro na Classificação"
    )

    assert result == {
        "classification": "Erro na Classificação",
        "suggested_response": "Erro na Geração de Resposta",
    }
