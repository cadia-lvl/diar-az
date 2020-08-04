#!/bin/bash
#SBATCH --output=gecko_rttm2rttm.log

mkdir -p rttm
mkdir -p json
mkdir -p segments

cp ./rttm_gecko/* ./rttm
cp ./srt_gecko/* ./segments
touch gecko_rttm2rttm.log
python3 scripts/gecko_rttm2rttm.py --create_csv_off 'True' | cat - gecko_rttm2rttm.log > temp && mv temp gecko_rttm2rttm.log
date | cat - gecko_rttm2rttm.log > temp && mv temp gecko_rttm2rttm.log 
#python3 scripts/gecko_rttm2rttm.py --create_csv_off 'False'