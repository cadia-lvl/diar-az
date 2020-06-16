# diar-az
Diarization A to Z - Gecko to Kaldi and corpus and back

There are two goals when automating the diarization process:
1. Adding to and existing diarization corpus
2. Running the corpus through kaldi

# Notes
Everything but the people name validation should be done by calling just one script. This script can call other scripts but the user should only have to call one. So possibly two scripts.


The corpus has the following:
```                corpus-root
                       README.txt
                       reco2spk_num2spk_label.csv
                       rttm/
                       json/
                       segments/
                       wav/
```

You do not need to concern yourself with the wav folder for this project. Assume you'll be working on directory above the corpus. 

I’ve created bash and python files using gawk, sed, sort -u, sox I believe. Create the appropriate folders. 

Do not commit any files or information that is specific to this corpus, e.g. names, the corpus README.

## Tasks
1. Add audio filenames to rttm files, as the second field. See [the template file in kaldi-speaker-diarization/master/templates.md](https://github.com/cadia-lvl/kaldi-speaker-diarization/blob/master/templates.md) for an example. DO NOT put angle brackets arounnd the recording-id/audio filenames. 
3. Remove [] stuff (foreign, noise, music) from rttm files and srt segments. For rttm file that means remove the line or remove the [] portion of a line with speaker-ids as [foreign]+15. For srt segments that means only remove the segments which don't have any speech. 
4. Rename the rttm/json/srt files themselves to just the audio filename. 
6. Also include the command to call [create_segments_and_text.py](https://github.com/cadia-lvl/broadcast_data_prep/blob/master/ruv/create_segments_and_text.py). It might be difficult due to where the resulting files are created. If so, then will need to generalize the python file. Do this and create a pull-request.
7. Generate text file with the updated corpus numbers in the corpus readme. If know how to, then also autoreplaces the values in the readme. 

### Other tasks
1. Create a csv file like in the corpus`<audio-filename>,<spk-num>,<speaker label>`. This involves pairing up all the written names across files then matching them up with the existing spkIds or creating new ones for new speakers. This needs to be done with unknowns too but they also need to be renamed to the next numbered unknown available. 
1. Also create `<audio-filename>,<spk-num>,<speaker name>,<speaker label>`
4. Allow there to be 1-3 spelling mistakes in the names which will then be manually validated and corrected.
1. Create/export the unvalidated csv file from Gecko instead of the other students manually making it.



## Possible tasks if the above are done
If have kaldi setup the run local/make_ruvdi.sh, fix_data_dir & utils/validate_data_dir.sh

5. Split each week’s files into 70/15/15% with the 70% portion holding the extra audio files.
1. Run the kaldi recipe and split_rttm (I'll need to supply this file). Add them to the callhome_rttm directory.
26. Run the kaldi recipe (kaldi-speaker-diarization/v4) to evaluate the new DER% with the increased data.
10. Create a script which creates new segments based on 2-6 speaker turns which looks like the current corpus but with those new audio files. 
