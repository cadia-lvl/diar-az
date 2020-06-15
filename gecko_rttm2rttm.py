# Author: Reykjavik University (Judy Fong <judyfong@ru.is>)
# Description: Convert gecko rttm files to also have recordingids in the first
# <NA>

def main(gecko_rttm):
    import os
    base = os.path.basename(gecko_rttm)
    (filename, ext) = os.path.splitext(base.replace("_",""))
    with open(gecko_rttm , 'r') as gecko_file, open('rttm/'+ base, 'w') \
        as rttm_file:
        for line in gecko_file:
            print(line.rstrip().replace('<NA>', filename, 1), end='\n',
            file=rttm_file)
    print("The recording ids have been added to {}.".format(base))

if __name__ == '__main__':
    ## TODO: pass in arguments with import argparse
    import argparse
    parser = argparse.ArgumentParser(description='The arguments need to \
    be passed in.')
    parser.add_argument('--rttm', required=True, help='the path to the rttm file')
    args = parser.parse_args()
    if args.rttm:
        main(args.rttm)
    else:
        print('A file needs to be given.')
        exit(0)
