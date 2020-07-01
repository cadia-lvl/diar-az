# Author: Reykjavik University (Judy Fong <judyfong@ru.is>)
# Description: Convert gecko rttm files to also have recordingids in the first <NA>,
# adds audio filenames to rttm files as the second field,
# remove [] stuff (foreign, noise, music) from rttm files where there is a [something]+number,
#renames the rttm/json/srt files to just the audio filename 
# and calls the create_segments_and_text.py
#All fields are optinal but at least one of these must be provided: --rrtm, --srt, --subtitle-file

from decimal import * 
import create_segments_and_text

#removes [something]+number (speaker number) - rttm files
def rm_brckts_spker_rttm(line):
    spkridOrBracketStuff = line.split(" ")[7]
    if "]+" in spkridOrBracketStuff:
        spkrnum = spkridOrBracketStuff.split("+")[1]
        endbrackpos = line.find("]")
        bgnbrackpos = line.find("[")
        removed = line.replace ( line[ bgnbrackpos : endbrackpos+2 ], "")
        return removed
    else:
        return line

#Convert timestamps to seconds and partial seconds hh:mm:ss.ff
def cnvrt_hh_mm_sec(hh_mm_ss):
    hh, m, s = hh_mm_ss.split(':')
    return ( int(hh) * 3600 ) + ( int(m) * 60) + Decimal(s.replace(",","."))

#Checks if a string is a timestamp
def is_srt_tmstmp(tmstamp):
    mintmstamplen = 8 # 00:00:00 (hh:mm:ss) - minimum timestamp length
    if (len (tmstamp) >= mintmstamplen):
        if(tmstamp[0:2].isnumeric() and tmstamp[2] == ':' and tmstamp[3:5].isnumeric() \
                    and tmstamp[5] == ':' and tmstamp[6:8].isnumeric() \
                    and tmstamp[9:].isnumeric() ):
            return True
    return False
    
#checks if there is some speech in the rttm file at specific segment 
def is_speech_rttm(srt_line, rttm_lines):
    if(tmstmp_scnds(srt_line) != []):
        srt_range = tmstmp_scnds(srt_line)
        for rttm_line in rttm_lines:
            rttm_bgn_tm = rttm_line.split(' ')[3]
            rttm_spkr_else = rttm_line.split(' ')[7]
            if( Decimal(rttm_bgn_tm) >= srt_range[0] and Decimal(rttm_bgn_tm) < Decimal(str(srt_range[1])) ):
                if(rttm_spkr_else.isnumeric()):
                    return False
    return True
#Returns the timestamps in seconds to compare the srt file to the rttm file to remove the correct segments with no speech in it.
def tmstmp_scnds(line):
      fstcol = line.split("\n")[0].split(' ')[0]
      lstcol = line.split("\n")[0].split(' ')[-1]
      arrow = "-->"
      #Find the correct line (a line that has a timestamp)
      if( is_srt_tmstmp(fstcol) and is_srt_tmstmp(lstcol)):
        expln = fstcol + " " + arrow + " " + lstcol
        if(expln == line[:-1]):
            return [ cnvrt_hh_mm_sec(fstcol), cnvrt_hh_mm_sec(lstcol) ]
      return []

#Gets the audio filename
def get_audio_filename(filename, os):
    (filename, ext) = os.path.splitext(filename)
    if ("_" in filename and "-" in filename):
        audiofilename = filename.split("_")[0].split("-")[1]
        return audiofilename+ext
    elif ("-" in filename):
        audiofilename = filename.split("-")[1]
        return audiofilename+ext
    else:
        return filename+ext

#renames files given a list contents of a directory and a file type
def rename(dircontents, dirname, os):
    for filename in dircontents:
        audiofilename = get_audio_filename(filename, os)
        os.rename(dirname+"/"+filename, dirname+"/"+audiofilename)
        (fl, ext) = os.path.splitext(filename)
        print("The {} file {} has been renamed to {}".format(ext, filename, audiofilename))

#Renames Json, Rttm and srt files
def rnm_json_rttm_srt(os):
    json_files = os.listdir('json')
    rttm_files = os.listdir('rttm')
    srt_files = os.listdir('segments')
    rename(json_files, "json", os)
    rename(rttm_files, "rttm", os)
    rename(srt_files, "segments", os)

#Checks the given arguments and calls the corresponding function
def checkArguments(args):
    if args.rttm and args.srt and not args.subtitle_file:
        main(args.rttm, args.srt)

    elif args.rttm and not args.srt and not args.subtitle_file:
       main(args.rttm, None)
    
    elif args.srt and not args.rttm and not args.subtitle_file:
       main(None, args.srt) 

    elif args.rttm and args.srt and args.subtitle_file:
        main(args.rttm, args.srt)
        create_segments_and_text.main(args.subtitle_file)
    
    elif args.subtitle_file and not args.srt and not args.rttm:
        create_segments_and_text.main(args.subtitle_file)
    
    elif args.rttm and args.subtitle_file and not args.srt:
        main(args.rttm, None)
        create_segments_and_text.main(args.subtitle_file)

    elif args.srt and args.subtitle_file and not args.rttm:
        main(None, args.srt)
        create_segments_and_text.main(args.subtitle_file)

    else:
        print('A file needs to be given.')
        exit(0)

def main(gecko_rttm, gecko_srt):
    import os
    srt_ranges = []
    rttm_lines = []
    if(gecko_rttm != None):
        base = os.path.basename(gecko_rttm)
        (audiofilename, ext) = os.path.splitext( get_audio_filename(gecko_rttm, os) )
        (filename, ext) = os.path.splitext(base.replace("_",""))
        with open(gecko_rttm , 'r') as gecko_file, open('rttm/'+ base, 'w') \
        as rttm_file:
            for line in gecko_file:
                line = rm_brckts_spker_rttm(line)
                rttm_lines.append(line)
                print(line.rstrip().replace('<NA>', filename, 1).replace('<NA>', audiofilename, 1), end='\n',
                file=rttm_file)
    if(gecko_srt != None):
        base = os.path.basename(gecko_srt)
        with open(gecko_srt , 'r') as gecko_srt_file, open('segments/'+ base, 'w') \
            as srt_file:
            for line in gecko_srt_file:
                    if(gecko_rttm != None):
                        if not is_speech_rttm(line, rttm_lines):
                            print(line, end='\n', file=srt_file)
    rnm_json_rttm_srt(os)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='The arguments need to \
    be passed in.')
    parser.add_argument('--rttm', required=False, help='the path to the rttm-file')
    parser.add_argument('--srt', required=False, help='the path to the srt-file')
    parser.add_argument('--subtitle-file', required=False, help='the path to the srt-file or subtitle-file')
    args = parser.parse_args()
    checkArguments(args)