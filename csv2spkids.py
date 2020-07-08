#Author: Judy Fong and Arnar Freyr Kristinsson
#Description: Create a csv file like in the corpus
#<audio-filename>,<spk-num>,<speaker label> and
#create CSV file on the form: 
#<audio-filename>,<spk-num>,<speaker name>,<speaker label>

def creating_id(spk_type, spkr_number):
        spk_id = '{}{:04}'.format(spk_type,spkr_number)
        return spk_id

def main():
    import csv
    spk_ids = {}
    with open('../reco2spk_num2spk_name.csv') as \
        csvfile, open('../reco2spk_num2spk_label.csv', 'w') as spk_label\
        , open('../reco2spk_num2spk_info.csv', 'w') as spk_info:
        spkreader = csv.reader(csvfile, delimiter=',')
        known_spkr_number = 1
        unknown_spkr_number = 1
        for row in spkreader:
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
    print("The speaker labels have been created.")

if __name__ == '__main__':
    main()