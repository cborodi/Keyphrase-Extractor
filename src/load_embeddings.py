import numpy as np
from gensim.models import KeyedVectors


def load_embeddings(file_path):
    embeddings = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            word = parts[0]
            vector = parts[1:]

            # Skip lines where the vector length is not 300
            if len(vector) != 300:
                continue

            try:
                vector = np.array(vector, dtype=float)
                embeddings[word] = vector
            except ValueError as e:
                print(f"Skipping word '{word}' due to error: {e}")

    return embeddings


def convert_to_keyed_vectors(embeddings_dict):
    word_vectors = KeyedVectors(vector_size=len(next(iter(embeddings_dict.values()))))
    words = list(embeddings_dict.keys())
    vectors = np.array(list(embeddings_dict.values()))
    word_vectors.add_vectors(words, vectors)
    return word_vectors


def get_word_vectors():
    file_path = 'corola.300.50.vec'
    embeddings_dict = load_embeddings(file_path)
    word_vectors = convert_to_keyed_vectors(embeddings_dict)
    return word_vectors

