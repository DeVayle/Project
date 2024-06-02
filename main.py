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
    bg = tk.Canvas(bg="#cfcfcf", width=1920, height=1080)
    bg.place(x=0, y=0)

    btn_back = tk.Button(bg="#cfcfcf", activebackground="#cfcfcf", text='Вернуться', command=restore_to_menu, font=text_font, borderwidth=0)
    btn_back.place(anchor="center", relx=.125, rely=.9, relheight=.1, relwidth=.2)

    you = "Ваш главный персонаж - серый квадрат"
    goal = "Основная цель игры - собрать все ключи на каждом уровне и успешно пройти все уровни, избегая опасности"
    you_lbl = tk.Label(bg="#cfcfcf", text=you, wraplength=575, justify="left", font=text_font)
    goal_lbl = tk.Label(bg="#cfcfcf", text=goal, wraplength=575, justify="left", font=text_font)
    you_lbl.place(anchor="n", relx=.2, rely=.35)
    goal_lbl.place(anchor="n", x=360, rely=.43)

    base_controls = "Игрок управляет персонажем с помощью клавиш стрелок:"
    base_controls_left = "Стрелка влево: персонаж движется влево"
    base_controls_right = "Стрелка вправо: персонаж движется вправо"
    base_controls_up = "Стрелка вверх: персонаж прыгает"
    bc_lbl = tk.Label(bg="#cfcfcf", text=base_controls, wraplength=550, justify="left", font=text_font)
    bcl_lbl = tk.Label(bg="#cfcfcf", text=base_controls_left, wraplength=550, justify="left", font=text_font)
    bcr_lbl = tk.Label(bg="#cfcfcf", text=base_controls_right, wraplength=550, justify="left", font=text_font)
    bcu_lbl = tk.Label(bg="#cfcfcf", text=base_controls_up, wraplength=550, justify="left", font=text_font)
    bc_lbl.place(anchor="n", relx=.5, rely=.35)
    bcl_lbl.place(anchor="n", x=924, rely=.46)
    bcr_lbl.place(anchor="n", x=924, rely=.57)
    bcu_lbl.place(anchor="n", x=912, rely=.68)

    base_mechanics = "Основные механики игры"
    key_mechanics = "Сбор ключей: Игрок должен собирать ключи, чтобы открыть доступ к следующим испытаниям"
    spike_mechanics = "Смерть о лаву: Если персонаж касается лавы, он погибает, и уровень начинается заново"
    level_mechanics = "Переход на новый уровень: После сбора всех ключей, игрок должен найти выход, чтобы перейти на следующий уровень"
    bm_lbl = tk.Label(bg="#cfcfcf", text=base_mechanics, wraplength=550, justify="left", font=text_font)
    km_lbl = tk.Label(bg="#cfcfcf", text=key_mechanics, wraplength=550, justify="left", font=text_font)
    sm_lbl = tk.Label(bg="#cfcfcf", text=spike_mechanics, wraplength=550, justify="left", font=text_font)
    lm_lbl = tk.Label(bg="#cfcfcf", text=level_mechanics, wraplength=550, justify="left", font=text_font)
    bm_lbl.place(anchor="n", relx=.8, rely=.35)
    km_lbl.place(anchor="n", x=1512, rely=.4)
    sm_lbl.place(anchor="n", x=1512, rely=.57)
    lm_lbl.place(anchor="n", x=1512, rely=.74)


def main_menu():
    background = tk.Canvas(width=1920, height=1080)
    background.place(x=0, y=0)

    def music():
        if music_playing.get() == 1:
            winsound.PlaySound(None, winsound.SND_PURGE)
            music_playing.set(False)
            music_button.configure(image=music_off_img)
        else:
            winsound.PlaySound('music/berlin.wav',
                               winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
            music_playing.set(True)
            music_button.configure(image=music_on_img)

    game_name = Canvas(width=1920, height=1080)
    game_name.place(anchor="center", relx=.5, rely=.5)
    game_name.create_image(960, 540, anchor='center', image=bg_img)
    game_name.create_image(500, 250, anchor='center', image=game_name_img)

    btn_play = tk.Button(command=level_1, image=play_img, borderwidth=0)
    btn_play.place(anchor="center", relx=.15, rely=.5, relheight=.1, relwidth=.2)

    btn_help = tk.Button(command=helper, image=rules_img, borderwidth=0)
    btn_help.place(anchor="center", relx=.15, rely=.61, relheight=.1, relwidth=.2)

    music_button = tk.Button(command=music, borderwidth=0)
    music_button.place(anchor="center", relx=.15, rely=.72, relheight=.1, relwidth=.2)

    if music_playing.get() == 1:
        music_button.configure(image=music_on_img)
    else:
        music_button.configure(image=music_off_img)

    btn_back = tk.Button(command=window.destroy, image=exit_img, borderwidth=0)
    btn_back.place(anchor="center", relx=.15, rely=.83, relheight=.1, relwidth=.2)


# Инициализация возможных описаний персонажа "В воздухе" и "В прыжке"
in_air = False
jumping = False
move_running = False
gravity_running = False


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
        if (ex1 <= x1 <= ex2 or ex1 <= x2 <= ex2) and (ey1 <= y1 <= ey2 or ey1 <= y2 <= ey2):
            next_level()


def create_character(x1, y1, x2, y2):
    global character_canvas, character
    character_canvas = tk.Canvas(bg="#cfcfcf", width=1920, height=1080)
    character_canvas.place(anchor="center", relx=.5, rely=.5)
    character = character_canvas.create_rectangle(x1, y1, x2, y2, outline="grey20", fill="grey20")

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

    num_tiles_x = width // 20
    num_tiles_y = height // 20

    # Создаем мозаику изображений внутри прямоугольника
    for i in range(num_tiles_x):
        for j in range(num_tiles_y):
            character_canvas.create_image(x + i*20, y + j*20, anchor='nw', image=lava_img)


def create_key(x, y):
    key = character_canvas.create_rectangle(x, y, x + 40, y + 20, fill="gold")
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
    create_character(400, 960, 440, 1000)

    # Вызов функции для создания уровня
    if v == 1:
        level_1()
    elif v == 2:
        level_2()
    elif v == 3:
        level_3()
    elif v == 4:
        level_4()
    elif v == 5:
        level_final()

    move_running = True
    gravity_running = True


def pause_menu():
    global pause, pause_text, btn_continue, btn_music, btn_exit, warning

    def music():
        if music_playing.get() == 1:
            winsound.PlaySound(None, winsound.SND_PURGE)
            music_playing.set(False)
            btn_music.configure(image=music2_off_img)
        else:
            winsound.PlaySound('music/berlin.wav',
                               winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
            music_playing.set(True)
            btn_music.configure(image=music2_on_img)

    pause = tk.Canvas(bg="#cfcfcf", width=1920, height=1080)
    pause.place(x=0, y=0)

    pause_text = tk.Label(image=pause_text_img, borderwidth=0)
    pause_text.place(anchor="center", relx=.5, rely=.225, relheight=.2, relwidth=.35)

    btn_continue = tk.Button(command=resume_play, image=resume_img, borderwidth=0)
    btn_continue.place(anchor="center", relx=.5, rely=.5, relheight=.1, relwidth=.25)

    btn_music = tk.Button(command=music, borderwidth=0)
    btn_music.place(anchor="center", relx=.5, rely=.61, relheight=.1, relwidth=.25)

    btn_exit = tk.Button(command=restore_to_menu_from_game, image=exit_to_menu_img, borderwidth=0)
    btn_exit.place(anchor="center", relx=.5, rely=.72, relheight=.1, relwidth=.25)

    if music_playing.get():
        btn_music.configure(image=music2_on_img)
    else:
        btn_music.configure(image=music2_off_img)

    warning = tk.Label(bg="#cfcfcf", text="(При выходе в главное меню накопленный прогресс будет сброшен)", font=btn_font)
    warning.place(anchor="center", relx=.5, rely=.78)

    window.unbind("<Up>")
    window.unbind_all('<KeyRelease>')
    window.unbind_all('<KeyPress>')


def resume_play():
    global pause, pause_text, btn_continue, btn_music, btn_exit, warning
    pause.place_forget()
    pause_text.place_forget()
    btn_continue.place_forget()
    btn_music.place_forget()
    btn_exit.place_forget()
    warning.place_forget()

    window.bind("<Up>", move_up)
    window.bind_all('<KeyRelease>', key_released)
    window.bind_all('<KeyPress>', key_pressed)


def next_level():
    global v
    if v == 1:
        level_2()
        v += 1
    elif v == 2:
        level_3()
        v += 1
    elif v == 3:
        level_4()
        v += 1
    elif v == 4:
        level_final()
        v += 1


def clear_level():
    global platforms, exits, spikes, keys, k
    clear_window()
    platforms = []
    exits = []
    spikes = []
    keys = []
    k = 0
    create_character(400, 960, 440, 1000)

    btn_pause = tk.Button(command=pause_menu, image=pause_bt_img, borderwidth=0)
    btn_pause.place(anchor="center", relx=.026, rely=.046, relwidth=.03125, relheight=.05)

    btn_restart = tk.Button(command=restart_level, image=restart_img, borderwidth=0)
    btn_restart.place(anchor="center", relx=.061, rely=.046, relwidth=.03125, relheight=.05)


def level_1():
    global time_start
    clear_window()
    create_character(400, 960, 440, 1000)
    time_start = time.time()

    btn_pause = tk.Button(command=pause_menu, image=pause_bt_img, borderwidth=0)
    btn_pause.place(anchor="center", relx=.026, rely=.046, relwidth=.03125, relheight=.05)

    btn_restart = tk.Button(command=restart_level, image=restart_img, borderwidth=0)
    btn_restart.place(anchor="center", relx=.061, rely=.046, relwidth=.03125, relheight=.05)

    create_platform(0, 1000, 2000, 100)  # spawn
    create_platform(1000, 850, 320, 20)
    create_platform(1400, 700, 450, 20)
    create_platform(1650, 500, 100, 20)
    create_platform(1550, 300, 100, 20)
    create_platform(1100, 350, 300, 20)
    create_platform(800, 550, 200, 20)
    create_platform(400, 750, 200, 20)  # key
    create_platform(0, 200, 1000, 20)  # end

    create_key(480, 720)
    req_keys1 = 1

    def exits():
        if check_keys(req_keys1):
            create_exito(50, 100, 60, 100)
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


def level_2():
    clear_level()

    create_platform(300, 1000, 200, 100)  # spawn
    create_platform(100, 850, 250, 20)
    create_platform(1570, 850, 250, 20)
    create_platform(350, 650, 250, 20)
    create_platform(1320, 650, 250, 20)
    create_platform(600, 450, 250, 20)
    create_platform(1070, 450, 250, 20)
    create_platform(850, 250, 220, 20)  # end
    create_platform(800, 750, 320, 20)  # key 1
    create_platform(280, 350, 150, 20)  # key 2
    create_platform(1490, 350, 150, 20)  # key 3

    create_spike(0, 1020, 2000, 100)

    create_key(940, 720)
    create_key(330, 320)
    create_key(1550, 320)
    req_keys2 = 3

    def exits():
        if check_keys(req_keys2):
            create_exito(930, 150, 60, 100)
        else:
            window.after(10, exits)
    exits()


def level_3():
    clear_level()

    create_platform(0, 1000, 2000, 100)  # ground
    create_platform(100, 850, 200, 20)
    create_platform(400, 700, 410, 20)
    create_platform(790, 720, 20, 80)
    create_platform(1290, 720, 20, 80)
    create_platform(1290, 700, 500, 20)
    create_platform(1025, 700, 50, 20)
    create_platform(1500, 500, 300, 20)
    create_platform(1300, 350, 100, 20)
    create_platform(1400, 700, 150, 20)
    create_platform(900, 400, 400, 20)
    create_platform(1300, 370, 20, 50)
    create_platform(970, 250, 80, 20)
    create_platform(100, 550, 200, 20)
    create_platform(400, 350, 150, 20)
    create_platform(650, 200, 150, 20)
    create_platform(1100, 150, 1000, 20)  # end

    create_spike(100, 870, 200, 20)
    create_spike(550, 680, 100, 20)
    create_spike(790, 780, 520, 20)
    create_spike(1780, 170, 20, 330)
    create_spike(1100, 170, 1000, 20)
    create_spike(900, 0, 20, 400)

    create_key(1850, 570)
    create_key(705, 170)
    req_keys3 = 2

    def exits():
        if check_keys(req_keys3):
            create_exito(1840, 50, 60, 100)
        else:
            window.after(10, exits)
    exits()


def level_4():
    clear_level()

    create_platform(300, 1000, 200, 100)  # spawn
    create_platform(700, 1000, 200, 20)
    create_platform(1100, 1000, 300, 20)
    create_platform(1450, 850, 200, 20)
    create_platform(1800, 950, 100, 20)  # key 1
    create_platform(1750, 700, 100, 20)
    create_platform(1400, 600, 200, 20)
    create_platform(1000, 600, 180, 20)
    create_platform(650, 600, 150, 20)
    create_platform(350, 600, 100, 20)
    create_platform(220, 620, 60, 20)
    create_platform(220, 760, 60, 20)
    create_platform(220, 900, 60, 20)
    create_platform(220, 1040, 60, 20)  # key 2
    create_platform(0, 500, 60, 20)
    create_platform(0, 350, 60, 20)
    create_platform(0, 200, 400, 20)  # end
    create_platform(550, 250, 150, 20)
    create_platform(900, 250, 120, 20)
    create_platform(1200, 250, 200, 20)
    create_platform(1800, 350, 200, 20)  # key 3
    create_platform(1550, 200, 200, 20)

    create_spike(300, 1030, 2000, 100)
    create_spike(0, 1060, 300, 50)
    create_spike(280, 480, 20, 1000)
    create_spike(280, 220, 20, 80)

    create_key(1830, 920)
    create_key(230, 1010)
    create_key(1830, 320)
    req_keys4 = 3

    def exits():
        if check_keys(req_keys4):
            create_exito(40, 100, 60, 100)
        else:
            window.after(10, exits)
    exits()


def level_final():
    global time_start
    clear_level()
    all_time = str(round(time.time() - time_start))

    final_message = tk.Label(bg="#cfcfcf", text='ggwp', font=btn_font)
    final_message.place(anchor='center', relx=.5, rely=.4)

    death = tk.Label(bg="#cfcfcf", text='Смертей/Перезапусков:', font=btn_font)
    death.place(anchor='center', relx=.3, rely=.5)
    death_count = tk.Label(bg="#cfcfcf", text=f"{deaths}", font=btn_font)
    death_count.place(anchor='center', relx=.3, rely=.55)

    time_spent = tk.Label(bg="#cfcfcf", text='Времени затрачено:', font=btn_font)
    time_spent.place(anchor='center', relx=.7, rely=.5)
    timer = tk.Label(bg="#cfcfcf", text=f"{all_time}" + " секунд", font=btn_font)
    timer.place(anchor='center', relx=.7, rely=.55)

    dead_end = tk.Button(bg="#cfcfcf", text="Перейти в Главное меню", command=restore_to_menu_from_game, font=btn_font)
    dead_end.place(anchor='center', relx=.5, rely=.65)

    create_platform(0, 1000, 2000, 100)


window = tk.Tk()
window.title('2D-Platformer')
window.configure(bg='#cfcfcf')
window.attributes('-fullscreen', True)
btn_font = font.Font(font=('Better VCR Regular', 12))
text_font = font.Font(font=('Better VCR Regular', 24))

# Изображения для игры:
game_name_img = ImageTk.PhotoImage(Image.open('textures/name.png'))
lava_img = ImageTk.PhotoImage(Image.open('textures/lava.png'))
key_img = ImageTk.PhotoImage(Image.open('textures/key.png'))
bg_img = ImageTk.PhotoImage(Image.open('textures/bg.png'))
play_img = ImageTk.PhotoImage(Image.open('textures/play.png'))
music_off_img = ImageTk.PhotoImage(Image.open('textures/music_off.png'))
music_on_img = ImageTk.PhotoImage(Image.open('textures/music_on.png'))
music2_off_img = ImageTk.PhotoImage(Image.open('textures/music2_off.png'))
music2_on_img = ImageTk.PhotoImage(Image.open('textures/music2_on.png'))
rules_img = ImageTk.PhotoImage(Image.open('textures/rules.png'))
exit_img = ImageTk.PhotoImage(Image.open('textures/exit.png'))
resume_img = ImageTk.PhotoImage(Image.open('textures/resume.png'))
exit_to_menu_img = ImageTk.PhotoImage(Image.open('textures/exit_to_menu.png'))
pause_text_img = ImageTk.PhotoImage(Image.open('textures/pause.png'))
restart_img = ImageTk.PhotoImage(Image.open('textures/restart.png'))
pause_bt_img = ImageTk.PhotoImage(Image.open('textures/pause_btn.png'))
levels_bg_img = ImageTk.PhotoImage(Image.open('textures/levels_bg.png'))

winsound.PlaySound('music/berlin.wav', winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
music_playing = BooleanVar()
music_playing.set(True)

main_menu()
window.mainloop()
