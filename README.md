# diar-az
Diarization A to Z - Gecko to Kaldi and corpus and back

Goal is automating the diarization process for 1. Adding to the corpus 2. Running the corpus through kaldi

1. Create the csv file using gecko

2. Add audio filenames to rttm files. 
3. Remove [] stuff from rttm files and srt segments which are only brackets. 
4. Rename rttm files to just the audio filename. 
5. Split each week’s files into 70/15/15%
6. Create a csv file like in the corpus. This involves pairing up all the written names across files (1-3 spelling mistakes allowed, extra spaces allowed- both corrected), then matching them up with the existing spkids or creating new ones for new speakers. This needs to be done with unknowns too but they also need to be renamed to the next numbered unknown available. 
7. Generate text file with the updated corpus numbers in the readme. If know how, then it also autoreplaces the readme. 

8 everything but the people name validation should be done with just one command. So one command for name validation then the rest will spit out everything to the correct folders. 
9. Also include the command to call subtitle2segments_and_text.py

I’ve created bash and python files using gawk, sed, sort -u, sox I believe. Try to only use tools which already exist. Create the appropriate folders. Unvalidated & validated

If have kaldi setup the run local/make_ruvdi.sh, fix_data_dir & utils/validate_data_dir.sh

10. Create a script which creates new segments based on 2-6 speaker turns which looks like the current corpus but with those new audio files. 

Link to broadcast_data_prep. Create new repo. Check my temp files. See if anything there would be useful and add it to the repo or swnd it over through PM. 
