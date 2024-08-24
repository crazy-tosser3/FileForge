import dearpygui.dearpygui as dpg
import ctypes
import os
from gui import *
import json
from tkinter import Tk

# Устанавливает DPI Awareness для четкости отображения на экранах с высоким разрешением (только для Windows)
ctypes.windll.shcore.SetProcessDpiAwareness(True)

# Константы для настроек окна приложения
ICON_PATH = os.path.join("sprite", "icon.ico")  # Путь к иконке приложения
TITLE = str("FileForge")  # Название окна приложения
WIDTH = 400  # Ширина окна приложения
HEIGHT = 300  # Высота окна приложения

# Глобальные переменные для директорий сохранения и выбора файла
save_dir = None
file_dir = None

# Типы файлов, поддерживаемые приложением
file_type = ['Image', 'Video', 'Audio', 'Document']

def load_path(file_path):
    """Загрузить настройки из JSON файла по указанному пути"""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return {}

def load_formats(F_PATH):
    """Загрузить поддерживаемые форматы файлов из JSON файла"""
    with open(F_PATH, 'r') as file:
        return json.load(file)

setting_path = os.path.join("JSON","Setting.json")
format_path = os.path.join("JSON", "Format.json")

# Загрузка настроек и форматов из JSON файлов
setting = load_path(setting_path)
formats = load_formats(format_path)

# Создание контекста для Dear PyGui
dpg.create_context()

# Загрузка изображений, которые будут использоваться в интерфейсе
width_save, height_save, channels_save, data_save = dpg.load_image(os.path.join("sprite", "folder.png"))
width_pick, height_pick, channels_pick, data_pick = dpg.load_image(os.path.join("sprite", "pick.png"))

with dpg.texture_registry():
    """Регистрация текстур для использования в интерфейсе"""
    texture_id_save = dpg.add_static_texture(width_save, height_save, data_save)
    texture_id_pick = dpg.add_static_texture(width_pick, height_pick, data_pick)

# Создание пользовательского интерфейса с использованием загруженных текстур и настроек
user_interface = GraphicalUserInterface(
    File_img=texture_id_pick, Save_img=texture_id_save,
    w_save=width_save, h_save=height_save,
    w_file=width_pick, h_file=height_pick,
    types=file_type, settings=setting, formats=formats,
    export_dir=save_dir, file_path=file_dir)

with dpg.window(tag="main window"):
    # Добавление элементов интерфейса в главное окно
    user_interface.menu_bar()
    user_interface.any_gui_ellement()

# Загрузка пути к файлам (если необходимо)
user_interface.load_file_path()

# Создание окна приложения с заданными параметрами
dpg.create_viewport(
    title=TITLE, width=WIDTH, height=HEIGHT,
    resizable=False, vsync=True,
    small_icon=ICON_PATH, large_icon=ICON_PATH)

# Установка главного окна приложения
dpg.set_primary_window("main window", True)

# Настройка и запуск Dear PyGui
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()

# Уничтожение контекста при завершении работы приложения
dpg.destroy_context()