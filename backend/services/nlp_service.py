import spacy
import spacy.cli
import spacy.cli.download

try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    print(
        "Modelo 'pt_core_news_sm' não encontrado. Rodando 'python -m spacy download pt_core_news_sm'"
    )
    spacy.cli.download("pt_core_news_sm")  # type: ignore
    nlp = spacy.load("pt_core_news_sm")


def preprocess_text(text: str) -> str:
    """
    Realiza o pré-processamento de texto usando spacy
    Inclui tokenização, remoção de stop words e lematização
    """

    doc = nlp(text.lower())  # Converte e processa com spacy

    processed_tokens = [
        token.lemma_.lower()
        for token in doc
        if not token.is_punct and not token.is_space and not token.is_stop
    ]

    return " ".join(processed_tokens)
