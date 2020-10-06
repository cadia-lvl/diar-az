#Author: Judy Fong
#Description:

#validates files given a list contents of a directory and a file type
def validate(dircontents, dirname, recordingIds):
    # check = all(ids in recordingIds for filename in dircontents)
    total = {}
    for rId in recordingIds:
        total[rId] = 0
    for filename in dircontents:
        for rId in recordingIds:
            if rId in filename:
                total[rId] = total[rId]+1
                if total[rId] > 1:
                    print('{} has multiple files in {}'.format(rId, dirname))
                    exit(1)
    # look for audiofiles without text files
    for rId, count in total.items():
        if count == 0:
            print('{} does not exist in {}'.format(rId, dirname))
            exit(1)

#validates json, rttm, csv and srt directories
def validateDataDirs(recordingIds):
    import os
    json = 'data/gecko/json'
    rttm = 'data/gecko/corrected_rttm'
    segments = 'data/gecko/srt'
    csv = 'data/gecko/csv'

    if os.path.exists(json):
        json_files = os.listdir(json)
        validate(json_files, json, recordingIds)

    if os.path.exists(rttm):
        rttm_files = os.listdir(rttm)
        validate(rttm_files, rttm, recordingIds)

    if os.path.exists(segments):
        srt_files = os.listdir(segments)
        validate(srt_files, segments, recordingIds)


def main(filename):
    # TODO: using the episode list check if a directory has multiple files of the
    # same name, if so, ask the user which file to keep
    # check if any of the episodes are missing files
    import os

    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # print('working directory is {}'.format(dir_path))

    with open(filename) as f:
        recordingIds = [line.rstrip('\n') for line in f]
    validateDataDirs(recordingIds)

if __name__ == '__main__':
    # TODO: pass in arguments with import argparse
    import argparse
    parser = argparse.ArgumentParser(description='''A text file with the list of
                                                    recording names''')
    parser.add_argument('--recordings', '-r',
                        required=True,
                        help='''the path to the recordings list file''')
    args = parser.parse_args()
    if args.recordings:
        main(args.recordings)
    else:
        print('A file needs to be given.')
        exit(0)
