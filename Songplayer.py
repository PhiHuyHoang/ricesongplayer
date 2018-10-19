import urllib.request
from urllib.parse import *
from bs4 import BeautifulSoup
import os,re
import youtube_dl, pafy
import time

class Youtube_mp3():
    def __init__(self):
        self.lst = []
        self.dict = {}
        self.dict_names = {}
        self.playlist = []

    def url_search(self, search_string, max_search):
        textToSearch = search_string
        query = urllib.parse.quote(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        i = 1
        for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
            if len(self.dict) < max_search:
                self.dict[i] = 'https://www.youtube.com' + vid['href']
                i += 1
            else:
                break

    def get_search_items(self, max_search):

        if self.dict != {}:
            i = 1
            for url in self.dict.values():
                try:
                    info = pafy.new(url)
                    self.dict_names[i] = info.title
                    print("{0}. {1}".format(i, info.title))
                    i += 1

                except ValueError:
                    pass

    def make_savepath(self, title):
        return os.path.join("%s.mp3" % (title.replace("mp3", "")))


    def play_media(self, num):
        url = self.dict[int(num)]
        options = {
            'format': 'bestaudio/best',
            'outtmpl': '%(id)s'
        }

        ydl = youtube_dl.YoutubeDL(options)
        song_name = ydl.extract_info(url, download=False)
        savepath = self.make_savepath(song_name['title'].replace(" ", ""))
        savepath = re.sub('[^A-Za-z0-9]+', '', savepath)
        savepath = self.make_savepath((savepath))
        with ydl:
            result = ydl.extract_info(url, download=True)
            if os.path.exists(savepath):
                os.remove(savepath)
            os.rename(result['id'], savepath)
        print(savepath)
        os.system("start "+ savepath)


if __name__ == '__main__':
    print('Welcome to the Youtube-Mp3-Rice player.')
    x = Youtube_mp3()
    search = ''
    while search != 'q':
        search = input("Youtube Search: ")
        old_search = search
        max_search = 10
        x.dict = {}
        x.dict_names = {}

        if search == 'q':
            print("Ending Youtube-Mp3 player.")
            keep = input('Want to keep the mp3 file? (Y/N)')
            if keep == 'Y':
                print('OK')
            elif keep == 'N':
                for file in os.listdir():
                    if file.endswith(".mp3"):
                        print(file)
                        os.remove(file)
                print('DONE')
            else:
                print("Don't understand")
            break

        print('\nFetching for: {0} on youtube.'.format(search.title()))
        x.url_search(search, max_search)
        x.get_search_items(max_search)
        song_number = input('Input song number: ')
        x.play_media(song_number)