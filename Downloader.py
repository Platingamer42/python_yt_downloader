from __future__ import unicode_literals
import os
import youtube_dl

class Downloader:
    def __init__(self):
        self. ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.dirname(os.path.realpath(__file__)) + '/output/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '256',
            }],
        }
        
    def init_as_main(self): 
        urls = self.read_url_file()
        self.download_song(urls)

    def read_url_file(self):
        with open ((os.path.dirname(os.path.realpath(__file__)) + '\\urls.txt'), 'rt') as myfile:
            contents = myfile.read()
        splitted = contents.split()
        print(splitted) 
        return splitted

    def download_song(self, url):  
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            try: 
                ydl.download(url)
                return "download successfull"
            except Exception:
                return "An error occured"

    def fetch_song_info(self, url):
        title = " "
        uploader = " "
        thumbnail_link = " "
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            try: 
                print("URLS: " + url)
                infosearched = ydl.extract_info(url, download=False)
                #print(infosearched)
                uploader = infosearched["uploader"]
                title = infosearched['title']
                thumbnail_link = infosearched["thumbnail"]

                debug = "information collected"
            except Exception:
                debug = "An error occured"
        return [uploader, title, thumbnail_link, debug]

if __name__ == "__main__":
    # execute only if run as a script
    main = Downloader()
    main.init_as_main()