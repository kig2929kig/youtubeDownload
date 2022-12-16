# _*_ coding: utf-8 _*_
from tkinter import *
import tkinter.messagebox 
from tkinter import ttk
from threading import *
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
import os, sys, ctypes, subprocess
import pygame

window_size_width = 450
window_size_height = 310
save_folder = "youtube"
pause_flag = 0 # pause or unpause flag
music = ""
n = 0 # listbox - music list index
pygame.init()
pygame.mixer.init()
MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)

def resource_path(relative_path) :
    try :
        base_path = sys._MEIPASS
    except Exception :
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def check_event() :
    for event in pygame.event.get() :
        if event.type == MUSIC_END:
            print("종료")
            next()
    root.after(100, check_event)

def prev() :
    global n, music
    
    if n > 0 :
        n = n - 1
        print("--", n)
        music = f_list.get(n)        
        f_list.selection_clear(0, END)
        f_list.selection_set(n)
        f_list.activate(n)
        f_list.see(n)        
        play()
    else :
        pass

def next() :
    global n, music
    
    if n < f_list.size() - 1 :
        n = n + 1
        print("--", n)
        music = f_list.get(n)                
        f_list.selection_clear(0, END)
        f_list.selection_set(n)
        f_list.activate(n)
        f_list.see(n)        
        play()
    else :
        pass
    
def pause() :
    global pause_flag
    if pause_flag == 0 :
        pygame.mixer.music.pause()
        btn_pause.config(text="UNPAUSE", foreground="red")
        pause_flag = 1
        btn_prev['state'] = 'disable'
        btn_next['state'] = 'disable'
    else :
        pygame.mixer.music.unpause()
        btn_pause.config(text="PAUSE", foreground="black")
        pause_flag = 0
        btn_prev['state'] = 'active'
        btn_next['state'] = 'active'

def music_select(event) :
    global music, n, play
    selection = f_list.curselection()
    n = selection[0]
    print(n)
    music = f_list.get(n)
    print(music)
    #stop()
    btn_play['state'] = "active"
    btn_prev['state'] = 'disable'
    btn_next['state'] = 'disable'
    play()
   
def play() :   
    global music
    path= f"./youtube/{music}"
    print(path)
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    btn_play.config(foreground="gray")
    btn_play["state"] = "disable"
    btn_stop.config(foreground="black")
    btn_stop["state"] = "active"
    btn_pause.config(foreground="black")
    btn_pause["state"] = "active"
    btn_prev.config(foreground="black")
    btn_prev["state"] = "active"
    btn_next.config(foreground="black")
    btn_next["state"] = "active"
    
def stop() :
    global n
    pygame.mixer.music.stop()
    
    n=f_list.size()-1
    f_list.selection_clear(0, END)
    f_list.selection_set(n)
    f_list.activate(n)
    f_list.see(n) 
           
    btn_stop.config(foreground="black")
    btn_stop["state"] = "disable" 
    btn_play.config(foreground="black")
    btn_play["state"] = "disable"
    btn_pause.config(foreground="gray", text="PAUSE")
    btn_pause["state"] = "disable"     
    btn_prev['state'] = 'disable'
    btn_next['state'] = 'disable'
       
def file_list() :
    if not os.path.exists(save_folder) :
        os.mkdir(save_folder)
    else :
        pass     
    f_list.delete(0,END)
    file_lst = os.listdir(save_folder)
    index = 0
    f_list.activate(index)
    f_list.select_set(index)
    f_list.select_anchor(index)
    for file in file_lst :
        if file.endswith(".mp3") :
            f_list.insert(index, str(file))
            index += 1    
        
def threading() :
    btn_download_thread = Thread(target=youtubu_download)
    btn_download_thread.start()

def progress_complete(self, file_path) :
    global file_list
    #url_entry.delete(0,END)
   
    if (radio_value.get() == "mp3"):
        try :
            btn_download.config(text="변환중..")
            #print(file_path)
            mp4 = VideoFileClip(file_path)
            mp4.audio.write_audiofile(file_path[:-3]+"mp3") 
            mp4.close()            
            os.remove(file_path)
            btn_download.config(text="다운로드")
            
            
        except Exception as e:
            tkinter.messagebox.showinfo("error", e)
            
             
    file_list()
    btn_download['state'] = "active"
    
def progress_callback(stream, chunk, bytes_remaining) :
    value = ((stream.filesize - bytes_remaining) / stream.filesize) * 100
    value = round(value, 2)
    progress_current_value.set(value)
    prs_label.set(str(value) + "%")
    progress_bar.update()     
       
def youtubu_download() :
    global file
    
    url = url_entry.get()    
    yt = YouTube(url, on_progress_callback=progress_callback, on_complete_callback=progress_complete)
    btn_download['state'] = "disable"
    yt.streams.get_highest_resolution().download(save_folder)
               
def url_entry_clear() :
    url_entry.delete(0, END)

def brower_open_button() :    
    path = os.path.realpath("youtube")
    os.startfile(path)    

# start
#################################################################################################################
root = Tk() # 최상위 레벨의 윈도우(window) 생성
root.iconphoto(False, PhotoImage(file=resource_path('icon\download.png'))) # Fase - 특정 창에만 적용
root.title("YouTube Downloader by kig2929kig") # 윈도우 제목 표시줄
root.geometry(str(window_size_width) + "x" + str(window_size_height)) # 너비 x 높이 + x좌표 + y좌표
root.resizable(False, False) # 윈도우 크기 조절 - True(가능), False(불가능)
#root.config(background='white')

url_Frame = LabelFrame(root, text="주소(URL)")
url_Frame.pack(padx=5, pady=5, fill="x", expand="yes")

progress_select_frame = Frame(root)
progress_select_frame.pack(padx=5, pady=5, fill="x", expand="yes")

progress_frame = LabelFrame(progress_select_frame, text="진행률")
progress_frame.pack(padx=5, pady=5, fill="x", expand="yes", side="left")

select_file_frame = LabelFrame(progress_select_frame, text="파일 선택")
select_file_frame.pack(padx=5, pady=5, fill="y", side="left")

folder_list_frame = LabelFrame(root, text="mp3 목록")
folder_list_frame.pack(padx=5, pady=5, fill="both", expand="yes")

# url_Frame
#################################################################################################################
url_entry = Entry(url_Frame)
url_entry.pack(padx=2, pady=10, fill="both", expand="yes", side="left")

btn_clear_icon = PhotoImage(file =resource_path(r"icon\close.png"))
btn_clear_icon = btn_clear_icon.subsample(40,40)
btn_url_clear = Button(url_Frame , text="x", image=btn_clear_icon, command=url_entry_clear)
#btn_url_clear = Button(url_Frame , text="x", command=url_entry_clear)
btn_url_clear.pack(padx=2, side="left")

btn_folder_icon = PhotoImage(file = resource_path(r"icon\folder.png"))
btn_folder_icon = btn_folder_icon.subsample(2, 2)
btn_url = Button(url_Frame , text="...", image=btn_folder_icon, command=brower_open_button)
#btn_url = Button(url_Frame , text="...", command=brower_open_button)
btn_url.pack(padx=5, side="left")
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

# select_file_frame - radio button
#################################################################################################################
radio_value = StringVar()
radio_value.set("mp3")
mp3_radio_btn = ttk.Radiobutton(select_file_frame, text="mp3", variable=radio_value)
mp4_radio_btn = ttk.Radiobutton(select_file_frame, text="mp4", variable=radio_value)
mp3_radio_btn.config(value="mp3")
mp4_radio_btn.config(value="mp4")
mp3_radio_btn.pack(side="left")
mp4_radio_btn.pack(side="left")
#################################################################################################################
#folder_list_frame
f_list = Listbox(folder_list_frame, activestyle="none")
f_list.pack(fill="both", side="left", expand="yes")
f_list_scrollbar = Scrollbar(folder_list_frame, orient=VERTICAL)
f_list_scrollbar.pack(side="right", fill="y")
f_list.config(yscrollcommand=f_list_scrollbar.set)
f_list_scrollbar.config(command=f_list.yview)
file_list()
f_list.bind("<<ListboxSelect>>", music_select)
    
btn_play = Button(folder_list_frame, text="PLAY", command=play)
btn_play.pack(fill="x")
btn_stop = Button(folder_list_frame, text="STOP", command=stop, foreground="gray")
btn_stop.pack(fill="x")
btn_pause = Button(folder_list_frame, text="PAUSE", command=pause, foreground="gray")
btn_pause.pack(fill="x")
btn_prev = Button(folder_list_frame, text="Prev", command=prev, foreground="gray")
btn_prev.pack(fill="x")
btn_next = Button(folder_list_frame, text="Next", command=next, foreground="gray")
btn_next.pack(fill="x")
btn_play['state'] = 'disable'
btn_pause['state'] = 'disable'
btn_stop['state'] = 'disable'

check_event()
console_hwnd = ctypes.windll.kernel32.GetConsoleWindow ()
ctypes.windll.user32.ShowWindow (console_hwnd, subprocess.SW_HIDE)
# end
root.mainloop() # 윈도우(window) 종료될 때까지 실행