import os
import glob
import re


from TextRank import TextRank
from RAKE import RAKE


def read_files_from_folder(folder_path):
    files = glob.glob(os.path.join(folder_path, '*.txt'))
    files.sort(key=lambda x: (int(''.join(filter(str.isdigit, os.path.basename(x)))), os.path.basename(x)))

    file_contents = {}

    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents[os.path.basename(file_path)] = file.read()

    return file_contents


def write_array_to_file(filename, array):
    with open(filename, 'w', encoding='utf-8') as file:
        for element in array:
            file.write(str(element) + '\n')


def main():
    folder_path = 'test' # 'KeyphraseExtraction_Dataset_RO'
    file_contents = read_files_from_folder(folder_path)

    for filename, content in file_contents.items():
        keyword_number = 4 # len(content.split()) // 100 + 1
        print(filename)
        tr = TextRank(content, keyword_number)
        print(tr)
        # write_array_to_file("KeyphraseExtraction_Results_RO_TR_Lemma_Comp/" + filename, tr)
        rk = RAKE(content, keyword_number)
        print(rk)
        # write_array_to_file("KeyphraseExtraction_Results_RO_RAKE/" + filename, rk)


if __name__ == "__main__":
    main()

"""
Inteligența artificială (IA) este un domeniu al informaticii care se ocupă cu dezvoltarea de sisteme capabile să 
îndeplinească sarcini care necesită inteligență umană. Aceste sarcini includ recunoașterea vorbirii, luarea deciziilor, 
traducerea limbilor și recunoașterea vizuală. Inteligența artificială utilizează algoritmi de învățare automată, rețele 
neuronale și procesarea limbajului natural pentru a obține aceste rezultate.
"""