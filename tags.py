import urllib2
import pickle
import videos
import copy
import os
import sys
from bs4 import BeautifulSoup

def GetVideosForPage(soup):
    video_urls = []
    for a in soup.findAll("a"):
        if a.has_key("class"):
            if a["class"] == "miniature":
                video_urls.append(a["href"])
    return video_urls
    
def IterateTagPages(url):
    url = urllib2.urlopen(url)
    urlcontent = url.read()
    soup = BeautifulSoup(urlcontent,"xml")
    video_urls = []
    video_urls.extend(GetVideosForPage(soup))
    print len(video_urls)
    for i in soup.findAll("a","nP"):
        if i.string == "Next":
            next = True
            next_url = "http://video.xnxx.com" + i["href"]
            break
        else:
            next = False
                       
    while next == True:
        print next_url
        url = urllib2.urlopen(next_url)
        urlcontent = url.read()
        soup = BeautifulSoup(urlcontent,"xml")
        video_urls.extend(GetVideosForPage(soup))
        print len(video_urls)
        for i in soup.findAll("a","nP"):
            if i.string == "Next":
                next = True
                next_url = "http://video.xnxx.com" + i["href"]
                break
            else:
                next = False
    return video_urls

def VideosForTag(video_collection,url):
    print "getting video-urls for tag"
    video_urls = IterateTagPages(url)
    print "got video-urls"
    print "getting tag-collection for all videos"
    for video in video_urls:
        video_tags = videos.GetVideoTags(video)
        video_collection[video_tags.url] = video_tags
    print "got all videos for tag"
    return video_collection

def TagList(url):
    url = urllib2.urlopen(url)
    urlcontent = url.read()
    soup = BeautifulSoup(urlcontent,"xml")
    invalid_tags = ["/tags/","/tags/","/tags/-","/tags/--","/tags/---"]
    tags = {}
    for a in soup.findAll("a"):
        if a.has_key("href"):
            if a["href"].find("/tags/") !=-1 and a["href"] not in invalid_tags:
                tags[str(a["href"])] = False
    return tags

def IterateTags(url):
    try:
        video_pickle = open("video_collection.pickle","rb")
        video_collection = pickle.load(video_pickle)
        video_pickle.close()
        print "loaded saved videos"
    except:
        print "created new video-collection"
        video_collection = {}
    try:
        tag_pickle = open("tag_collection.pickle","rb")
        tag_collection = pickle.load(tag_pickle)
        tag_pickle.close()
        print "loaded tag-collection"
    except:
        print "getting new tags"
        tag_collection = TagList(url)
        print "got new tags"
    new_tag_collection = copy.deepcopy(tag_collection)
    
    for tag,value in tag_collection.items():
        if value == False:
            print "############################################"
            print "iterate over videos for %s" % (tag)
            video_collection = VideosForTag(video_collection,"http://video.xnxx.com"+tag)
            print "got all videos for %s" % (tag)
            new_tag_collection[tag] == True
            video_pickle = open("video_collection.pickle","wb")
            tag_pickle = open("tag_collection.pickle","wb")
            pickle.dump(new_tag_collection,tag_pickle)
            print "Saved Tag-Collection"
            pickle.dump(video_collection,video_pickle)
            print "Saved Video Collection"
            tag_pickle.close()
            video_pickle.close()
            print "Now got "+str(len(video_collection))+" videos"
            print "############################################"