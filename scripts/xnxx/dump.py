import videos
import pickle
import datetime

def readVideos(handle):
    filehandle = open(handle,"rb")
    video_collection = pickle.load(filehandle)
    return video_collection
    
def csvOutput(video_collection):
    deadline = datetime.date(2012,8,12)
    videosTimeFiltered = open("videos_crawltime_filtered.csv","w")
    videosAll = open("videos_raw.csv","w")
    
    header = "url;upload date(dd.mm.yyyy);upload hour;upload minute;length;number of tags;tags\n"
    videosAll.write(header)
    videosTimeFiltered.write(header)
    counter = 0
    for url,video_object in video_collection.items():
        counter += 1
        output = url + ";"
        try:
            year = int(video_object.date.split(" ")[0].split("/")[-1])
            month = int(video_object.date.split(" ")[0].split("/")[0])
            day = int(video_object.date.split(" ")[0].split("/")[1])
            upload_date = datetime.date(year,month,day)
            
            upload_time = video_object.date.split(" ")[1]
            pm = video_object.date.split(" ")[-1]
            minute = int(upload_time.split(":")[-1])
            if pm == "pm":
                hour = int(upload_time.split(":")[0])+12
            else:
                hour = int(upload_time.split(":")[0])
            output = output + str(day) + "." + str(month) + "." + str(year) + ";"
            output = output + str(hour) + ";" + str(minute) + ";"
        except:
            print video_object.date
            output = output + "-;-;-;"
            upload_date = "-"
        output = output + str(video_object.length) + ";"
        output = output + str(len(video_object.tags)) + ";"
        output = output + "\t".join(video_object.tags)+"\n"
        videosAll.write(output)
        if upload_date != "-":
            if upload_date < deadline:
                videosTimeFiltered.write(output)
        else:
            videosTimeFiltered.write(output)
        
        if counter % 1000 == 0:
            print "wrote "+ str(counter) + " videos"