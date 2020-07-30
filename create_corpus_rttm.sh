#!/bin/bash
#SBATCH --output=gecko_rttm2rttm.log

mkdir -p rttm
mkdir -p json
mkdir -p segments

cp ./rttm_gecko/* ./rttm
cp ./srt_gecko/* ./segments
python3 scripts/gecko_rttm2rttm.py
#ls rttm_gecko/ | xargs -I % python3 scripts/gecko_rttm2rttm.py --rttm rttm_gecko/% --create_csv_off 'True'
#ls srt_gecko/  | xargs -I % python3 scripts/gecko_rttm2rttm.py --srt srt_gecko/% --create_csv_off 'True'