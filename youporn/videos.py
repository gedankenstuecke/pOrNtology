import urllib2
from bs4 import BeautifulSoup

class Video():
    '''
    Set up simple video-class
    '''
    def __init__(self):
        self.url = ""
        self.tags = []
        self.categories = []
        self.length = "-"
        self.date = "-"
    
    def __repr__(self):
        return "%s, Tags: %s, Categories: %s, %s, %s" % (self.url,str(self.tags),str(self.categories),self.length,self.date)

def GetVideoTags(videourl):
    video = Video() # initialize new video
    try: # failsafe: youporn is great in giving links to broken URLs which crash everything. 
        opener = urllib2.build_opener()
        opener.addheaders.append(("Cookie","age_verified=1"))
        url = opener.open(videourl)
        urlcontent = url.read() # read content
        soup = BeautifulSoup(urlcontent,"xml") # parse using the xml-parser & beautiful soup
        video.url = str(videourl)
        length_date = soup.find("ul",{"class":"spaced"}).findAll("li")
        for element in length_date:
            if element.getText().find("Duration:") != -1:
                video.length = element.getText()[element.getText().find("Duration:")+10:]
            elif element.getText().find("Date:") != -1:
                video.date = element.getText()[element.getText().find("Date:")+6:]
        tag_elements = soup.find("ul",{"class":"listCat"}).findAll("a") # iterate over all <a></a>-tags
        for element in tag_elements:
            if element["href"].find("porntags") == -1:
                video.categories.append(str(element.string))
            else:
                video.tags.append(str(element.string))
    except:
        pass
    return video