from tkinter import *
from tkinter import font
import tkinter as tk
import ctypes
import winsound

ctypes.windll.shcore.SetProcessDpiAwareness(1)

def clear_window():
    for widget in window.winfo_children():
        widget.destroy()

def settings():
    clear_window()
    enabled_screen = BooleanVar()

    def screen_mode():
        if enabled_screen.get() == 0:
            window.attributes('-fullscreen', True)
        else:
            window.attributes('-fullscreen', False)

    def music():
        if music_playing.get() == 1:
            winsound.PlaySound(None, winsound.SND_PURGE)
            music_playing.set(False)
            music_button.configure(text='Включить музыку')

        else:
            winsound.PlaySound('music\static-symphony.wav',
                              winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
            music_playing.set(True)
            music_button.configure(text='Выключить музыку')

    music_button = tk.Button(window, command=music, font=btn_font)
    music_button.place(anchor="center", relx=.15, rely=.61, relheight=.1)

    music_playing.set(True)
    music_button.configure(text='Выключить музыку')

    lbl_screen1 = tk.Label(window, text="Оконный", font=btn_font)
    lbl_screen1.place(anchor="center", relx=.15, rely=.70, relheight=.03, relwidth=.2)
    lbl_screen2 = tk.Label(window, text="режим", font=btn_font)
    lbl_screen2.place(anchor="center", relx=.15, rely=.735, relheight=.04, relwidth=.2)
    enabled_chbtn1 = tk.Checkbutton(window, variable=enabled_screen, command=screen_mode)
    enabled_chbtn1.place(anchor="center", relx=.26, rely=.72)

    btn_back = tk.Button(window, text="Вернуться", command=restore_menu, font=btn_font)
    btn_back.place(anchor="center", relx=.15, rely=.83, relheight=.1, relwidth=.2)

def restore_menu():
    clear_window()
    main_menu()

def main_menu():
    lbl_gamename = tk.Label(window, text="SkyBound", font=btn_font)
    lbl_gamename.place(anchor="center", relx=.2, rely=.2, relheight=.1, relwidth=.2)

    btn_play = tk.Button(window, text="Играть", font=btn_font)
    btn_play.place(anchor="center", relx=.15, rely=.5, relheight=.1, relwidth=.2)

    btn_sett = tk.Button(window, text="Настройки", command=settings, font=btn_font)
    btn_sett.place(anchor="center", relx=.15, rely=.61, relheight=.1, relwidth=.2)

    btn_exit = tk.Button(window, text="Выход", command=window.destroy, font=btn_font)
    btn_exit.place(anchor="center", relx=.15, rely=.72, relheight=.1, relwidth=.2)



window = tk.Tk()
window.title('Platformer')
window.geometry("1280x720")
window.attributes('-fullscreen', True)

btn_font = font.Font(font=('Arial', 22))

winsound.PlaySound('music\static-symphony.wav', winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
music_playing = BooleanVar()
music_playing.set(True)

main_menu()
window.mainloop()