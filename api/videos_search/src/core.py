from videos_search.src.models import Video

all_videos = lambda : [video.json() for video in Video.objects.all()]
search_videos = lambda text : [video.json() for video in Video.search_videos(text)]
