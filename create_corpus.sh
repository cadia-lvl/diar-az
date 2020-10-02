#!/bin/bash
# Copyright 2020 Arnar Freyr Kristinsson
# Copyright 2020 Judy Fong - lvl@judyyfong.xyz
# Apache 2.0
#
#SBATCH --output=gecko_rttm2rttm.log
#SBATCH --nodelist=terra

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

mkdir -p rttm
mkdir -p json
mkdir -p segments

cp ./rttm_gecko/* ./rttm
cp ./srt_gecko/* ./segments
touch gecko_rttm2rttm.log
python3 scripts/gecko_rttm2rttm.py | cat - gecko_rttm2rttm.log > temp && mv temp gecko_rttm2rttm.log
date | cat - gecko_rttm2rttm.log > temp && mv temp gecko_rttm2rttm.log 
python3 scripts/gecko_rttm2rttm.py --only_csv 'True'
fi
