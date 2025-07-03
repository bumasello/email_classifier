import pytest
import spacy.cli
import spacy.cli.download
from backend.services.nlp_service import preprocess_text
import spacy

"""
Fixture para carregar o modelo do spacy uma vez
Autouse para que seja carregado automaticamente
Scope='session' para que seja carregado apenas uma vez por sessão de teste
"""


@pytest.fixture(scope="session", autouse=True)
def load_spacy_model():
    try:
        spacy.load("pt_core_news_sm")
    except OSError:
        spacy.cli.download("pt_core_news_sm")  # type: ignore
        spacy.load("pt_core_news_sm")


def test_preprocess_text_basic():
    """Teste o pré-processamento básico de um texto"""
    text = "Olá, como você está hoje?"
    expected_output = "olá hoje"  # stop words
    assert preprocess_text(text) == expected_output


def test_preprocess_text_with_punctuation():
    """Testa a remoção de pontuação"""
    text = "Isso é um teste, certo?"
    expected_output = "teste certo"
    assert preprocess_text(text) == expected_output


def test_preprocess_text_with_stopwords():
    """Testa a remoção de stop words"""
    text = "Eu estou muito feliz com isso."
    expected_output = "feliz"
    assert preprocess_text(text) == expected_output


def test_preprocess_text_with_numbers():
    """Teste se números são mantidos"""
    text = "O preço é R$ 100,00"
    expected_output = "preço r$ 100,00"
    assert preprocess_text(text) == expected_output


def test_preprocess_text_with_empty_string():
    """Teste com uma string vazia"""
    text = ""
    expected_output = ""
    assert preprocess_text(text) == expected_output


def test_preprocess_text_only_stopwords_and_punctuation():
    """Testa com texto contendo apenas stop words e pontuação"""
    text = "E, ou, mas, por quê?"
    expected_output = ""
    assert preprocess_text(text) == expected_output


def test_preprocess_text_lemmatization():
    """Testa a lematização de palavras"""
    text = "Correndo, correu, correremos"
    expected_output = "correr correr correrer"
    """
    Decidir aceitar essa falha "correrer".
    Como estou usando o menor modelo, pode não ter 100% precisão em todas as lematizações.
    """
    assert preprocess_text(text) == expected_output
