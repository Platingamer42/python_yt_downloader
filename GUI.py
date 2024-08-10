try:
    import tkinter as tk
    from tkinter import scrolledtext
except: # Python2 compatible
    import Tkinter as tk
    from Tkinter import scrolledtext
from turtle import bgcolor
from Downloader import Downloader
import os
import urllib
from PIL import Image, ImageTk

class GUI:
    _version_str = "V1.0"
    def __init__(self):
        self.init_downloader()

        self.root = tk.Tk()

        self.root.title("YouTube converter " + self._version_str)
        self.root.geometry('405x280')

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        subMenu = tk.Menu(menubar)
        subMenu.add_command(label="Download from .txt file", command=self.download_from_file)
        subMenu.add_command(label="EXIT", command=self.exit)
        menubar.add_cascade(label="Options", menu=subMenu)
        #self.root.resizable(False, False)

        #for resizing reasons, we open this as normal Image now.
        self.background_image = Image.open(os.path.dirname(os.path.realpath(__file__)) + "\\images\\background.jpg")
        self.background_label = tk.Label(self.root, image=ImageTk.PhotoImage(self.background_image))
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.image = self.background_image
        self.background_label.bind('<Configure>', self.on_resize) # on_resize will be executed whenever label l is resized0

        self._create_upper_frame()
        self._fill_upper_frame()

        self._create_lower_frame()
        self._fill_lower_frame()

    def _create_upper_frame(self):
        #upper frame (buttons and input)
        self.frame1 = tk.Frame(master=self.root, bg="#FFCFC9")
        self.frame1.grid(row=0, columnspan=1, padx=30, pady=10, sticky=tk.E + tk.W)
        
        self.frame1.rowconfigure(0, weight=1)
        self.frame1.columnconfigure(1, weight=1)

        #self.root.rowconfigure(0,1)
        #self.root.columnconfigure(0,1)
    
    def _fill_upper_frame(self):
        #input label
        dummyframe = tk.Frame(master=self.frame1, bg="#FFFFFF")
        dummyframe.rowconfigure(0, weight=1)
        dummyframe.columnconfigure(0, weight=1)
        dummyframe.columnconfigure(1, weight=1)



        self.lbl_input = tk.Label(master=dummyframe, text="Link: ")
        self.lbl_input.grid(row=0, column=0, sticky=tk.E + tk.W)
        
        #txtlabel
        self.txt = tk.Entry(master=dummyframe, width=50)
        self.txt.insert(5, "https://www.youtube.com/watch?v=hTWKbfoikeg")
        self.txt.grid(row=0, column=1, columnspan=2, sticky=tk.E + tk.W)

        dummyframe.grid(row=0, column=1, sticky=tk.E + tk.W)


        #buttons
        self.btn_download = tk.Button(self.frame1, text="DOWNLOAD", command=self.btn_download_clicked)
        self.btn_download.grid(row=1, column=1, columnspan=1)

        self.btn_fetch_info = tk.Button(self.frame1, text = "FETCH INFO", command=self.btn_fetch_info_clicked)
        self.btn_fetch_info.grid(row=2, column=1, columnspan=1)

    def _create_lower_frame(self):
        # #lower frame (information)
        self.frame2 = tk.LabelFrame(master=self.root, bg="#FFCFC9")
        self.frame2.grid(row=1, padx=30, pady=10, sticky=tk.E+tk.W+tk.N+tk.S)
        self.frame2.rowconfigure(0, weight=1)
        self.frame2.columnconfigure(0, weight=1)
        
    def _fill_lower_frame(self):
        #info
        self.lbl_uploader = tk.Label(self.frame2, text="Uploader: ----------", width=50)
        self.lbl_uploader.grid(row=0)

        self.lbl_title = tk.Label(self.frame2, text="Title: ----------", width=50)
        self.lbl_title.grid(row=1 )

        self.lbl_debug = tk.Label(self.frame2, text="DEBUG: ", width = 50)
        self.lbl_debug.grid(row=2)

        self._create_thumbnail_frame()
        self._fill_thumbnail_frame()

    def _create_thumbnail_frame(self):
        # #thumbnail-frame
        self.frame3 = tk.Frame(master=self.frame2, bg="black")
        self.frame3.grid(row=3)
        self.frame3.rowconfigure(0, weight=1)
        self.frame3.columnconfigure(0, weight=1)

    def _fill_thumbnail_frame(self):
        self.update_thumbnail(os.path.dirname(os.path.realpath(__file__)) + "\\images\\icon.png")



    def on_resize(self, event):
        # resize the background image to the size of label
        image = self.background_image.resize((event.width, event.height), Image.Resampling.LANCZOS)
        # update the image of the label
        self.background_label.image = ImageTk.PhotoImage(image)
        self.background_label.config(image=self.background_label.image)

    def update_thumbnail(self, url):
        self.canv = tk.Canvas(self.frame3, width=128, height=72, bg="white")
        self.canv.grid(row=0)
        img = Image.open(url)
        img.thumbnail((128,72))
        img.save(url)
        img = ImageTk.PhotoImage(Image.open(url))
        self.canv.image = img
        self.canv.create_image(0,0,anchor=tk.NW,image=img)

    def init_downloader(self):
        self.downloader = Downloader()

    def btn_download_clicked(self):
        #print(self.txt.get())
        #self.downloader.urls = self.txt.get()
        
        url = self.txt.get()
        debug = self.downloader.download_song([url])
        self.update_debug(debug)

    def download_from_file(self):
        print("What.")
        urls = self.downloader.read_url_file()
        debug = self.downloader.download_song(urls)
        self.update_debug(debug)

    def btn_fetch_info_clicked(self):
        url = self.txt.get()
        print(url)
        uploader, title, thumbnail_link, debug = self.downloader.fetch_song_info(url)
        # print("U:" + uploader)
        # print("T: " + title)
        # print("TN: " + thumbnail_link)
        self.update_debug(debug)
        self.lbl_uploader.configure(text = "Uploader: " + uploader)
        self.lbl_title.configure(text = "Title: " + title)

        urllib.request.urlretrieve(thumbnail_link, "images\\thumbnail.jpg")
        #time.sleep(5)
        self.canv.destroy()        
        self.update_thumbnail(os.path.dirname(os.path.realpath(__file__)) + "\\images\\thumbnail.jpg")      
    
    def update_debug(self, debug):
        self.lbl_debug.configure(text = "DEBUG: " + debug)


    def exit(self):
        quit()

if __name__ == "__main__": 
    gui =GUI()
    gui.root.mainloop()
else:
    print("GUI must run as main function")