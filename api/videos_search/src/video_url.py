import re
import datetime
import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

GOOGLE_URL_SEARCH="https://www.google.com/search?q="

GET_HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,charset=UTF-8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'close'}

SESSION = requests.Session()
SESSION.trust_env = False

def get_soup_html(url, headers = GET_HEADER):
    resp = SESSION.get(url, headers = headers)
    http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
    encoding = html_encoding or http_encoding
    soup = BeautifulSoup(resp.content, 'lxml', from_encoding=encoding)

    return soup

def get_page_videos(url):
    soup = get_soup_html(url)
    for tag in soup.find_all("video"):
        video_url = tag.source["src"]
        yield (video_url, soup.title.string, get_video_info(video_url))

def get_video_info(video_url):
    headers = SESSION.get(video_url, stream = True).headers
    return {
        "formato" : headers["Content-Type"],
        "ultima_modificação" : headers["Last-Modified"],
        "tamanho" : int(headers["Content-Length"])/1024
    }

get_google_url = lambda search_text: GOOGLE_URL_SEARCH+search_text
get_google_links = lambda url: [tag.a["href"] for tag in get_soup_html(url).find_all("div","rc")]

def get_videos(seach_text, max_videos):
    for link in get_google_links(get_google_url(seach_text)):
        for video_url, page_title, video_info in get_page_videos(link):
            yield {
                "url" : video_url,
                "page_title" : page_title,
                "page_url" : link,
                "video_info" : video_info,
                "keywords" : seach_text.split(" "),
                "addition_date" : datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }


if __name__ == "__main__":
    list(get_videos("naruto ep 1", 10))