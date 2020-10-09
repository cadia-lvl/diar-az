# Author: Judy Fong (Reykjavik University)
# Edits: Inga Rún Helgadóttir (Reykjavik University)
# Description:
# Create segments file from subtitle timestamps
# create a corresponding text file
# create a single segment for each timestamp set

# TODO: normalize the text
# TODO: create corpus file
from itertools import groupby
from decimal import Decimal
import os
import argparse
from pathlib import Path


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="""Create segments file from subtitle timestamps and a corresponding text file\n
        Create a single segment for each timestamp set\n
        Usage: python create_segments_and_text.py <input-file> <output-dir>\n
            E.g. python local/create_segments_and_text.py data/vtt_transcripts/4886083R7.vtt data
        """
    )
    parser.add_argument(
        "subtitle_file", type=file_path, help="Input subtitle file",
    )
    parser.add_argument(
        "outdir", type=str, help="base path for output files",
    )
    return parser.parse_args()


def file_path(path):
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_file:{path} is not a valid file")


# Convert timestamps to seconds and partial seconds so hh:mm:ss.ff
def time_in_seconds(a_time):
    hrs, mins, secs = a_time.split(":")
    return Decimal(hrs) * 3600 + Decimal(mins) * 60 + Decimal(secs.replace(",", "."))


def no_transcripts(subtitle_path):
    HEADER_ONLY = 10
    ACCESS_ERROR_ONLY = 36
    return os.stat(subtitle_path).st_size in (HEADER_ONLY, ACCESS_ERROR_ONLY)


def create_segm_and_text(subtitle_filename, outdir):
    if no_transcripts(subtitle_filename):
        print(f"{subtitle_filename} is presumed to not have transcripts")
    else:
        base = os.path.basename(subtitle_filename)
        (filename, ext) = os.path.splitext(base.replace("_", ""))
        segmentsdir = outdir + '/segments/'
        textdir = outdir + '/text/'
        Path(segmentsdir).mkdir(parents=True, exist_ok=True)
        Path(textdir).mkdir(parents=True, exist_ok=True)

    with open(subtitle_filename, "r") as fin, open(
        segmentsdir + "/" + filename + ".segments", "w"
    ) as fseg, open(textdir + "/" + filename + ".text", "w") as ftext:
        if ext == ".vtt":
            # skip header(first two) lines in file
            next(fin)
            next(fin)
        groups = groupby(fin, str.isspace)
        count = 0
        for (_, *rest) in (map(str.strip, v) for g, v in groups if not g):
            # write to text file
            # better to create individual speaker ids per episode or shows,
            # more speaker ids, because a global one would create problems for
            # cepstral mean normalization ineffective in training
            string = " ".join([*rest[1:]])
            ftext.write(f"{filename}_{count:05d} {string}\n")
            if ext == ".vtt":
                start_time, _, end_time, _ = (str(*rest[:1])).split(" ", 3)
            elif ext == ".srt":
                start_time, _, end_time = (str(*rest[:1])).split(" ", 2)
            else:
                print(
                    "The file was not recognized as a subtitle file(\
                        .vtt or .srt)."
                )
                exit(1)
            start_seconds = time_in_seconds(start_time)
            end_seconds = time_in_seconds(end_time)
            # write to segments file
            fseg.write(
                f"{filename}_{count:05d} {filename} {start_seconds} {end_seconds}\n"
            )
            count = count + 1


def main():
    args = parse_arguments()
    Path(args.outdir).mkdir(parents=True, exist_ok=True)
    create_segm_and_text(args.subtitle_file, args.outdir)


if __name__ == "__main__":
    main()
