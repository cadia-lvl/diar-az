#!/bin/bash
# Copyright 2020 Arnar Freyr Kristinsson
# Copyright 2020 Judy Fong - lvl@judyyfong.xyz
# Apache 2.0
#
#SBATCH --output=logs/create_corpus_%J.log
#SBATCH --nodelist=terra


# TODO: gecko_rtt2rttm.log

set -eu -o pipefail

if [ "$#" -eq 0 ] || [ "$1" == "-h" ]; then
    echo "This script creates files for a (diarization) corpus from Gecko files (json, rttm, srt)"
    echo "It must be run from the project's root directory"
    echo "Usage: $0 <gecko archive> <audiodirectory>"
    echo " e.g.: $0 gecko_files.zip /data/ruv_unprocessed/audio/"
    echo ""
    exit 1;
fi

# NOTE: consider using the kaldi parse_options script to make stage a parameter option

text_archive=$1
audio_directory=$2
data=data
recording_list=$data/episode_list.txt
stage=1

mkdir -p $data/gecko/.backup

if [ $stage -le 0 ]; then
  # Move all the existing gecko data back and use the archive specified
  for x in csv corrected_rttm srt json; do
    if [ -d $data/gecko/$x ]; then
      mv $data/gecko/$x $data/gecko/.backup/$x
    fi
  done

  # Unzip files from Teams
  if [ ! -d "$data/gecko/csv" ]; then
    echo -e "\nDownload files created from Gecko"
    unzip $text_archive -d $data/gecko/
  fi

  # TODO: move corpus data to backup directory
  mkdir -p $data/corpus/.backup

  for x in segments rttm; do
    if [ -d $data/corpus/$x ]; then
      mv $data/corpus/$x $data/corpus/.backup/$x
    fi
  done

  mkdir -p $data/corpus/rttm
  mkdir -p $data/corpus/segments
fi

if [ $stage -le 1 ]; then
  # Get a list of episode names
  # TODO If we are working with the summer student data then use episode_list.py
  # otherwise people should provide the list of filenames they want for their
  # corpus, perhaps the filenames within the audio directory are correct
  python3 scripts/episode_list.py > $recording_list

  cp $recording_list $data/gecko/.backup/.
  # Check for missing episode files
  # Using the episode list check if a directory has multiple files of the same name
  # TODO: if so, # ask the user which file to keep
  python3 scripts/validate_data_dir.py -r $recording_list
  exit 0
fi

if [ $stage -le 2 ]; then
  mkdir -p $data/corpus/json
  mkdir -p $data/temp/{rttm,segments,json,csv}

  cp $data/gecko/corrected_rttm/* $data/temp/rttm
  cp $data/gecko/srt/* $data/temp/segments
  cp $data/gecko/json/* $data/temp/json
  cp $data/gecko/csv/* $data/temp/csv
fi

if [ $stage -le 3 ]; then
  touch gecko_rttm2rttm.log
  # TODO: TEST THIS NEXT!!! Renames corresponding files if they exist and update the readme file
  python3 scripts/gecko_rttm2rttm.py | cat - gecko_rttm2rttm.log > temp && mv temp gecko_rttm2rttm.log
  # Adds the date to the readme file
  date | cat - gecko_rttm2rttm.log > temp && mv temp gecko_rttm2rttm.log
  # Only correct spelling errors and create the csv file
  python3 scripts/gecko_rttm2rttm.py --only_csv 'True'
fi
