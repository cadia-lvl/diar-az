# Authors: Reykjavik University (Judy Fong <judyfong@ru.is>) and (Arnar Freyr Kristinsson <arnark17@ru.is> )
# Description: This script does several things.
# 1. Convert gecko rttm files to also have recordingids in the first <NA>,
#    adds audio filenames to rttm files as the second field,
# 2. remove [] stuff (foreign, noise, music) from rttm files where there is a
#    [something]+number,
# 3. renames the rttm/json/srt files to just the audio filename
# 4. and calls the create_segments_and_text.py
# All fields are optional: --rrtm, --srt or --subtitle-file
# If no arguments are provided the script will only rename the corresponding
# files if they exist and update the readme file

from decimal import *
from create_segments_and_text import create_segm_and_text

# Removes [something]+number (speaker number) and number+[something] - rttm files
# Remove segments which are only [] stuff
# Identify segments which have no speaker label
# Identify files which have non-numeric speaker ids
def rm_brckts_spker_rttm(line, audiofilename):

    if(line != '\n'):
        spkridOrBracketStuff = line.split()[7]
        endbrackpos = line.find("]")
        bgnbrackpos = line.find("[")

        if "]+" in spkridOrBracketStuff:
            removed = line.replace ( line[ bgnbrackpos : endbrackpos+2 ], "")
            return removed
        elif "+[" in spkridOrBracketStuff:
            removed = line.replace ( line[ bgnbrackpos-1 : endbrackpos+2 ], " ")
            return removed
        elif "[" in spkridOrBracketStuff:
            return None
        elif "<NA>" in spkridOrBracketStuff:
            print("<NA> found as speaker in {}".format(audiofilename))
        elif spkridOrBracketStuff.isnumeric():
            return line
        else:
            print("{} found as speaker in {}".format(spkridOrBracketStuff, audiofilename))

# Convert timestamps to seconds and partial seconds ss.ff
def cnvrt_hh_mm_sec(hh_mm_ss):
    hh, m, s = hh_mm_ss.split(':')
    return ( int(hh) * 3600 ) + ( int(m) * 60) + Decimal(s.replace(",","."))

# Checks if a string is a timestamp
def is_srt_tmstmp(tmstamp):
    mintmstamplen = 8 # 00:00:00 (hh:mm:ss) - minimum timestamp length
    if (len (tmstamp) >= mintmstamplen):
        if(tmstamp[0:2].isnumeric() and tmstamp[2] == ':' and tmstamp[3:5].isnumeric() \
                    and tmstamp[5] == ':' and tmstamp[6:8].isnumeric() \
                    and tmstamp[9:].isnumeric() ):
            return True
    return False

# Check if there is some speech in the rttm file at specific segment
def is_speech_rttm(srt_line, rttm_lines):
    if(tmstmp_scnds(srt_line) != []):
        srt_range = tmstmp_scnds(srt_line)
        for rttm_line in rttm_lines:
            rttm_bgn_tm = rttm_line.split()[3]
            rttm_spkr = rttm_line.split()[7]
            if( Decimal(rttm_bgn_tm) >= srt_range[0] and Decimal(rttm_bgn_tm) < Decimal(str(srt_range[1])) ):
                if(rttm_spkr.isnumeric()):
                    return True
    return False
# Returns the timestamps in seconds to compare the srt file to the rttm file to
# remove the correct segments with no speech in it.
def tmstmp_scnds(line):
      fstcol = line.split("\n")[0].split(' ')[0]
      lstcol = line.split("\n")[0].split(' ')[-1]
      arrow = "-->"
      # Find the correct line (a line that has a timestamp)
      if( is_srt_tmstmp(fstcol) and is_srt_tmstmp(lstcol)):
        expln = fstcol + " " + arrow + " " + lstcol
        if(expln == line[:-1]):
            return [ cnvrt_hh_mm_sec(fstcol), cnvrt_hh_mm_sec(lstcol) ]
      return []

# Gets the audio filename
# NOTE: this function fails if the files were in an windows archive and
# unzipped to a linux machine without specifying the encoding of the original
# archive
def get_audio_filename(filename, os):
    base = os.path.basename(filename)
    (filename, ext) = os.path.splitext(base)
    if ("_" in filename and "-" in filename):
        audiofilename = filename.split("_")[0].split("-")[1]
        return audiofilename+ext
    elif ("-" in filename):
        audiofilename = filename.split("-")[1]
        return audiofilename+ext
    else:
        return filename+ext

# Renames files given a list contents of a directory and a file type
def rename(dircontents, dirname, os):
    for filename in dircontents:
        audiofilename = get_audio_filename(filename, os)
        os.rename(dirname+"/"+filename, dirname+"/"+audiofilename)
        (fl, ext) = os.path.splitext(filename)
        print("The file {} has been renamed to {}".format(filename, audiofilename))

# Renames Json, Rttm and srt files
def rnm_json_rttm_srt(os):
    json = 'data/temp/json'
    rttm = 'data/temp/rttm'
    srt = 'data/temp/srt'

    if os.path.exists(json):
        json_files = os.listdir(json)
        rename(json_files, json, os)

    if os.path.exists(rttm):
        rttm_files = os.listdir(rttm)
        rename(rttm_files, rttm, os)

    if os.path.exists(srt):
        srt_files = os.listdir(srt)
        rename(srt_files, srt, os)

# Checks the given arguments and calls the corresponding function
def checkArguments(args):
    if args.only_csv == 'True':
        create_csv(args.create_csv)

        if args.statistics_off == 'False':
            create_statistics(args.statistics)

        if args.update_ruv_di_readme_off == 'False':
            update_ruv_di_readme(args.ruv_di_readme, "Statistics", args.statistics)
        exit(0)

# Trims the srt file - removes segments that don't have any speech
# Renumbers srt segments
# The correct segment is removed even if there are 2 segments in the rttm file
# for one segment in the srt file
def trim_srt(gecko_srt, srt_folder, rttm_lines, os):
    base = os.path.basename(gecko_srt)
    segment_id = 0
    segment = ""
    if not os.path.exists(srt_folder):
        os.mkdir(srt_folder)
    with open(srt_folder+gecko_srt, 'r') as gecko_srt_file:
        for line in gecko_srt_file:
                if is_speech_rttm(line, rttm_lines):
                    segment_id = segment_id + 1
                    segment = segment + str(segment_id) + "\n" + line + "<NA>\n\n"

    with open(srt_folder+gecko_srt, 'w') as srt_file:
        print(segment, end='\n', file=srt_file)
    print("The file {} has been trimmed of non-speech segments".format(base))

# Removes []+number stuff and number+[] stuff
def trim_rttm(gecko_rttm, rttm_folder, os):
    base = os.path.basename(gecko_rttm)
    contents = ""
    (audiofilename, ext) = os.path.splitext( get_audio_filename(gecko_rttm, os) )
    (filename, ext) = os.path.splitext(base.replace("_",""))
    if not os.path.exists(rttm_folder):
        os.mkdir(rttm_folder)
    with open(rttm_folder+gecko_rttm, 'r') as rttm_file:
        for line in rttm_file:
            line = rm_brckts_spker_rttm(line, audiofilename)
            if(line != None):
                # Replace second field of the rttm files to the audiofilename
                second_field = line.split()[1]
                line = line.replace(second_field, audiofilename, 1)
                contents = contents + line

    with open(rttm_folder+gecko_rttm, 'w') as rttm_file:
        print(contents, end='\n', file=rttm_file)
    print("The file {} has been trimmed".format(base))
    return contents.split('\n')[:-1]

# Creates the csv file
def create_csv(csv_filename):
    import csv2spkids # The csv script used to create the csv file
    csv2spkids.main(csv_filename, 'data/corpus/', "True")
    print("CSV file have been created")

def total_speech_time():
    import os
    total = 0
    segment_time = 0
    srt_folder = "data/temp/srt"
    srt_files = os.listdir(srt_folder)
    segment_time = [] # For sorting segment time for correct subtraction
    segment_cnt = 0
    fstcol = None
    lstcol = None

    for srt_segment_file in srt_files:
        with open(srt_folder+"/"+srt_segment_file) as srt_file:
            for line in srt_file:
                fstcol = line.split("\n")[0].split(' ')[0]
                lstcol = line.split("\n")[0].split(' ')[-1]
                if(is_srt_tmstmp(fstcol) and is_srt_tmstmp(lstcol)):
                    segment_time = cnvrt_hh_mm_sec(lstcol) - cnvrt_hh_mm_sec(fstcol)
                    # Some .srt files may contain invalid srt line(s) that
                    # affect the calculations,
                    # so some minimal .srt verfication is done here.
                    # Gecko should fix this when .srt file is saved again,
                    # including the segment id's.
                    # To avoid this in the future a little bit of verification
                    # must take place.
                    segment_cnt = segment_cnt + 1
                    if(segment_time < 0):
                        print("Segment failure")
                        print(line)
                        print("The segment above, segment id: {} in the file {} needs to be fixed".format(segment_cnt, segment_file))
                        exit(0) # Obviously something wrong so won't continue until the file is fixed manually
                    total = total + segment_time
            segment_cnt = 0
    return total

# Creates a string to print in the Readme for statistics
def statistics_string(total_speakers, total_time, ided_speakers, unknown_speakers):
    statistics = "\n----------\n"
    statistics_lines = None
    total_mins = round( (Decimal(total_time / 60 )), 3)
    hours = total_mins // 60
    minutes = round(total_mins - (60*hours))
    statistics = statistics + "{} minutes ({} hrs {} mins) of speech\n{} ided speakers\n".format(total_mins, hours, minutes, ided_speakers)
    statistics = statistics + "{} unknown speakers\n".format(unknown_speakers)
    statistics = statistics + "{} total speakers\n".format(total_speakers)
    return statistics

# Creates the statistics from the Info CSV file and from the segments files in
# the segments folder
def create_statistics(csv_info_file):
    ided_speakers = 0
    unknown_speakers = 0
    total_speakers = 0
    total_time = total_speech_time()
    stats = None
    speaker_names = set()
    with open(csv_info_file, 'r') as spk_info:
        for line in spk_info:
            spk_name = line.split(',')[2]
            if(spk_name.split()[0] != "Unknown"):
                speaker_names.add(spk_name)
            else:
                unknown_speakers = unknown_speakers + 1

    ided_speakers = len(speaker_names)
    total_speakers = ided_speakers + unknown_speakers

    stats = statistics_string(total_speakers, total_time, ided_speakers, unknown_speakers)
    return stats

# Auto replaces statistics given there is a line that has some string that
# indicates the correct place in the file
# Only one occourence of any name should be taken into the account so for
# people who share exactly the same name,
# only one of them will be considered.
def update_ruv_di_readme(ruv_di_readme, statistics_indicator, csv_info_file):
    statistics = create_statistics(csv_info_file)
    statistics_line_count = 0
    readme_contents = ""
    with open(ruv_di_readme, 'r') as readme_file_contents:
        for line in readme_file_contents:
            if(line.rstrip() == statistics_indicator):
                readme_contents = readme_contents + statistics_indicator + statistics
                # How many lines to skip in the original file - create
                # statistics is the string for writing
                # in the readme file
                # -2 because of new line in the end - don't want to skip new
                # line
                statistics_line_count = len(create_statistics(csv_info_file).split('\n'))-2
            elif(statistics_line_count == 0):
                readme_contents = readme_contents + line
            else:
                statistics_line_count = statistics_line_count - 1

    with open(ruv_di_readme, 'w') as readme_file:
        print(readme_contents, file=readme_file)

    print("Statistics have been updated")

# Feeds the create_segments script of srt files
def create_segments(os):
    srt_folder = 'data/temp/srt/'
    srt_files = os.listdir(srt_folder)
    for filename in srt_files:
        create_segm_and_text("{}/{}".format(srt_folder, filename), 'data/temp')

def main():
    import os
    rttm_lines = []
    srt_folder = 'data/temp/srt/'
    rttm_folder = 'data/temp/rttm/'
    rnm_json_rttm_srt(os)
    # for each file in srt folder and for each file in rttm folder
    srt_files = sorted(os.listdir(srt_folder))
    rttm_files = sorted(os.listdir(rttm_folder))

    # Taking usage of the fact there is a rttm file for each srt file
    for filename_enum in enumerate(rttm_files):
        line_number = filename_enum[0]
        rttm_file = filename_enum[1]
        srt_file = srt_files[line_number] # same line number as in rttm file as there is a .rttm file for each .srt file
        rttm_base = os.path.basename(rttm_file)
        srt_base = os.path.basename(srt_file)
        rttm_lines = trim_rttm(rttm_base, rttm_folder, os)
        trim_srt(srt_base, srt_folder, rttm_lines, os)
    create_segments(os)
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='''Optional arguments that
        are possible to provide, depending on what is needed to be done.
        If no arguments are provided the script will only rename the
        corresponding files if they exist and create segments''')
    parser.add_argument('--statistics', required=False,
        default='data/corpus/reco2spk_num2spk_info.csv', help='the path to the CSV file')
    parser.add_argument('--statistics_off', required=False,
        default='False', help='log the statistics on/off')
    parser.add_argument('--create_csv', required=False,
        default='reco2spk_num2spk_name.csv', help='the path to the CSV file')
    parser.add_argument('--ruv_di_readme', required=False,
        default='data/corpus/ruv-di_README', help='Ruv-di readme file path')
    parser.add_argument('--update_ruv_di_readme_off', required=False,
        default='False', help='Update Ruv-di readme on/off')
    parser.add_argument('--only_csv', default='False',
        help='Correct spelling, create CSV, statistics, and update corpus readme')
    args = parser.parse_args()
    checkArguments(args)
    main()
