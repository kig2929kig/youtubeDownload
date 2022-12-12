from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from threading import *
from pytube import YouTube
import os

window_size_width = 450
window_size_height = 150
save_folder = "./youtube"


def threading() :
    btn_download_thread = Thread(target=youtubu_download)
    btn_download_thread.start()

def progress_complete(self, file_path) :
   btn_download['state'] = "active"
   url_entry.delete(0,END)

def progress_callback(stream, chunk, bytes_remaining) :
    global prs_label
    value = ((stream.filesize - bytes_remaining) / stream.filesize) * 100
    value = round(value, 2)
    progress_current_value.set(value)
    prs_label.set(str(value) + "%")
    progress_bar.update()
    #progress_label.update()    
       
def youtubu_download() :
    btn_download['state'] = "disable"
    url = url_entry.get()    
    yt = YouTube(url, on_progress_callback=progress_callback, on_complete_callback=progress_complete)
    down_clip = yt.streams.get_highest_resolution().download(save_folder)

def url_entry_clear() :
    url_entry.delete(0, END)

def brower_open_button() :    
    if not os.path.exists(save_folder) :
        os.mkdir(save_folder)
    else :
        pass    
    path = os.path.realpath("youtube")
    os.startfile(path)    

# start
#################################################################################################################
root = Tk() # 최상위 레벨의 윈도우(window) 생성
#root.iconphoto(False, PhotoImage(file='icon\download.png')) # Fase - 특정 창에만 적용
root.title("YouTube Downloader by kig2929kig") # 윈도우 제목 표시줄
root.geometry(str(window_size_width) + "x" + str(window_size_height)) # 너비 x 높이 + x좌표 + y좌표
root.resizable(False, False) # 윈도우 크기 조절 - True(가능), False(불가능)
root.config(background='white')

url_Frame = LabelFrame(root, text="주소(URL)")
url_Frame.pack(padx=5, pady=5, fill="x")

progress_frame = LabelFrame(root, text="진행률")
progress_frame.pack(padx=5, pady=5, fill="both")

# url_Frame
#################################################################################################################
url_entry = Entry(url_Frame)
url_entry.pack(padx=2, pady=10, fill="both", expand="yes", side="left")

#btn_clear_icon = PhotoImage(file = r"icon\close.png")
#btn_clear_icon = btn_clear_icon.subsample(40,40)
#btn_url_clear = Button(url_Frame , text="x", image=btn_clear_icon, command=url_entry_clear)
btn_url_clear = Button(url_Frame , text="x", command=url_entry_clear)
btn_url_clear.pack(padx=2, side="left")

#btn_folder_icon = PhotoImage(file = r"icon\folder.png")
#btn_folder_icon = btn_folder_icon.subsample(30,35)
#btn_url = Button(url_Frame , text="...", image=btn_folder_icon, command=brower_open_button)
btn_url = Button(url_Frame , text="...", command=brower_open_button)
btn_url.pack(padx=2, side="left")
#################################################################################################################

# progress_frame
#################################################################################################################
progress_current_value = DoubleVar()
prs_label = StringVar()
progress_bar = ttk.Progressbar(progress_frame, maximum=100, variable=progress_current_value)
progress_bar.pack(padx=1, pady=10, fill="both", expand="yes", side="left")
progress_label = Label(progress_frame, textvariable=prs_label)
progress_label.pack(padx=2, side="left")
btn_download = Button(progress_frame, text="다운로드", command=threading)
btn_download.pack(padx=2, side="left")
#################################################################################################################

# end
root.mainloop() # 윈도우(window) 종료될 때까지 실행