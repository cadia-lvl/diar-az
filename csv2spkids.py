#Author: Judy Fong 
#Description: Convert speaker names to spkids using intermediate files
# might be another way to do this now that the first corpus file exists

def creating_ids(filename, spk_type):
    spk_ids = {}
    with open(filename,'r') as names:
        line_number = 1
        for line in names:
            spk_ids[line.rstrip()] = '{}{:04}'.format(spk_type,line_number)
            line_number = line_number + 1
    return spk_ids

def main():
    import csv
    known_spks = creating_ids('../ided_spk', 'SPK')
    unknown_spks = creating_ids('../unk_spk', 'UNK')
    from itertools import chain
    spk_ids = dict(chain.from_iterable(d.items() for d in (known_spks, unknown_spks)))
    with open('../reco2spk_num2spk_name.csv') as \
        csvfile, open('../reco2spk_num2spk_label.csv', 'w') as spk_label\
        , open('../reco2spk_num2spk_info.csv', 'w') as spk_info:
        spkreader = csv.reader(csvfile, delimiter=',')
        for row in spkreader:
            print(row[0].split("-")[1], row[1], spk_ids[row[2]], sep=',', file=spk_label)
            print(row[0].split("-")[1], row[1], row[2], spk_ids[row[2]], sep=',', file=spk_info)
    print("The speaker labels have been created.")

if __name__ == '__main__':
    ## TODO: pass in arguments with import argparse
    #import argparse
    #parser = argparse.ArgumentParser(description='The arguments need to \
    #be passed in.')
    #parser.add_argument('--spk-file', required=True, help='the path to the file')
    #args = parser.parse_args()
    main()
    # if args.file:
    #     main(args.file)
    # else:
    #     print('A file needs to be given.')
    #     exit(0)
