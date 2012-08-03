import urllib2
from bs4 import BeautifulSoup

class Video():
    def __init__(self):
        self.url = ""
        self.tags = []
        
def GetVideoTags(videourl):
    url = urllib2.urlopen(videourl)
    urlcontent = url.read()
    soup = BeautifulSoup(urlcontent,"xml")
    video = Video()
    video.url = str(videourl)
    for a in soup.findAll("a"):
        if a.has_key("href"):
            if a["href"].find("tags") != -1 and a.string != "Tags":
                video.tags.append(str(a.string))
    return video