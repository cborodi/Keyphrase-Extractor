from text_processing import *

import numpy as np
import math


WINDOW_SIZE = 4


def build_graph(processed_text, vocabulary):
    vocab_len = len(vocabulary)

    weighted_edge = np.zeros((vocab_len, vocab_len), dtype=np.float32)

    score = np.zeros((vocab_len), dtype=np.float32)
    window_size = WINDOW_SIZE
    covered_coocurrences = []

    for i in range(0, vocab_len):
        score[i] = 1
        for j in range(0, vocab_len):
            if j == i:
                weighted_edge[i][j] = 0
            else:
                for window_start in range(0, (len(processed_text) - window_size + 1)):

                    window_end = window_start + window_size

                    window = processed_text[window_start:window_end]

                    if (vocabulary[i] in window) and (vocabulary[j] in window):

                        index_of_i = window_start + window.index(vocabulary[i])
                        index_of_j = window_start + window.index(vocabulary[j])

                        # index_of_x is the absolute position of the xth term in the window
                        # (counting from 0)
                        # in the processed_text

                        if [index_of_i, index_of_j] not in covered_coocurrences:
                            weighted_edge[i][j] += 1 / math.fabs(index_of_i - index_of_j)
                            covered_coocurrences.append([index_of_i, index_of_j])

    inout = np.zeros((vocab_len), dtype=np.float32)

    for i in range(0, vocab_len):
        for j in range(0, vocab_len):
            inout[i] += weighted_edge[i][j]

    return score, weighted_edge, inout, vocab_len


def pake_rank(score, weighted_edge, inout, vocab_len):
    MAX_ITERATIONS = 50
    d = 0.85
    threshold = 0.0001  # convergence threshold

    for iter in range(0, MAX_ITERATIONS):
        prev_score = np.copy(score)

        for i in range(0, vocab_len):

            summation = 0
            for j in range(0, vocab_len):
                if weighted_edge[i][j] != 0:
                    summation += (weighted_edge[i][j] / inout[j]) * score[j]

            score[i] = (1 - d) + d * (summation)

        if np.sum(np.fabs(prev_score - score)) <= threshold:  # convergence condition
            break

    return score


def rank_keyphrases(keywords, phrase_scores, keyword_number):
    sorted_index = np.flip(np.argsort(phrase_scores), 0)

    keywords_num = keyword_number
    final_keywords = []

    for i in range(0, keywords_num):
        final_keywords.append(keywords[sorted_index[i]])

    return final_keywords


def TextRank(text, keyword_number=4):
    processed_text, textrank_vocabulary = textrank_preprocessing(text)

    score, weighted_edge, inout, vocab_len = build_graph(processed_text, textrank_vocabulary)

    score = pake_rank(score, weighted_edge, inout, vocab_len)

    # ## v1
    # keywords, phrase_scores = textrank_postprocessing_v1(text, score, textrank_vocabulary)
    #
    # return rank_keyphrases(keywords, phrase_scores, keyword_number)

    ## v2
    ranked_keywords = []
    for i in range(0, vocab_len):
        ranked_keywords.append((textrank_vocabulary[i], score[i]))

    sorted_keywords = sorted(ranked_keywords, key=lambda x: x[1], reverse=True)
    sorted_keywords = [elem[0] for elem in sorted_keywords]

    return textrank_postprocessing_v2(text, sorted_keywords, keyword_number)
