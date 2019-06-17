from videos_search.src import video_url
from videos_search.src.firebase_database import Database

from videos_search.settings import MAX_SCRAPED_VIDEOS

class VideoManager:
    _db = Database("videos")

    def create_video(self, save,*args, **kwargs):
        video_obj = object.__new__(Video)
        video_obj.__init__(*args, **kwargs)
        if save:
            video_obj.save(self._db)

        return video_obj

    def all(self):
        objects_dict = self._db.read()
        for obj_dict in objects_dict:
            yield self.create_video(False, **obj_dict)
    
    def filter(self):
        pass

class Video:
    objects = VideoManager()
    
    def __init__(self, url, page_title, page_url, addition_date, keywords, 
                 video_info, likes = 0, deslikes = 0, visualizations = 0, number_querys = 0):

        self.url = url
        self.page_title = page_title
        self.page_url = page_url
        self.addition_date = addition_date
        self.keywords = keywords
        self.video_info = video_info

        self.likes = likes
        self.deslikes = deslikes
        self.visualizations = visualizations
        self.number_querys = number_querys

    def save(self, db):
        db.insert(self.page_title, self.json())

    def json(self):
        return {
            "url" : self.url,
            "page_title" : self.page_title,
            "page_url" : self.page_url,
            "addition_date" : self.addition_date,
            "keywords" : self.keywords,
            "video_info" : self.video_info,
            "likes" : self.likes,
            "deslikes" : self.deslikes,
            "visualizations" : self.visualizations,
            "number_querys" : self.number_querys
        }
    
    def __new__(cls, *args, **kwargs):
        return cls.objects.create_video(True, *args, **kwargs)
    
    @classmethod
    def search_videos(cls, seach_text, max_videos = MAX_SCRAPED_VIDEOS):
        for video_dict in video_url.get_videos(seach_text, max_videos):
            yield Video(**video_dict)

if __name__ == "__main__":
    test = Video("https://video.google.com", "Overlord ep 3", "https://google.com","1/1/2013", 
                 ["overlord","ep", "1"], {"duration":"10min","title":"overlord ep 1"})

    print(len(list(test.objects.all())))