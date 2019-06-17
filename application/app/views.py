from django.shortcuts import render

from .core import Page_video

# Create your views here.
def index(request):
    if request.method == 'POST':
        try:
            search_text = request.POST["Search_box"]
            videos=Page_video.search_videos(search_text)
            if(len(videos) == 1):
                col_size = 6
                offset_size = 3
            else:
                col_size = int(12/len(videos))
                offset_size = 0
        except ZeroDivisionError as e:
            if settings.DEBUG:
                return render_template("index.html",error_msg="Nenhum video encontrado")
                


        return render(request, "app/index.html", {"videos" : videos, "col_size" : col_size, 
                                                         "offset_size" : offset_size})

    return render(request,"app/index.html")