import os
import Levenshtein

from load_embeddings import get_word_vectors


def read_keywords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        keywords = {line.strip().lower() for line in file}
    return keywords


def is_similar_lev(word1, word2, threshold=0.75):
    return Levenshtein.ratio(word1, word2) >= threshold


def is_similar_we(word1, word2, word_vectors, threshold=0.75):
    try:
        cosine_similarity = word_vectors.similarity(word1, word2)
        if cosine_similarity > threshold:
            print(word1, word2)
            return True
        return False
    except:
        return is_similar_lev(word1, word2)


def find_similar_keywords(extracted_keywords, expert_keywords, word_vectors):
    matched_keywords = set()
    for ek in extracted_keywords:
        for expk in expert_keywords:
            if is_similar_lev(ek, expk):
                matched_keywords.add(ek)
                break
    return matched_keywords


def evaluate_keywords(extracted_folder, expert_folder):
    file_scores = []
    total_correct = 0
    total_extracted = 0
    total_expert = 0
    word_vectors = get_word_vectors()

    for filename in os.listdir(extracted_folder):
        if filename.endswith('.txt'):
            extracted_file_path = os.path.join(extracted_folder, filename)
            expert_file_path = os.path.join(expert_folder, filename)

            if os.path.exists(expert_file_path):
                extracted_keywords = read_keywords(extracted_file_path)
                expert_keywords = read_keywords(expert_file_path)

                correct_keywords = find_similar_keywords(extracted_keywords, expert_keywords, word_vectors)
                num_correct = len(correct_keywords)
                num_extracted = len(extracted_keywords)
                num_expert = len(expert_keywords)

                precision = num_correct / num_extracted if num_extracted > 0 else 0
                recall = num_correct / num_expert if num_expert > 0 else 0
                f1_score = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0

                file_scores.append((filename, precision, recall, f1_score))

                total_correct += num_correct
                total_extracted += num_extracted
                total_expert += num_expert

    overall_precision = total_correct / total_extracted if total_extracted > 0 else 0
    overall_recall = total_correct / total_expert if total_expert > 0 else 0
    overall_f1_score = (2 * overall_precision * overall_recall / (overall_precision + overall_recall)) if (overall_precision + overall_recall) > 0 else 0

    return file_scores, overall_precision, overall_recall, overall_f1_score


def print_results(file_scores, overall_precision, overall_recall, overall_f1_score):
    # print("File-wise Scores:")
    # for filename, precision, recall, f1_score in file_scores:
        # print(f"{filename} - Precision: {precision:.2%}, Recall: {recall:.2%}, F1 Score: {f1_score:.2%}")

    print("\nOverall Scores:")
    print(f"Precision: {overall_precision:.2%}")
    print(f"Recall: {overall_recall:.2%}")
    print(f"F1 Score: {overall_f1_score:.2%}")


extracted_folder = 'KeyphraseExtraction_Results_RO_TR_Lemma_Comp'
expert_folder = 'ExpertKeyphrases_merge'

file_scores, overall_precision, overall_recall, overall_f1_score = evaluate_keywords(extracted_folder, expert_folder)
print_results(file_scores, overall_precision, overall_recall, overall_f1_score)
