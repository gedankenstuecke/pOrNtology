# Results of the XNXX Crawling

The crawling was done in two instances. The first crawling took from 08/04/2012 to 08/11/2012. Afterwards a second run, on 08/12/2012, was done to make sure no bias was introduced through the length of the first crawling run. The results of the second run were tested for how many videos were uploaded after the second run started. As only 11 videos were uploaded during the second run they were included in the final analysis.

## Some Basic Numbers
* Total number of videos crawled: 1449142
* Total number of videos after excluding videos uploaded on 08/13/12: 1449131
* Total number of tags over all videos: 14061156
* Number of unique tags: 66277

## Data: Pickle Object & CSVs
The data is available as the pickle object which was used for the crawling in *video_collection.pickle*. To load the object you need to import the video-class which is defined in */scripts/xnxx/videos.py*. The pickle objects were dumped into a CSV. The data can be found including all videos (*videos_raw.csv*) or excluding the 11 videos which were found during the intermediate crawling (*videos_crawltime_filtered.csv*).   

## Clustering
The videos were clustering using the Markov Clustering Algorithm [1]. Data was with the following parameters: *mcl -i mclInput -scheme 7 -i 5.0 -o mclOutputInflation5.0*.  

**Description of results missing until now** 

## Histograms
*R* was used to create histograms in order to visualize the distribution of tags and upload times. For a start all videos which included no tags were removed. Tags were available for 1449142 of the videos. The graph can be found in */figures/histogram_tags_per_video.pdf*, the raw data used for the graph in *videos_no_empty_tags.csv*. 

For 1447988 videos the hour of the upload was available. The resulting histogram can be found in */figures/histogram_hour_of_upload.pdf*. Interestingly most videos have been uploaded between 1 and 2 am, followed by nearly no videos between 2 and 7 am. Unfortunately it's not clear for which time zone those hours are displayed by xnxx. But it looks like the main uploads are done programmatically or at least through some supervised process. The raw data used for the analysis can be found in *videos_no_empty_hour.csv*. 


# To Do
##Graphs
* Histogram of number of videos per tag
* Histogram of uploads per Year/Month, analogous to openSNP-paper-graphs
* Histogram of length distribution 

##Structuring Data
* CSV of Ranking Tags of form *"tag;number videos;cluster this tag belongs to";mean length* 
* Month/Week(?)-wise splitting of data to see whether picture changes with time

## Stats
* Sig. changes of tag-frequency/clip-length over time?
* Your idea here (and in the above categories as well)

# References
[1] http://micans.org/mcl/
