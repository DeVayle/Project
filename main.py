from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
import tkinter as tk
import winsound
import time

platforms = []
exits = []
spikes = []
keys = []
pressed_keys = set()
deaths = 0
k = 0
v = 1


def key_pressed(event):
    pressed_keys.add(event.keysym)


def key_released(event):
    pressed_keys.remove(event.keysym)


def clear_window():
    for widget in window.winfo_children():
        widget.destroy()


def restore_to_menu():
    clear_window()
    main_menu()


def restore_to_menu_from_game():
    global move_running, gravity_running, k, v
    move_running = False
    gravity_running = False

    character_canvas.delete(character)
    for platform in platforms:
        character_canvas.delete(platform)
    for spike in spikes:
        character_canvas.delete(spike)
    for key in keys:
        character_canvas.delete(key)
    for exito in exits:
        character_canvas.delete(exito)

    # Обнуление списков и переменных
    platforms.clear()
    exits.clear()
    spikes.clear()
    keys.clear()
    k = 0
    v = 1

    clear_window()
    main_menu()


def helper():
    bg = tk.Canvas(bg='White', width=1920, height=1080)
    bg.place(x=0, y=0)

    btn_back = tk.Button(window, text='Вернуться', command=restore_to_menu, font=btn_font)
    btn_back.place(anchor="center", relx=.125, rely=.9, relheight=.1, relwidth=.2)


def main_menu():
    background = tk.Canvas(bg='White', width=1920, height=1080)
    background.place(x=0, y=0)

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


    game_name = Canvas(window, width=576, height=162)
    game_name.place(anchor="center", relx=.5, rely=.5)
    game_name.pack()
    game_name_img = tk.PhotoImage('textures/lava.png')
    print(game_name_img.width())
    game_name.create_image(0, 0, anchor='nw', image=game_name_img)

    btn_play = tk.Button(window, text="Играть", command=level_1, font=btn_font)
    btn_play.place(anchor="center", relx=.15, rely=.5, relheight=.1, relwidth=.2)

    btn_help = tk.Button(window, text='Правила Игры', command=helper, font=btn_font)
    btn_help.place(anchor="center", relx=.15, rely=.61, relheight=.1, relwidth=.2)

    music_button = tk.Button(window, command=music, font=btn_font)
    music_button.place(anchor="center", relx=.15, rely=.72, relheight=.1, relwidth=.2)
    music_playing.set(True)
    music_button.configure(text='Выключить музыку')

    btn_back = tk.Button(window, text="Выход", command=window.destroy, font=btn_font)
    btn_back.place(anchor="center", relx=.15, rely=.83, relheight=.1, relwidth=.2)


# Инициализация возможных описаний персонажа "В воздухе" и "В прыжке"
in_air = False
jumping = False
move_running = False
gravity_running = False

time_start = 0


def move():
    global move_running, time_start
    x1, y1, x2, y2 = character_canvas.coords(character)
    collision = check_collision_platforms(x1, y1, x2, y2)
    if "Left" in pressed_keys and collision != 'right' and x1 > 0:
        character_canvas.move(character, -10, 0)
    elif "Right" in pressed_keys and collision != 'left' and x2 < window.winfo_width():
        character_canvas.move(character, 10, 0)
    check_collision_exits()
    check_collision_spikes()
    keys_collected()
    move_running = True
    if time_start == 0: time_start = time.time()
    window.after(20, move)  # Повторить перемещение через 20 мс


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
    if y1 > initial_y - 220:  # Проверка, достиг ли персонаж во время прыжка своей максимальной высоты прыжка
        character_canvas.move(character, 0, -20)
        window.after(3, lambda: jump_up(initial_y))  # Вызов функции еще раз после задержки
    else:
        jumping = False


def apply_gravity():
    global in_air, jumping, gravity_running
    # Получение текущих координат персонажа
    x1, y1, x2, y2 = character_canvas.coords(character)

    # Проверка, находится ли персонаж на земле или на платформе
    collision = check_collision_platforms(x1, y1, x2, y2)
    if y2 < window.winfo_height() and collision != 'top':
        # Если персонаж находится в воздухе, начать опускать его вниз (эффект гравитации)
        character_canvas.move(character, 0, 10)
        in_air = True
    else:
        in_air = False
        jumping = False
    # Вызов функции ещё раз после задержки
    gravity_running = True
    window.after(4, apply_gravity)


def check_collision_platforms(x1, y1, x2, y2):
    for platform in platforms:
        px1, py1, px2, py2 = character_canvas.coords(platform)
        if (px1 < x1 < px2 or px1 < x2 < px2) and (py1 - 10 < y2 < py1 + 10):
            return 'top'
        elif (py1 < y1 < py2 or py1 < y2 < py2) and (px1 - 10 < x2 < px1 + 10):
            return 'left'
        elif (py1 < y1 < py2 or py1 < y2 < py2) and (px2 - 10 < x1 < px2 + 10):
            return 'right'
    return None


def check_collision_spikes():
    global in_air, jumping
    x1, y1, x2, y2 = character_canvas.coords(character)
    for spike in spikes:
        sx1, sy1, sx2, sy2 = character_canvas.coords(spike)
        if (sx1 <= x1 <= sx2 or sx1 <= x2 <= sx2) and (sy1 <= y1 <= sy2 or sy1 <= y2 <= sy2):
            if in_air:
                jumping = False
                in_air = False
            restart_level()
            return 'dead'
    return None


def keys_collected():
    global k
    x1, y1, x2, y2 = character_canvas.coords(character)
    for key in keys:
        kx1, ky1, kx2, ky2 = character_canvas.coords(key)
        if kx1 <= (x1 + x2) / 2 <= kx2 and ky1 <= (y1 + y2) / 2 <= ky2:
            k += 1
            keys.remove(key)  # Удаление ключа из списка
            character_canvas.delete(key)  # Удаление ключа с экрана


def check_collision_exits():
    x1, y1, x2, y2 = character_canvas.coords(character)
    for exito in exits:
        ex1, ey1, ex2, ey2 = character_canvas.coords(exito)
        if (ex1 < x1 < ex2 or ex1 < x2 < ex2) and (ey1 - 10 < y2 < ey1 + 10 or ey1 - 10 < y1 < ey1 + 10):
            next_level()
        elif (ey1 < y1 < ey2 or ey1 < y2 < ey2) and (ex1 - 10 < x2 < ex1 + 10 or ex1 - 10 < x1 < ex1 + 10):
            next_level()


def create_character(x1, y1, x2, y2):
    global character_canvas, character
    character_canvas = tk.Canvas(window, bg="WhiteSmoke", width=1920, height=1080)
    character_canvas.place(anchor="center", relx=.5, rely=.5)
    character = character_canvas.create_rectangle(x1, y1, x2, y2, outline="azure4", fill="grey20")

    # Назначение клавиш для функций передвижения
    window.bind("<Up>", move_up)
    window.bind_all('<KeyRelease>', key_released)
    window.bind_all('<KeyPress>', key_pressed)


def create_platform(x, y, width, height):
    # Создание платформ в character_canvas
    platform = character_canvas.create_rectangle(x, y, x + width, y + height, fill="black")
    platforms.append(platform)


def create_spike(x, y, width, height):
    spike = character_canvas.create_rectangle(x, y, x + width, y + height, fill="red")
    spikes.append(spike)


def create_key(x, y, width, height):
    key = character_canvas.create_rectangle(x, y, x + width, y + height, fill="gold")
    keys.append(key)


def check_keys(required_keys):
    return k == required_keys


def create_exito(x, y, width, height):
    exito = character_canvas.create_rectangle(x, y, x + width, y + height, fill="blue")
    exits.append(exito)


def restart_level():
    global character_canvas, character, k, exits, spikes, keys, exito, move_running, gravity_running, deaths

    # Удаление существующих объектов с холста
    character_canvas.delete(character)
    for platform in platforms:
        character_canvas.delete(platform)
    for spike in spikes:
        character_canvas.delete(spike)
    for key in keys:
        character_canvas.delete(key)
    for exito in exits:
        character_canvas.delete(exito)

    # Обнуление списков и переменных
    platforms.clear()
    exits.clear()
    spikes.clear()
    keys.clear()
    k = 0
    deaths += 1

    # Создание персонажа на начальной позиции
    create_character(800, 800, 840, 840)

    # Вызов функции для создания уровня
    if v == 1:
        level_1()
    elif v == 2:
        level_2()
    elif v == 3:
        level_3()
    elif v == 4:
        level_final()

    move_running = True
    gravity_running = True


def pause_menu():
    global pause, pause_text, btn_continue, btn_settings, btn_exit

    def music():
        if music_playing.get() == 1:
            winsound.PlaySound(None, winsound.SND_PURGE)
            music_playing.set(False)
            btn_music.configure(text='Включить музыку')
        else:
            winsound.PlaySound('music/berlin.wav',
                               winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
            music_playing.set(True)
            btn_music.configure(text='Выключить музыку')

    pause = tk.Canvas(bg="white", width=1920, height=1080)
    pause.place(x=0, y=0)

    pause_text = tk.Label(window, text="ПАУЗА", font=btn_font)
    pause_text.place(anchor="center", relx=.5, rely=.225, relheight=.2, relwidth=.35)

    btn_continue = tk.Button(window, text="Продолжить", command=resume_play, font=btn_font)
    btn_continue.place(anchor="center", relx=.5, rely=.5, relheight=.1, relwidth=.25)

    btn_music = tk.Button(window, command=music, font=btn_font)
    btn_music.place(anchor="center", relx=.5, rely=.61, relheight=.1, relwidth=.25)

    btn_exit = tk.Button(window, text="Выйти в главное меню", command=restore_to_menu_from_game, font=btn_font)
    btn_exit.place(anchor="center", relx=.5, rely=.72, relheight=.1, relwidth=.25)


def resume_play():
    global pause, pause_text, btn_continue, btn_settings, btn_exit
    pause.place_forget()
    pause_text.place_forget()
    btn_continue.place_forget()
    btn_settings.place_forget()
    btn_exit.place_forget()


def next_level():
    global v
    if v == 1:
        level_2()
        v += 1
    elif v == 2:
        level_3()
        v += 1
    elif v == 3:
        level_final()
        v += 1


def level_1():
    clear_window()
    create_character(800, 800, 840, 840)
    req_keys = 1

    btn_pause = tk.Button(window, text="II", command=pause_menu, font=btn_font)
    btn_pause.place(anchor="center", relx=.026, rely=.046, relwidth=.03125, relheight=.05)

    btn_restart = tk.Button(window, text="R", command=restart_level, font=btn_font)
    btn_restart.place(anchor="center", relx=.061, rely=.046, relwidth=.03125, relheight=.05)

    create_platform(0, 1000, 2000, 100) #ground
    create_platform(100, 850, 200, 20)
    create_platform(400, 700, 500, 20)
    create_platform(900, 800, 300, 20)
    create_platform(1200, 700, 500, 20)
    create_platform(900, 700, 20, 100)
    create_platform(1180, 700, 20, 100)
    create_platform(1000, 650, 100, 20)
    create_platform(1500, 500, 300, 20)
    create_platform(1300, 350, 100, 20)
    create_platform(1400, 700, 150, 20)
    create_platform(900, 400, 400, 20)
    create_platform(1300, 370, 20, 50)
    create_platform(970, 250, 80, 20)
    create_platform(1100, 150, 1000, 20) #endline

    create_spike(100, 870, 200, 10)
    create_spike(550, 680, 100, 20)
    create_spike(920, 780, 260, 20)
    create_spike(1300, 500, 200, 20)
    create_spike(1780, 170, 20, 330)
    create_spike(1100, 170, 1000, 10)
    create_spike(900, 0, 20, 400)

    create_key(1200, 970, 40, 20)

    def exits():
        if check_keys(req_keys):
            create_exito(1900, 850, 200, 100)
        else:
            window.after(10, exits)
    exits()

    global move_running, gravity_running
    if not move_running:
        move()
        move_running = True
    if not gravity_running:
        apply_gravity()
        gravity_running = True


def clear_level():
    global platforms, exits, spikes, keys
    clear_window()
    platforms = []
    exits = []
    spikes = []
    keys = []
    create_character(800, 800, 840, 840)

    btn_pause = tk.Button(window, text="II", command=pause_menu, font=btn_font)
    btn_pause.place(anchor="center", relx=.026, rely=.046, relwidth=.03125, relheight=.05)

    btn_restart = tk.Button(window, text="R", command=restart_level, font=btn_font)
    btn_restart.place(anchor="center", relx=.061, rely=.046, relwidth=.03125, relheight=.05)


def level_2():
    clear_level()
    create_platform(100, 900, 200, 20)
    create_exito(1700, 900, 80, 120)


def level_3():
    clear_level()
    create_platform(1000, 900, 200, 20)

    create_exito(1500, 900, 200, 100)


def level_final():
    global time_start
    clear_level()
    all_time = str(round(time.time() - time_start))

    final_message = tk.Label(text='ggwp', font=btn_font)
    final_message.place(anchor='center', relx=.5, rely=.4)

    death = tk.Label(text='Смертей/Перезапусков:', font=btn_font)
    death.place(anchor='center', relx=.3, rely=.5)
    death_count = tk.Label(text=f"{deaths}", font=btn_font)
    death_count.place(anchor='center', relx=.3, rely=.55)

    time_spent = tk.Label(text='Времени затрачено:', font=btn_font)
    time_spent.place(anchor='center', relx=.7, rely=.5)
    timer = tk.Label(text=f"{all_time}" + " секунд", font=btn_font)
    timer.place(anchor='center', relx=.7, rely=.55)


window = tk.Tk()
window.title('2D-Platformer')
window.attributes('-fullscreen', True)
btn_font = font.Font(font=('Arial', 22))

winsound.PlaySound('music/berlin.wav', winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
music_playing = BooleanVar()
music_playing.set(True)

main_menu()
window.mainloop()