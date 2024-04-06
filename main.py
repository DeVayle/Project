from tkinter import *
from tkinter import font
import tkinter as tk
import ctypes
import winsound

ctypes.windll.shcore.SetProcessDpiAwareness(1)
platforms = []
exits = []
pressed_keys = set()

def key_pressed(event):
    pressed_keys.add(event.keysym)

def key_released(event):
    pressed_keys.remove(event.keysym)


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
            winsound.PlaySound('music/berlin.wav',
                              winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
            music_playing.set(True)
            music_button.configure(text='Выключить музыку')

    music_button = tk.Button(window, command=music, font=btn_font)
    music_button.place(anchor="center", relx=.15, rely=.61, relheight=.1, relwidth=.2)

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
    lbl_gamename = tk.Label(window, text="AeroCube", font=btn_font)
    lbl_gamename.place(anchor="center", relx=.2, rely=.2, relheight=.1, relwidth=.2)

    btn_play = tk.Button(window, text="Играть", command=level_1, font=btn_font)
    btn_play.place(anchor="center", relx=.15, rely=.5, relheight=.1, relwidth=.2)

    btn_sett = tk.Button(window, text="Настройки", command=settings, font=btn_font)
    btn_sett.place(anchor="center", relx=.15, rely=.61, relheight=.1, relwidth=.2)

    btn_exit = tk.Button(window, text="Выход", command=window.destroy, font=btn_font)
    btn_exit.place(anchor="center", relx=.15, rely=.72, relheight=.1, relwidth=.2)


def move():
    x1, y1, x2, y2 = character_canvas.coords(character)
    if (x1 > 0 and check_collision_platforms(x1, y1, x2, y2)) or (x2 < window.winfo_width() and check_collision_platforms(x1, y1, x2, y2)) != 'left_or_right':
        vel = -10 * ("Left" in pressed_keys) + 10 * ("Right" in pressed_keys)
        character_canvas.move(character, vel, 0)
        check_collision_exits()
        window.after(25, move)  # Повторить перемещение через 50 мс

# Инициализация возможных описаний персонажа "В воздухе" и "В прыжке"
in_air = False
jumping = False

def move_up(event):
    global in_air, jumping
    x1, y1, x2, y2 = character_canvas.coords(character)
    if not in_air:  # Проверка, находится ли персонаж в воздухе
        in_air = True
        jumping = True
        jump_up(y1)  # Используется начальная У-координата, с которой происходит прыжок

def jump_up(initial_y):
    global in_air, jumping
    x1, y1, x2, y2 = character_canvas.coords(character)
    if y1 > initial_y - 300:  # Проверка, достиг ли персонаж во время прыжка своей максимальной высоты прыжка
        character_canvas.move(character, 0, -15)
        window.after(15, lambda: jump_up(initial_y))  # Вызов функции еще раз после задержки
    else:
        jumping = False


def apply_gravity():
    global in_air, jumping
    # Получение текущих координат персонажа
    x1, y1, x2, y2 = character_canvas.coords(character)

    # Проверка, находится ли персонаж на земле или на платформе
    if y2 < window.winfo_height() and check_collision_platforms(x1, y1, x2, y2) != 'top_or_bottom':
        # Если персонаж находится в воздухе, начать опускать его вниз (эффект гравитации)
        character_canvas.move(character, 0, 15)
        in_air = True
    else:
        in_air = False
        jumping = False
    # Вызов функции еще раз после задержки
    window.after(30, apply_gravity)


def check_collision_platforms(x1, y1, x2, y2):
    for platform in platforms:
        px1, py1, px2, py2 = character_canvas.coords(platform)
        if (px1 < x1 < px2 or px1 < x2 < px2) and (py1 - 10 < y2 < py1 + 10 or py1 - 10 < y1 < py1 + 10):
            return 'top_or_bottom'
        elif (py1 < y1 < py2 or py1 < y2 < py2) and (px1 - 10 < x2 < px1 + 10 or px2 - 10 < x1 < px2 + 10):
            return 'left_or_right'
    return None

def check_collision_exits():
    x1, y1, x2, y2 = character_canvas.coords(character)
    for exit in exits:
        ex1, ey1, ex2, ey2 = character_canvas.coords(exit)
        if (ex1 < x1 < ex2 or ex1 < x2 < ex2) and (ey1 - 10 < y2 < ey1 + 10 or ey1 - 10 < y1 < ey1 + 10):
            level_2()


def create_character():
    global character_canvas, character
    character_canvas = tk.Canvas(window, bg="DarkGray", width=1920, height=1080)
    character_canvas.place(anchor="center", relx=.5, rely=.5)

    btn_pause = tk.Button(window, text="II", command=restore_menu, font=btn_font)
    btn_pause.place(anchor="center", relx=.026, rely=.046, relwidth=.03125, relheight=.05)

    character = character_canvas.create_rectangle(800, 1020, 860, 1080, fill="blue")

    # Назначение клавиш для функций передвижения
    move()
    window.bind("<Up>", move_up)

    window.bind_all('<KeyRelease>', key_released)
    window.bind_all('<KeyPress>', key_pressed)

    apply_gravity()


def create_platform(x, y, width, height):
    # Создание платформ в character_canvas
    platform = character_canvas.create_rectangle(x, y, x + width, y + height, fill="green")
    platforms.append(platform)


def create_exit(x, y, width, height):
    exit = character_canvas.create_rectangle(x, y, x + width, y + height, fill="red")
    exits.append(exit)


def level_1():
    clear_window()
    create_character()

    create_platform(100, 900, 200, 20)
    create_platform(500, 650, 100, 20)
    create_platform(1400, 700, 150, 20)
    create_exit(1800, 1020, 100, 100)


def level_2():
    clear_window()
    create_character()



window = tk.Tk()
window.title('2D-Platformer')
window.geometry("1280x720")
window.attributes('-fullscreen', True)

btn_font = font.Font(font=('Arial', 22))

winsound.PlaySound('music/berlin.wav', winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
music_playing = BooleanVar()
music_playing.set(True)

main_menu()
window.mainloop()