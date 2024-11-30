import spacy


def load_spacy_model():
    try:
        nlp = spacy.load("ro_core_news_sm")
    except OSError:
        from spacy.cli import download
        download("ro_core_news_sm")
        nlp = spacy.load("ro_core_news_sm")
    return nlp
