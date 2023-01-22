import os
import pickle
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import pygame.mixer_music
from pygame import mixer
from PIL import ImageTk, Image

root = Tk() #create a frame
root.geometry('600x400') #create a size
root.wm_title('MUSIC') #name
root.resizable(False, False)
pygame.mixer.init()




class Player(tk.Frame): #закидываем root в наш класс
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.create_frames()
        self.main_image()
        self.get_control()
        self.scroll_bar()
        self.songs = []

#Create_Windows
    def create_frames(self):
        self.frame_top = Frame(root, bg = 'dimgrey')
        self.frame_top.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.5)

        self.top = Label(self.frame_top, text="Songs", font=('Impact', 15), padx=0, pady=9, bg='dimgrey')
        self.top.place(x=0, y=0)

        self.left = Frame(root, bg='dimgrey')
        self.left.place(relx=0, rely=0, relwidth=0.5, relheight=0.7)

        self.right_lst = Listbox(root, selectmode=SINGLE, font=("Arial 9 bold", 17),  bg='dimgrey', fg="White")
        self.right_lst.place(relx=0.5, rely=0.1, relwidth=0.5, relheight=0.6)

        self.down = Frame(root, bg='aqua')
        self.down.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)


#List_for_Songs
    def show(self): #показывает список песен
        for song in self.songs:
            self.right_lst.insert("end", song) #ПоказываетСписокПесен


    def scroll_bar(self):
        self.bar = Scrollbar(self.right_lst)
        self.bar.place(relx=0.95)

        self.right_lst.configure(yscrollcommand=self.bar.set)
        self.bar.config(command= self.right_lst.yview)


#Main_image
    def main_image(self):
        self.image_1 = Label(self.left, height=200, width=200, image=image_1, bg='dimgrey')
        self.image_1.place(x=43, y=24)

#Controls
    def get_control(self):
        self.load_songs = Button(self.down, bg='Green', fg='Black', font='Arial 9 bold')
        self.load_songs['text'] = 'Load Songs'
        self.load_songs['command'] = self.retrieve_songs
        self.load_songs.place(x=300, y=0)

        self.play = Button(self.down, height=40, width=40, image=image_play, background = 'aqua')
        self.play['command'] = self.play_song
        self.play.place(x=101, y=7)

        self.stop = Button(self.down, height=40, width=40, image=image_stop, background='aqua')
        self.stop['command'] = self.stop_song
        self.stop.place(x=149, y=7)

        self.prev = Button(self.down, height=40, width=40, image=image_prev, bg = 'aqua')
        self.prev["command"] = self.prev_song
        self.prev.place(x=53, y=7)

        self.next = Button(self.down, height=40, width=40, image=image_nex, bg = 'aqua')
        self.next['command'] = self.next_song
        self.next.place(x=197, y=7)

        self.volume = DoubleVar() #хранилище
        self.slider = Scale(self.down, from_=0, to=10, orient=tk.HORIZONTAL, bg = 'aqua') #создвниеПолзунка
        self.slider['variable'] = self.volume #чтоОнРегулирует
        self.slider.set(8) #приОткрытииЭтоБудетДефолт
        mixer.music.set_volume(0.8)
        self.slider['command'] = self.change_volume
        self.slider.place(x=98, y=55)

#загрузка песен в ScrollBar
    def retrieve_songs(self):
        global current_song
        self.directory = filedialog.askdirectory()

        for song in self.songs:
            if song in self.songs:
                self.delete()   #удаляем старый список песен

        for song in os.listdir(self.directory):
            name, ext = os.path.splitext(song)

            if ext == ".mp3":
                self.songs.append(song)

        self.show()

        self.right_lst.selection_set(0)
        current_song = self.songs[self.right_lst.curselection()[0]]


#delete - для того, чтобы при обновлении папки, старый список песен удалялся
    def delete(self):
        self.right_lst.delete(0, tk.END)
        self.top['text'] = "Songs"
        if len(self.songs) > 0:
            self.songs.clear()



    #def: play, prev, next, stop, volume
    def play_song(self):
        global current_song, paused

        if not paused:
            self.top['text'] = current_song
            pygame.mixer_music.load(os.path.join(self.directory, current_song))
            pygame.mixer_music.play()
        else:
            pygame.mixer_music.unpause()
            paused = False


    def prev_song(self):
        global current_song, paused
        #try, except - чтобы не выскакивала ошибка, когда добираемся
        #до конца списка песен
        try:
            self.right_lst.selection_clear(0, tk.END)
            self.right_lst.selection_set(self.songs.index(current_song) - 1)
            current_song = self.songs[self.right_lst.curselection()[0]]
            self.play_song()
        except:
            pass


    def next_song(self):
        global current_song, paused

        try:
            self.right_lst.selection_clear(0, tk.END)
            self.right_lst.selection_set(self.songs.index(current_song) + 1)
            current_song = self.songs[self.right_lst.curselection()[0]]
            self.play_song()
        except:
            pass

    def stop_song(self):
        mixer.music.stop()

    def change_volume(self, event=None):
        self.v = self.volume.get()
        mixer.music.set_volume(self.v / 10)


#распаковка изображений
image_1 = Image.open('/Users/igorbogdanov/Desktop/Pictures/1663595084_1-top-fon-com-p-serii-depressivnii-fon-foto-1.png')
image_1 = image_1.resize((200, 200))
image_1 = ImageTk.PhotoImage(image_1)

image_play = Image.open('/Users/igorbogdanov/Desktop/Pictures/play.png')  #открываю изображение
image_play = image_play.resize((27, 27))
image_play = ImageTk.PhotoImage(image_play)

image_prev = Image.open('/Users/igorbogdanov/Desktop/Pictures/prev.png')  #открываю изображение
image_prev = image_prev.resize((25, 25)) #изменяю размер
image_prev = ImageTk.PhotoImage(image_prev) #загружаем изображение

image_nex = Image.open('/Users/igorbogdanov/Desktop/Pictures/next.png')
image_nex = image_nex.resize((25, 25))
image_nex = ImageTk.PhotoImage(image_nex)

image_stop = Image.open('/Users/igorbogdanov/Desktop/Pictures/stop.png')
image_stop = image_stop.resize((25, 25))
image_stop = ImageTk.PhotoImage(image_stop)

mixer.init()
music_ctate = StringVar()
music_ctate.set("Choose one!")

current_song = ""
paused = False


app = Player(master=root)
app.mainloop()



























