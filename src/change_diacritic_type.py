import os
import glob
import re


def read_files_from_folder(folder_path):
    files = glob.glob(os.path.join(folder_path, '*.txt'))
    files.sort(key=lambda x: (int(''.join(filter(str.isdigit, os.path.basename(x)))), os.path.basename(x)))

    file_contents = {}

    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents[os.path.basename(file_path)] = file.read()

    return file_contents

def write_files_to_folder(folder_path, file_contents):
    for filename, content in file_contents.items():
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

def main():
    folder_path = 'KeyphraseExtraction_Dataset_RO_Modif'
    file_contents = read_files_from_folder(folder_path)

    for filename, content in file_contents.items():
        modified_content = content.replace('ş', 'ș').replace('ţ', 'ț').replace('Ţ', 'Ț')
        file_contents[filename] = modified_content

    write_files_to_folder(folder_path, file_contents)


if __name__ == "__main__":
    main()
