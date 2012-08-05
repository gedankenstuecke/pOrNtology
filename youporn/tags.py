import urllib2
import pickle
import videos
import copy
import os
import sys
from bs4 import BeautifulSoup

def GetVideosForPage(soup):
    '''
    Grab all Video-Links from single tag-page, like
    http://video.xnxx.com/tags/acrobat
    '''
    video_urls = []
    for a in soup.findAll("a","videoTitle"): # iterate over all <a></a>-tags in soup. Return link to video if found
        if a["href"].find("?from") != -1:
            video_urls.append("http://www.youporn.com"+a["href"][:a["href"].find("?from")])
    return video_urls
    
def IterateTagPages(url):
    '''
    Iterate over all video-pages for a single tag. E.g. get "acrobat"-videos
    from page 1 to 8:  
    '''
    opener = urllib2.build_opener()
    opener.addheaders.append(("Cookie","age_verified=1"))
    url = opener.open(url)
    urlcontent = url.read() # read content
    soup = BeautifulSoup(urlcontent,"xml") # parse using the xml-parser & beautiful soup
    video_urls = []
    video_urls.extend(GetVideosForPage(soup)) # give soup to function to find all videos on initial page
    next_url = ""
    next = False
    print len(video_urls)
    for i in soup.findAll("li","prev-next"): # check whether there are more pages to grab. if yes return url of next page and set flag to True
        if i.a.getText().find("NEXT") != -1:
            next = True
            next_url = "http://www.youporn.com" + i.a["href"]
            break
        else:
            next = False
                       
    while next == True: # if there are more pages in forward direction: grab those as well. 
        print next_url
        opener = urllib2.build_opener()
        opener.addheaders.append(("Cookie","age_verified=1"))
        url = opener.open(next_url)
        urlcontent = url.read()
        soup = BeautifulSoup(urlcontent,"xml")
        video_urls.extend(GetVideosForPage(soup))
        print len(video_urls)
        for i in soup.findAll("li","prev-next"): # check whether there are more pages to grab. if yes return url of next page and set flag to True
             if i.a.getText().find("NEXT") != -1:
                 next = True
                 next_url = "http://www.youporn.com" + i.a["href"]
                 break
             else:
                 next = False
    return video_urls

def VideosForTag(video_collection,url):
    '''
    Iterate over all videos in array and return a dictionary with
    key = videourl, value = video-object, see videos.py
    '''
    print "getting video-urls for tag"
    video_urls = IterateTagPages(url)
    print "got video-urls"
    print "getting tag-collection for all videos"
    for video in video_urls:
        if video_collection.has_key(video) == False:
            print "saving "+video
            video_tags = videos.GetVideoTags(video)
            video_collection[video_tags.url] = video_tags
        else:
            print "skipped "+video+ " as already saved"
    print "got all videos for tag"
    return video_collection

def TagList(url):
    '''
    Set up initial tag-list from URL. 
    Take http://www.youporn.com/categories/ and iterate over all tags and get list of links to each tag
    '''
    opener = urllib2.build_opener()
    opener.addheaders.append(("Cookie","age_verified=1"))
    url = opener.open(url)
    urlcontent = url.read() # read content
    soup = BeautifulSoup(urlcontent,"xml")
    tags = {}
    for td in soup.findAll("td","col1"):
        a = td.a
        tags[str(a["href"])] = False
    return tags

def IterateTags(url):
    '''
    Load or get all tags, iterate over each tag to get videos & tags
    '''
    try:
        video_pickle = open("youporn_video_collection.pickle","rb") # if we already ran the script there should be videos to save
        video_collection = pickle.load(video_pickle)
        video_pickle.close()
        print "loaded saved videos"
    except:
        print "created new video-collection"        # if not create new collection
        video_collection = {}
    try:
        tag_pickle = open("youporn_tag_collection.pickle","rb") # same is true for tags
        tag_collection = pickle.load(tag_pickle)
        tag_pickle.close()
        print "loaded tag-collection"
    except:
        print "getting new tags"
        tag_collection = TagList(url)
        print "got new tags"
    
    for tag,value in tag_collection.iteritems():    # now iterate over each tag
        if value == False:  # if it already was parsed (value == True: great, we skip it)
            print "############################################"
            print "iterate over videos for %s" % (tag)
            video_collection = VideosForTag(video_collection,"http://www.youporn.com"+tag)
            print "got all videos for %s" % (tag)
            tag_collection[tag] = True
            print tag_collection[tag]
            video_pickle = open("youporn_video_collection.pickle","wb")
            tag_pickle = open("youporn_tag_collection.pickle","wb")
            pickle.dump(tag_collection,tag_pickle)
            print "Saved Tag-Collection"
            pickle.dump(video_collection,video_pickle)
            print "Saved Video Collection"
            tag_pickle.close()
            video_pickle.close()
            print "Now got "+str(len(video_collection))+" videos"
            print "############################################"