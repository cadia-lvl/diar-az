# Author: Judy Fong (Reykjavik University)
# Description:
# Create segments file from subtitle timestamps
# create a corresponding text file
# create a single segment for each timestamp set

# TODO: normalize the text
# TODO: create corpus file
from itertools import groupby
from decimal import *

# Convert timestamps to seconds and partial seconds so hh:mm:ss.ff
def time_in_seconds(a_time):
    hrs, mins, secs = a_time.split(':')
    return Decimal(hrs)*3600+Decimal(mins)*60+Decimal(secs.replace(",","."))

def no_transcripts(subtitle_path):
    import os
    HEADER_ONLY = 10
    ACCESS_ERROR_ONLY = 36 
    return os.stat(subtitle_path).st_size in (HEADER_ONLY, ACCESS_ERROR_ONLY)

def main(subtitle_filename):
    import os
    
    if no_transcripts(subtitle_filename):
        print('{} is presumed to not have transcripts'.format(subtitle_filename))
    else:
        base = os.path.basename(subtitle_filename)
        (filename, ext) = os.path.splitext(base.replace("_",""))
        show_title = os.path.basename(os.path.dirname(subtitle_filename))

        if not os.path.exists('data/' + show_title):
            os.makedirs('data/' + show_title)
        
        if not os.path.exists('data/' + show_title + '/' + filename):
            os.makedirs('data/' + show_title + '/' + filename)
        
        with open(subtitle_filename, 'r') as fin, open('data/' + show_title + '/' + filename + '/' + filename + '_segments', 'w') as seg, open('data/' + show_title + '/' + filename + '/' + filename + '_text', 'w') as trans:
            # skip header(first two) lines in file
            if (ext == '.vtt'):
                next(fin)
                next(fin)
            groups = groupby(fin, str.isspace)
            count = 0
            for (segment, *rest) in (map(str.strip, v) for  g, v in groups if not g):
                # write to text file
                # better to create individual speaker ids per episode or shows, more speaker ids, because a global one would create problems for cepstral mean normalization ineffective in training
                print("{}-{}_{:05d}".format(show_title, filename, count) , *rest[1:], sep=' ', file=trans)
                if (ext == '.vtt'):
                    start_time, arrow, end_time, position = (str(*rest[:1])).split(' ', 3)
                elif (ext == '.srt'):
                    start_time, arrow, end_time = (str(*rest[:1])).split(' ', 2)
                else:
                    print("The file was not recognized as a subtitle file(\
                            .vtt or .srt).")
                    exit(1)
                start_seconds = time_in_seconds(start_time)
                end_seconds = time_in_seconds(end_time)
                # write to segments file
                seg.write('unknown-{}_{:05d} unknown-{} {} {}\n'.format(filename, count, filename, start_seconds, end_seconds))
                count = count + 1

if __name__ == '__main__':
    # TODO: pass in filename as argument with import argparse
    import argparse
    parser = argparse.ArgumentParser(description='Create ASR segments and \
        text files from a subtitle file')
    parser.add_argument('--subtitle-file', required=True, help='the path to the subtitle file')
    args = parser.parse_args()
    if args.subtitle_file:
        main(args.subtitle_file)
    else:
        print('A subtitle file needs to be given.')
        exit(0)