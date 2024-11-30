import re
import time
import string
import nltk
from nltk import word_tokenize, sent_tokenize

from stopwords import get_stopwords
from model_loading import load_spacy_model


def to_lowercase(text):
    result = ''

    for char in text:
        if char == 'Ă':
            result += 'ă'
        elif char == 'Â':
            result += 'â'
        elif char == 'Î':
            result += 'î'
        elif char == 'Ț':
            result += 'ț'
        elif char == 'Ș':
            result += 'ș'
        elif 'A' <= char <= 'Z':
            result += chr(ord(char) + (ord('a') - ord('A')))
        else:
            result += char

    return result


def clean_text(text):
    text = to_lowercase(text)
    # printable = set(string.printable)
    # text = filter(lambda x: x in printable, text)  # filter funny characters, if any.
    return text


def tokenize(text):
    sentences = sent_tokenize(text)
    tokens = [word for sent in sentences for word in word_tokenize(sent)]
    return tokens


def lemmatize(words):
    nlp = load_spacy_model()

    lemmas = []
    for word in words:
        doc = nlp(word)
        lemmas.extend([to_lowercase(token.lemma_) for token in doc])

    return lemmas


def get_tr_stops():
    punctuations = list(str(string.punctuation))

    stopwords = get_stopwords() + punctuations + ["„", "”", "'", "“", "’", "-", "–", "/", "…", "`", "«", "»", '-']

    return stopwords


def remove_stopwords(text):
    processed_text = []
    stopwords = get_tr_stops()
    for word in text:
        if word not in stopwords:
            processed_text.append(word)

    return processed_text


def create_vocabulary(text):
    vocabulary = list(set(text))
    return vocabulary


def textrank_preprocessing(text):
    # processed_text = remove_stopwords(lemmatize(tokenize(clean_text(text))))
    processed_text = remove_stopwords(tokenize(clean_text(text)))

    return processed_text, create_vocabulary(processed_text)


def phrase_partitioning(text):
    # lemmatized_text = lemmatize(tokenize(clean_text(text)))
    lemmatized_text = tokenize(clean_text(text))

    stopwords = get_tr_stops()

    phrases = []
    phrase = " "

    for word in lemmatized_text:

        if word in stopwords:
            if phrase != " ":
                phrases.append(str(phrase).strip().split())
            phrase = " "
        elif word not in stopwords:
            phrase += str(word)
            phrase += " "

    return phrases


def get_unique_phrases(phrases):
    unique_phrases = []

    for phrase in phrases:
        if phrase not in unique_phrases:
            unique_phrases.append(phrase)

    return unique_phrases


# Remove single word keyphrase candidates that are present in multi-word alternatives
def thin_candidate_keyphrases(unique_phrases, vocabulary):
    for word in vocabulary:
        for phrase in unique_phrases:
            if (word in phrase) and ([word] in unique_phrases) and (len(phrase) > 1):
                # if len(phrase)>1 then the current phrase is multi-worded.
                # if the word in vocabulary is present in unique_phrases as a single-word-phrase
                # and at the same time present as a word within a multi-worded phrase,
                # then I will remove the single-word-phrase from the list.
                unique_phrases.remove([word])

    return unique_phrases


def score_keyphrases(phrases, score, vocabulary):
    phrase_scores = []
    keywords = []
    for phrase in phrases:
        phrase_score = 0
        keyword = ''
        for word in phrase:
            keyword += str(word)
            keyword += " "
            phrase_score += score[vocabulary.index(word)]
        phrase_scores.append(phrase_score)
        keywords.append(keyword.strip())

    return keywords, phrase_scores


def textrank_postprocessing_v1(text, score, vocabulary):
    phrases = phrase_partitioning(text)
    unique_phrases = get_unique_phrases(phrases)
    removed = thin_candidate_keyphrases(unique_phrases, vocabulary)
    return score_keyphrases(removed, score, vocabulary)


def textrank_postprocessing_v2(text, sorted_keywords, keyword_number):
    phrases = phrase_partitioning(text)
    unique_phrases = get_unique_phrases(phrases)

    top_n = sorted_keywords[:keyword_number]
    sorted_keywords = sorted_keywords[keyword_number:]

    final_phrases = []
    while len(final_phrases) < keyword_number:
        final_phrases = []

        for phrase in unique_phrases:
            kp = True
            for word in phrase:
                if word not in top_n:
                    kp = False
                    break
            if kp:
                final_phrases.append(phrase)

        extracted_phrases = thin_candidate_keyphrases(final_phrases, top_n)
        final_phrases = [" ".join(sublist) for sublist in extracted_phrases]

        top_n.extend(sorted_keywords[:1])
        sorted_keywords = sorted_keywords[1:]

    return final_phrases[:keyword_number]

def split_text_into_words(text):
    return re.findall(r'\w+', text.lower())


def extract_candidate_keyphrases(text):
    sentences = re.split(r'[.!?,;:\t\-\"\(\)]', text)
    phrases = []
    stop_words = get_stopwords()
    for sentence in sentences:
        words = split_text_into_words(sentence)
        phrase = []
        for word in words:
            if word in stop_words:
                if phrase:
                    phrases.append(phrase)
                    phrase = []
            else:
                phrase.append(word)
        if phrase:
            phrases.append(phrase)
    return phrases
