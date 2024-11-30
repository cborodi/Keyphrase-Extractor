import os
import re
from collections import defaultdict


def extract_content(text):
    # Regular expression to match content within square brackets
    matches = re.findall(r'\[\s*"?(.*?)"?\s*\]', text)
    return matches


def process_files(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Dictionary to hold content for each prefix
    content_dict = defaultdict(list)

    for filename in os.listdir(source_folder):
        if filename.endswith('.txt'):
            prefix = filename.split('_')[0]
            source_file_path = os.path.join(source_folder, filename)
            with open(source_file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            extracted_content = extract_content(content)
            content_dict[prefix].extend(extracted_content)

    # Write combined content to respective files in the destination folder
    for prefix, content_list in content_dict.items():
        destination_file_path = os.path.join(destination_folder, f"{prefix}.txt")
        with open(destination_file_path, 'w', encoding='utf-8') as file:
            for item in content_list:
                file.write(item + '\n')


source_folder = 'ManuallyExtracted'
destination_folder = 'ExpertKeyphrases_merge'

process_files(source_folder, destination_folder)
