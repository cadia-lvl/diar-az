# Author: Judy Fong
# Description: Validate data directories. Check to make sure that each audio
# /recording file has only one rttm,srt,csv, and json file.

#validates files given a list contents of a directory and a file type
def validate(dircontents, dirname, recordingIds):
    total = {}
    for rId in recordingIds:
        total[rId] = 0
    for filename in dircontents:
        for rId in recordingIds:
            if rId in filename:
                total[rId] = total[rId]+1
                # Using the episode list check if a directory has multiple
                # files of the same name,
                # TODO:  DEFAULT just remove it from the episode list
                # USER OPTION: inform user if an audio file has multiple files
                # and exit
                if total[rId] > 1:
                    print('{} has multiple files in {}'.format(rId, dirname))
                    exit(1)
    # Check for audiofiles without text files
    for rId, count in total.items():
        if count == 0:
            print('{} does not exist in {}'.format(rId, dirname))
            recordingIds.remove(rId)
    return recordingIds


# Validates json, rttm, csv and srt directories
# and returns list of good recording ids
def validateDataDirs(recordingIds):
    import os
    json = 'data/gecko/json'
    rttm = 'data/gecko/corrected_rttm'
    segments = 'data/gecko/srt'
    csv = 'data/gecko/csv'
    validRecordingIds = []

    if os.path.exists(json):
        json_files = os.listdir(json)
        validRecordingIds.append(validate(json_files, json, recordingIds))

    if os.path.exists(rttm):
        rttm_files = os.listdir(rttm)
        validRecordingIds.append(validate(rttm_files, rttm, recordingIds))

    if os.path.exists(segments):
        srt_files = os.listdir(segments)
        validRecordingIds.append(validate(srt_files, segments, recordingIds))

    if os.path.exists(csv):
        csv_files = os.listdir(csv)
        validRecordingIds.append(validate(csv_files, csv, recordingIds))

    # Get the list of recordings which have one srt, rttm, csv, and json file
    # This becomes the final recording list
    recordingIds = list(set.intersection(
        *[set(x) for x in validRecordingIds]))
    recordingIds.sort()
    return recordingIds

def main(filename):
    import os

    with open(filename) as f:
        recordingIds = [line.rstrip('\n') for line in f]
    recordingIds = validateDataDirs(recordingIds)
    with open(filename, 'w') as f:
        print(*recordingIds, sep='\n', file=f)

if __name__ == '__main__':
    # Pass in arguments with import argparse
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
