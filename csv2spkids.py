# Author: Judy Fong and Arnar Freyr Kristinsson
# Description: Create a csv file like in the corpus
# <audio-filename>,<spk-num>,<speaker label> and
# create CSV file on the form:
# <audio-filename>,<spk-num>,<speaker name>,<speaker label>
# Install python-Levenshtein for detecting spelling mistakes: pip3 install python-Levenshtein

from Levenshtein import distance
from collections import Counter
import numpy as np


def creating_id(spk_type, spkr_number):
        spk_id = '{}{:04}'.format(spk_type, spkr_number)
        return spk_id

# Corrects spelling mistakes depending on which possible misspelled name appears the most often
def correct_spelling_mistakes(row, contents):
    name = row[1][2]
    tmp_names = {}
    tmp_names[row[0]] = name
    for other_name in enumerate(contents):
        if(distance(name, other_name[1][2]) >= 0 and distance(name, other_name[1][2]) <= 3):
            tmp_names[other_name[0]] = other_name[1][2]

    most_common = Counter(tmp_names.values()).most_common(1)[0]
    for line, name in tmp_names.items():
        row[1][2] = most_common[0]
    return row


def main():
    import csv
    spk_ids = {}
    with open('../reco2spk_num2spk_name.csv') as \
        csvfile, open('../reco2spk_num2spk_label.csv', 'w') as spk_label, open('../reco2spk_num2spk_info.csv', 'w') as spk_info:
        spkreader = csv.reader(csvfile, delimiter=',')
        known_spkr_number = 1
        unknown_spkr_number = 1
        spkr_names = []
        contents = []

        for row in spkreader:
            contents.append(row)

        for row in enumerate(contents):
            correct_spelling_mistakes(row, contents)
            row = row[1]
            if(row[2].split()[0] == "Unknown"):
                print(row[0].split("-")[1], row[1], row[2],creating_id("UNK", unknown_spkr_number), sep=',', file=spk_info)
                print(row[0].split("-")[1], row[1],creating_id("UNK", unknown_spkr_number), sep=',', file=spk_label)
                unknown_spkr_number = unknown_spkr_number + 1
            else: 
                if(row[2] not in spk_ids):
                    spk_ids[row[2]] = creating_id("SPK", known_spkr_number)
                    known_spkr_number = known_spkr_number + 1
                print(row[0].split("-")[1], row[1],spk_ids[row[2]], sep=',', file=spk_label)
                print(row[0].split("-")[1], row[1], row[2],spk_ids[row[2]], sep=',', file=spk_info)

    print("Spelling mistakes have been corrected.")
    print("The speaker labels have been created.")

if __name__ == '__main__':
    main()
