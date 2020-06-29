# Author: Reykjavik University (Judy Fong <judyfong@ru.is>)
# Description: Convert gecko rttm files to also have recordingids in the first
# <NA>
from decimal import * #For correct decimal rounding 

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

#Converts hh_mm_ss to just seconds
def cnvrt_hh_mm_sec(hh_mm_ss):
    hh_mm_ss = hh_mm_ss.split(':')
    hh = hh_mm_ss[0] #Seconds in the hour
    m = hh_mm_ss[1] #Seconds in the minute
    s = hh_mm_ss[2] #Seconds
    s_d = s.replace(",",".")
    total = ( int(hh) * 3600 ) + ( int(m) * 60) + Decimal(s_d)
    return total

#Checks if a string is a timestamp
def is_srt_tmstmp(tmstamp):
    mintmstamplen = 8 # 00:00:00 (hh:mm:ss)
    if (len (tmstamp) >= mintmstamplen):
        if(tmstamp[0:2].isnumeric() and tmstamp[2] == ':' and tmstamp[3:5].isnumeric() \
                    and tmstamp[5] == ':' and tmstamp[6:8].isnumeric() \
                    and tmstamp[9:].isnumeric() ):
            return True
    return False

#checks if there is some speech in the rttm file
def is_speech_rttm(srt_line, rttm_lines):
    ln_ind = 0
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
      #Find the correct line (a line that has a timestamp)
      if( is_srt_tmstmp(fstcol) and is_srt_tmstmp(lstcol)):
        expln = fstcol + " --> " + lstcol
        if(expln == line[:-1]):
            return [ cnvrt_hh_mm_sec(fstcol), cnvrt_hh_mm_sec(lstcol) ]
      return []

def main(gecko_rttm, gecko_srt):
    import os
    base = os.path.basename(gecko_rttm)
    (audiofilename, ext) = os.path.splitext(base.split("_")[0].split("-")[1])
    (filename, ext) = os.path.splitext(base.replace("_",""))
    srt_ranges = []
    rttm_lines = []
    i = -1
    with open(gecko_rttm , 'r') as gecko_file, open('rttm/'+ base, 'w') \
        as rttm_file:
        for line in gecko_file:
                line = rm_brckts_spker_rttm(line)
                rttm_lines.append(line)
                print(line.rstrip().replace('<NA>', filename, 1).replace('<NA>', audiofilename, 1), end='\n',
            file=rttm_file)
    base = os.path.basename(gecko_srt)
    with open(gecko_srt , 'r') as gecko_srt_file, open('segments/'+ base, 'w') \
        as srt_file:
        for line in gecko_srt_file:
            if(tmstmp_scnds(line) != []):
                if not is_speech_rttm(line, rttm_lines):
                     print(line, end='\n', file=srt_file)
    print("The recording ids have been added to {}.".format(base))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='The arguments need to \
    be passed in.')
    parser.add_argument('--rttm', required=True, help='the path to the rttm file')
    parser.add_argument('--srt', required=True, help='the path to the srt file')
    args = parser.parse_args()
    if args.rttm and args.srt:
        main(args.rttm, args.srt)
    else:
        print('A file needs to be given.')
        exit(0)
