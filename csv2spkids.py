# Author: Judy Fong and Arnar Freyr Kristinsson
# Description: Create a csv file like in the corpus
# <audio-filename>,<spk-num>,<speaker label> and
# create CSV file on the form:
# <audio-filename>,<spk-num>,<speaker name>,<speaker label>
# Install python-Levenshtein for detecting spelling mistakes: pip3 install python-Levenshtein

from Levenshtein import distance
from collections import Counter

#creates an id
def creating_id(spk_type, spkr_number):
        spk_id = '{}{:04}'.format(spk_type, spkr_number)
        return spk_id

#Sometimes, as in the case when the names are very similar, 
# the script will correct spelling mistakes when it isn't supposed to do so.
#So manual verification is needed, but only for these lines 
# that actually may have spelling errors
def manual_correction(old_name, new_name):
    if(old_name == new_name):
        return new_name

    print("Type in enter if the correction is correct, otherwise type in the correct name")
    name = input("{} will be corrected to: {} ".format(old_name, new_name))
    if(name == ""):
        return new_name
    else:
        return name

#Corrects a name to have uppercase or lower case where appropriate
def name_to_capital(name):
    full_name = name.split()
    index = 0
    for name in full_name:
        full_name[index] = (name[0].upper()) + (name[1:].lower())
        index = index + 1
    return " ".join(full_name)

# Corrects spelling mistakes depending on which possible misspelled name appears the most often
def correct_spelling_mistakes(row, contents, corrected):
    name = row[1][2]
    name = name_to_capital(name)
    tmp_names = {}
    tmp_names[row[0]] = name
    contents.sort()
    for other_name in enumerate(contents):
        if(distance(name, other_name[1][2]) >= 0 and distance(name, other_name[1][2]) <= 3):
            tmp_names[other_name[0]] = other_name[1][2]
    most_common = Counter(tmp_names.values()).most_common(1)[0]
    most_common = name_to_capital(most_common[0])
    
    if(name not in corrected):
        row[1][2] = manual_correction(name, most_common)
    else:
        row[1][2] = most_common
    return (name, row[1][2], row)

def main(name_file, correct_spelling):
    import csv
    spk_ids = {}
    with open(name_file) as \
        csvfile, open('../reco2spk_num2spk_label.csv', 'w') as spk_label, open('../reco2spk_num2spk_info.csv', 'w') as spk_info:
        spkreader = csv.reader(csvfile, delimiter=',')
        known_spkr_number = 1
        unknown_spkr_number = 1
        contents = []
        episodes = []
        episode = None
        unknown = None
        unk_num = 1
        corrected = {}

        for row in spkreader:
            contents.append(row)

        for row in enumerate(contents):
            name = row[1][2]
            recording_id = row[1][0]
            spk_num = row[1][1]
            if(name.split()[0] != "Unknown"):
                if(correct_spelling == "True"):   
                    correction = correct_spelling_mistakes(row, contents, corrected)
                    old_name =  correction[0]
                    new_name = correction[1]
                    corrected[old_name] = new_name
                    name = new_name
                if(name not in spk_ids):
                    spk_ids[name] = creating_id("SPK", known_spkr_number)
                    known_spkr_number = known_spkr_number + 1
                print(recording_id.split("-")[1], spk_num, spk_ids[name], sep=',', file=spk_label)
                print(recording_id.split("-")[1], spk_num, name, spk_ids[name], sep=',', file=spk_info)
            else:
                if(correct_spelling == "True"):  
                    episode = recording_id.split("-")[1]
                    episodes.sort()
                    if(episode in episodes):
                        unknown_spkr_number = unknown_spkr_number + 1
                    else:
                        episodes.append(episode)
                        unknown_spkr_number = 1
                unknown = "Unknown {0:0=2d}".format(unknown_spkr_number)
                print(recording_id.split("-")[1], spk_num, unknown, creating_id("UNK", unk_num ), sep=',', file=spk_info)
                print(recording_id.split("-")[1], spk_num, unknown, creating_id("UNK", unknown_spkr_number), sep=',', file=spk_label)
                unk_num = unk_num + 1
           
    if(correct_spelling == "True"):
        print("Spelling mistakes have been corrected.")
    print("The speaker labels have been created.")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='The arguments need to be passed in.')
    parser.add_argument('--file', default= "../reco2spk_num2spk_name.csv", help='the path to the file')
    parser.add_argument('--correct_spelling', default="True", help='correct spelling mistakes on or off (True on False off)')
    args = parser.parse_args()
    main(args.file, args.correct_spelling)