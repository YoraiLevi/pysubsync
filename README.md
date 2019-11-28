# Subtitle_Resync
This module attempts to correct unsynced subtitle files based on already synced subtitles.

Inspiration, originaly 2017: 

    There are plenty of raw japanese anime without perfectly timed subtitle for them.
    Anime is aired on TV and as a result many of the raw releases of japanese subtitles have different timings compared to their counterpart English releases.
    To solve this issue, one could manually find the anomaly when watching the episode, correct it and keep watching. This is a tidious process that can be easily automated.

The process:

    Originally listening to a lecture about linear systems I noticed a special property to Convolution Intergral.
    given 2 boolean square signals, the peak of the output function is the maximum value of correlating area under the graph.
    Armed with this idea we represent the subtitles into a boolean function over time and find the phase shift compared to our gold standard.

Problems:

    some anime subtitles aren't so simple. Some subtitles have long asynchronies in between the show run time saved for the ad breaks.
    to combat this issue, a simple analysis of the lack of subtitles can help hinting us in the direction where such events can happen.
    Assuming a normal distobution (might be better to use a poisson) these anomalies are found and the subtitles shifted to their correct place.

TODOs:

sync based on voice activity

gui+win release
    utils: merge 2 subtitle files, for bilingual viewing

required packages:
    pysubs2
    numpy
    scipy

supported file types by pysubs2 at the time of writing:

    '.ass','.ssa','.srt','.microdvd'

To Run:

hardness is an optional argument which refines the search for abnormalities throughout the run time

    $ python run.py "synced_subtitles.ass" "bad_subtitles.ass" "out_subtitles.ass" -harshness 3
for help:

    $ python run.py -h