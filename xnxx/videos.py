import urllib2
from bs4 import BeautifulSoup

class Video():
    '''
    Set up simple video-class
    '''
    def __init__(self):
        self.url = ""
        self.tags = []
        self.length = ""
        self.date = ""
    
    def __repr__(self):
        return "%s, %s, %s, %s" % (self.url,str(self.tags),self.length,self.date)

def GetVideoTags(videourl):
    url = urllib2.urlopen(videourl) # open url
    urlcontent = url.read() # read content
    soup = BeautifulSoup(urlcontent,"xml") # parse using the xml-parser & beautiful soup
    video = Video() # initialize new video
    video.url = str(videourl)
    for a in soup.findAll("a"): # iterate over all <a></a>-tags
        if a.has_key("href"):
            if a["href"].find("tags") != -1 and a.string != "Tags": # if href includes "/tags/": Append <a>string</a> to video-tag
                video.tags.append(str(a.string))
    len_date = soup.findAll("font",{"color":"#FFFFFF"}) # get array which includes video length & upload date, try to save it to class instance
    try:
        video.length = str(len_date[1].string)
    except:
        video.length = "-"
    try:
        video.date = str(len_date[3].string)
    except:
        video.date = "-"
    return video