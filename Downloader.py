from __future__ import unicode_literals
import os
import yt_dlp

class Downloader:
    def __init__(self):
        self._format = 'bestaudio/best'
        self._outtmpl = os.path.dirname(os.path.realpath(__file__)) + '/output/%(title)s.%(ext)s'
        self._key = 'FFmpegExtractAudio'
        self._prefferedcodec = 'mp3'
        self._prefferedquality = '256'
        self.ydl_opts = {
            'format': self._format,
            'outtmpl': self._outtmpl,
            'postprocessors': [{
                'key': self._key,
                'preferredcodec': self._prefferedcodec,
                'preferredquality': self._prefferedquality,
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
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try: 
                ydl.download(url)
                return "download successfull"
            except Exception:
                return "An error occured"

    def fetch_song_info(self, url):
        title = " "
        uploader = " "
        thumbnail_link = " "
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
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