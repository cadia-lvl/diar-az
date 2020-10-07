#!/usr/bin/env bash
# Author: Judy Fong - lvl@judyyfong.xyz
# Apache 2.0

cd data/gecko

mkdir -p dup/good
mkdir -p dup/bad

mv corrected_rttm/*$1.rttm dup/$2/.
mv json/*$1.json dup/$2/.
mv srt/*$1.srt dup/$2/.
# mv csv/*$1.csv dup/$2/.
