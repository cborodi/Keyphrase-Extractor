from text_processing import extract_candidate_keyphrases

from collections import defaultdict
import re
from collections import Counter
from itertools import chain


def calculate_word_scores(phrases):
    word_freq = Counter(chain(*phrases))

    word_degree = Counter()
    for phrase in phrases:
        degree = len(phrase)
        for word in phrase:
            word_degree[word] += degree
    word_scores = {word: word_degree[word] / word_freq[word] for word in word_freq}
    return word_scores


def calculate_phrase_scores(phrases, word_scores):
    phrase_scores = {}
    for phrase in phrases:
        phrase_score = sum(word_scores[word] for word in phrase)
        phrase_scores[" ".join(phrase)] = phrase_score
    return phrase_scores


def RAKE(text, keyword_number=4):
    phrases = extract_candidate_keyphrases(text)
    word_scores = calculate_word_scores(phrases)
    phrase_scores = calculate_phrase_scores(phrases, word_scores)
    sorted_phrases = sorted(phrase_scores.items(), key=lambda x: x[1], reverse=True)

    final_keyphrases = [phrase[0] for phrase in sorted_phrases]
    return final_keyphrases[:keyword_number]
