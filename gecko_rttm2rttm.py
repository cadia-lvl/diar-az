# Author: Reykjavik University (Judy Fong <judyfong@ru.is>)
# Description: Convert gecko rttm files to also have recordingids in the first
# <NA>

#removes [something]+number (speaker number) - rttm files
def rm_brckts_spker_rttm(line):
    spkridOrBracketStuff = line.split(" ")[7]

    if "]+" in spkridOrBracketStuff:

        spkrnum = spkridOrBracketStuff.split("+")[1]
        endbrackpos = line.find("]")
        bgnbrackpos = line.find("[")
        removed = line.replace ( line[ bgnbrackpos : endbrackpos+2 ], "")
        print (removed)
    else:
        print (line)



    #else:
     #   print (line)


def main(gecko_rttm):
    import os
    base = os.path.basename(gecko_rttm)
    (audiofilename, ext) = os.path.splitext(base.split("_")[0].split("-")[1])
    (filename, ext) = os.path.splitext(base.replace("_",""))
    print(ext)
    with open(gecko_rttm , 'r') as gecko_file, open('rttm/'+ base, 'w') \
        as rttm_file:
        for line in gecko_file:
            if ext == ".rttm":
                removeBracketsWithSpeakerRttm(line)
            else:
                print ("this is not a rttm!")
            print(line.rstrip().replace('<NA>', filename, 1).replace('<NA>', audiofilename, 1), end='\n',
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
