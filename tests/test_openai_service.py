# tests/test_openai_service.py

import pytest
from unittest.mock import MagicMock, patch, Mock
from backend.services.openai_service import OpenAIService
import os
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice
from typing import cast


@pytest.fixture(autouse=True)
def mock_openai_api_key():
    os.environ["OPENAI_API_KEY"] = "sk-test-key"  # Chave de teste
    yield
    del os.environ["OPENAI_API_KEY"]  # Limpa após o teste


@patch("backend.services.openai_service.OpenAI")
def test_classify_email_productive(
    mock_openai_class: Mock,
):
    """Testa a classificação de um e-mail como Produtivo."""
    mock_instance = cast(MagicMock, mock_openai_class.return_value)

    mock_message = MagicMock(spec=ChatCompletionMessage, content="Produtivo")
    mock_choice = MagicMock(spec=Choice, message=mock_message)
    mock_completion = MagicMock(spec=ChatCompletion, choices=[mock_choice])

    mock_instance.chat.completions.create.return_value = mock_completion

    service = OpenAIService()
    email_content = "Por favor, atualize o status do meu pedido #123."
    result = service.classify_email(email_content)
    assert result == "Produtivo"
    mock_instance.chat.completions.create.assert_called_once()
    args, kwargs = mock_instance.chat.completions.create.call_args  # type: ignore
    assert "Produtivo" in kwargs["messages"][1]["content"]


@patch("backend.services.openai_service.OpenAI")
def test_classify_email_unproductive(mock_openai_class: Mock):
    """Testa a classificação de um e-mail como Improdutivo."""
    mock_instance = cast(MagicMock, mock_openai_class.return_value)
    mock_message = MagicMock(spec=ChatCompletionMessage, content="Improdutivo")
    mock_choice = MagicMock(spec=Choice, message=mock_message)
    mock_completion = MagicMock(spec=ChatCompletion, choices=[mock_choice])
    mock_instance.chat.completions.create.return_value = mock_completion

    service = OpenAIService()
    email_content = "Feliz Natal e um próspero Ano Novo!"
    result = service.classify_email(email_content)
    assert result == "Improdutivo"


@patch("backend.services.openai_service.OpenAI")
def test_classify_email_api_error(mock_openai_class: Mock):
    """Testa o tratamento de erro na classificação."""
    mock_instance = cast(MagicMock, mock_openai_class.return_value)
    mock_instance.chat.completions.create.side_effect = Exception(
        "Erro de API simulado"
    )

    service = OpenAIService()
    email_content = "Qualquer e-mail."
    result = service.classify_email(email_content)
    assert result == "Erro na Classificação"


@patch("backend.services.openai_service.OpenAI")
def test_generate_response_productive(mock_openai_class: Mock):
    """Testa a geração de resposta para e-mail Produtivo."""
    mock_instance = cast(MagicMock, mock_openai_class.return_value)
    mock_message = MagicMock(
        spec=ChatCompletionMessage, content="Sua solicitação será processada em breve."
    )
    mock_choice = MagicMock(spec=Choice, message=mock_message)
    mock_completion = MagicMock(spec=ChatCompletion, choices=[mock_choice])
    mock_instance.chat.completions.create.return_value = mock_completion

    service = OpenAIService()
    email_content = "Preciso de ajuda com meu login."
    classification = "Produtivo"
    result = service.generate_response(email_content, classification)
    assert result == "Sua solicitação será processada em breve."
    args, kwargs = mock_instance.chat.completions.create.call_args  # type: ignore
    assert "Produtivo" in kwargs["messages"][1]["content"]


@patch("backend.services.openai_service.OpenAI")
def test_generate_response_unproductive(mock_openai_class: Mock):
    """Testa a geração de resposta para e-mail Improdutivo."""
    mock_instance = cast(MagicMock, mock_openai_class.return_value)
    mock_message = MagicMock(
        spec=ChatCompletionMessage, content="Agradecemos sua mensagem."
    )
    mock_choice = MagicMock(spec=Choice, message=mock_message)
    mock_completion = MagicMock(spec=ChatCompletion, choices=[mock_choice])
    mock_instance.chat.completions.create.return_value = mock_completion

    service = OpenAIService()
    email_content = "Obrigado pelo seu tempo."
    classification = "Improdutivo"
    result = service.generate_response(email_content, classification)
    assert result == "Agradecemos sua mensagem."
    args, kwargs = mock_instance.chat.completions.create.call_args  # type: ignore
    assert "Improdutivo" in kwargs["messages"][1]["content"]


@patch("backend.services.openai_service.OpenAI")
def test_generate_response_api_error(mock_openai_class: Mock):
    """Testa o tratamento de erro na geração de resposta."""
    mock_instance = cast(MagicMock, mock_openai_class.return_value)
    mock_instance.chat.completions.create.side_effect = Exception(
        "Erro de API simulado"
    )

    service = OpenAIService()
    email_content = "Qualquer e-mail."
    classification = "Produtivo"
    result = service.generate_response(email_content, classification)
    assert result == "Erro na Geração de Resposta"


@patch("backend.services.openai_service.OpenAI")
def test_classify_email_unexpected_response(mock_openai_class: Mock):
    """Testa a classificação com uma resposta inesperada do modelo."""
    mock_instance = cast(MagicMock, mock_openai_class.return_value)
    mock_message = MagicMock(
        spec=ChatCompletionMessage, content="Isso é uma categoria nova."
    )
    mock_choice = MagicMock(spec=Choice, message=mock_message)
    mock_completion = MagicMock(spec=ChatCompletion, choices=[mock_choice])
    mock_instance.chat.completions.create.return_value = mock_completion

    service = OpenAIService()
    email_content = "E-mail com conteúdo estranho."
    result = service.classify_email(email_content)
    assert result == "Desconhecido"


@patch("backend.services.openai_service.OpenAI")
def test_classify_email_partial_match(mock_openai_class: Mock):
    """Testa a classificação com uma resposta que contém a categoria mas com texto extra."""
    mock_instance = cast(MagicMock, mock_openai_class.return_value)
    mock_message = MagicMock(
        spec=ChatCompletionMessage, content="A categoria é Produtivo."
    )
    mock_choice = MagicMock(spec=Choice, message=mock_message)
    mock_completion = MagicMock(spec=ChatCompletion, choices=[mock_choice])
    mock_instance.chat.completions.create.return_value = mock_completion

    service = OpenAIService()
    email_content = "E-mail de teste."
    result = service.classify_email(email_content)
    assert result == "Produtivo"
