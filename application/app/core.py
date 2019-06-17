import re
import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

from django.conf import settings

GOOGLE_URL_SEARCH="https://www.google.com/search?q="

GET_HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,charset=UTF-8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'close'}

SESSION = requests.Session()
SESSION.trust_env = False

class Page_video():
    def __init__(self, url, title):
        self.title = title
        self.url = url
    
    def __str__(self):
        return self.url

    @classmethod
    def get_page_videos(cls, url):
        soup = get_soup_html(url)
        page_videos = []
        for tag in soup.find_all("video"):
            try:
                url = tag.source["src"]
                if soup.title:
                    title = soup.title.string
                else:
                    title = "Sem titulo"
                page_videos.append(Page_video(url,title))
            except:
                pass

        return page_videos
    
    @classmethod
    def search_videos(cls, seach_text, max_videos = settings.MAX_SHOW_VIDEOS):
        links = get_google_links(seach_text)
        videos = []
        for link in links:
            print(link)
            _videos = cls.get_page_videos(link)
            videos = videos + _videos
            if max_videos!=None and len(videos) >= max_videos:
                break
        
        return videos


def get_soup_html(url, headers = GET_HEADER):
    resp = SESSION.get(url, headers = headers)
    http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
    encoding = html_encoding or http_encoding
    soup = BeautifulSoup(resp.content, 'lxml', from_encoding=encoding)

    return soup

def get_google_links(search_text):
    soup = get_soup_html(GOOGLE_URL_SEARCH+search_text+"&lr=lang_pt-BR&hl=pt-BR")
    links = [tag.a["href"] for tag in soup.find_all("div","rc")]
    print("links:"+str(links))
    return links


if __name__ == "__main__":
    print(Page_video.search_videos("overlord ep 1")[0])