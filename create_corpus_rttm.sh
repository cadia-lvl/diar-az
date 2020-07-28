#!/bin/bash
#SBATCH --output=gecko_rttm2rttm.log

mkdir -p rttm
ls rttm_gecko/ | xargs -I % python3 scripts/gecko_rttm2rttm.py --rttm rttm_gecko/%