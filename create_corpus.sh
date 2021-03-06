#!/bin/bash
# Copyright 2020 Arnar Freyr Kristinsson
# Copyright 2020 Judy Fong - lvl@judyyfong.xyz
# Apache 2.0
#
#SBATCH --output=logs/create_corpus_%J.log
#SBATCH --nodelist=terra


set -eu -o pipefail

if [ "$#" -eq 0 ] || [ "$1" == "-h" ]; then
    echo "This script creates files for a (diarization) corpus from Gecko"
    echo "files(json, rttm, srt)."
    echo "It must be run from the project's root directory"
    echo "Usage: $0 <gecko archive> <audio directory>"
    echo " e.g.: $0 gecko_files.zip /data/ruv_unprocessed/audio/"
    echo ""
    exit 1;
fi

# NOTE: consider using the kaldi parse_options script to make stage a parameter
# option

text_archive=$1
audio_directory=$2

# TODO: allow the user to pass these in as options
data=data
recording_list=$data/episode_list.txt
combined_csv=$data/reco2spk_num2spk_name.csv

stage=0

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

  # Move corpus data to backup directory
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
  # Remove the example.csv file if it exists
  if [ -f $data/gecko/csv/example.csv ]; then
    rm $data/gecko/csv/example.csv
  fi

  # Get a list of episode names
  # If we are working with the summer student data then use episode_list.py
  # otherwise people should modify recording_list to reference the list of
  # filenames they want for their corpus. Perhaps the filenames within the
  # audio directory are correct
  if [ ! -f $recording_list ]; then
    # TODO: use the directory filenames themselves. Do something like in
    # scripts/gecko_rttm2rttm.rnm_json_rttm_srt but use it to print out a list
    # of all recording_ids to a file
    # make sure the recording_list has only unique ids
    # might be able to combine this with validating directories
    python3 scripts/episode_list.py > $recording_list
  fi

  cp $recording_list $data/gecko/.backup/.
  # Check for missing episode files
  # Using the episode list check if a directory has multiple files with the
  # same recording id
  # TODO: if so, # ask the user which file to keep
  # TODO: make sure that each directory has the same number of files. throw an
  # error if the number of files differ
  python3 scripts/validate_data_dir.py -r $recording_list
fi

if [ $stage -le 2 ]; then
  # Remove any existing temp files
  if [ -d $data/temp ]; then
    rm -rf $data/temp
  fi

  mkdir -p $data/corpus/json
  mkdir -p $data/temp/{rttm,srt,text,segments,json,csv}

  cp $data/gecko/corrected_rttm/* $data/temp/rttm
  cp $data/gecko/srt/* $data/temp/srt
  cp $data/gecko/json/* $data/temp/json
  cp $data/gecko/csv/* $data/temp/csv
fi

if [ $stage -le 3 ]; then
  gecko_rttm_log=gecko_rttm2rttm.log
  touch $gecko_rttm_log

  # TODO: in rttm files identify 1.[noise], + (return as tuple?) and crosstalk
  # and deal with them

  # Convert second column of rttm file to the audio filename
  # Removes [xxx] within rttm segments with X+[xxx]
  # Remove srt and rttm segments which are only [] stuff
  # In rttm files, log files with segments with <NA> as speaker id
  # Identify rttm files which have something other than a plain number,
  # num+[tag], or [tag]+num and log the filename
  echo "Rename rttm, srt, and json files"
  echo "Create segments files in data/temp/segments."
  echo "The log file can be found at ${gecko_rttm_log}"
  python3 scripts/gecko_rttm2rttm.py > $gecko_rttm_log

  # Remove empty lines from rttm files
  for f in $data/temp/rttm/*.rttm; do
    sed -i '/^ *$//d' "$f"
  done
fi

if [ $stage -le 4 ]; then
  # 4882758R10.csv has a completely different encoding than everything else and
  # within it's already corrupt so it was corrected manually up until this stage
  for c in $data/temp/csv/*.csv; do
    # change semicolons to commas
    sed -i 's/;/,/g' "$c";
    # convert windows line endings to unix
    sed -i 's/\r$//g' "$c";
    # add new line to end of file
    sed -i -e '$a\' "$c";
    # remove bom encoding
    sed -i $'1s/^\uFEFF//' "$c";
  done

  cat $data/temp/csv/* >> $combined_csv
  # remove lines with only the delimiter
  # remove empty lines, with or without spaces
  # remove trailing commas
  sed -i -e '/,,/d' -e '/^ *$/d' -e 's/,$//' $combined_csv
fi

if [ $stage -le 5 ]; then
  # Adds the date to the readme file
  date | cat - $gecko_rttm_log > temp && mv temp $gecko_rttm_log
  # Correct spelling errors and create the csv files
  # Create the statistics and update the readme
  # NOTE: This is interactive unless you use --correct_spelling False directly
  # on scripts/csv2spkids.py
  python3 scripts/gecko_rttm2rttm.py --only_csv 'True' \
    --create_csv $combined_csv
fi

if [ $stage -le 6 ]; then
  # Copy temp_dir segments,json,rttm directories to corpus then delete temp_dir
  for x in rttm segments json; do
    cp -r $data/temp/$x $data/corpus/
  done
  cp $audio_directory/* $data/corpus/wav
  rm -rf $data/temp
fi
