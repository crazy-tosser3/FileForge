import dearpygui.dearpygui as dpg
import os
from func import *
import json
from tkinter import filedialog
from tkinter.messagebox import showinfo, showwarning

# Константы и глобальные переменные
PATH = "Setting.json"
save_dir = None
file_dir = None
file_type = ["Image", "Video", "Audio"]
formats = {
    "Image": ["png", "jpg", "jpeg","tiff",'tif',"bmp","jpe","ras","webp"],
    "Video": ['mp4', 'mov', 'mkv', 'flv', 'avi', 'webm', 'mpg'],
    "Audio": ['mp3', 'flac', 'wav', 'aiff', 'ogg', 'paf', 'sd2', 'mve', 'caf']
}

def convert(param):
    """Конвертировать файл на основе выбранных параметров"""
    global save_dir, file_dir
    formate = dpg.get_value("ch")
    name = dpg.get_value("name")
    width = dpg.get_value("w")
    height = dpg.get_value("h")
    
    print(f"""
    1.метка: {name} ({type(name)})
    2.формат: {formate} ({type(formate)})
    3.ширина,высота: {(width, height)} ({type(width)}, {type(height)})
    4.параметр:{param} ({type(param)})
    """)

    if name and formate and width and height is not None:

        if file_dir is None:
            file_path()

        if param == "Image":
            showinfo("Info","Converting...\nPress Enter to continue!")
            Image_convert(
                path=file_dir, save_dir=save_dir,
                image_name=name, image_format=formate,
                width=width, height=height
            )
            showinfo("Info","Converting has been compleate\nPress Enter to continue!")
        elif param == "Video":
            showinfo("Info","Converting...\nPress Enter to continue!")
            Video_convert(
                video_path=file_dir, name=name,
                save_dir=save_dir, format=formate
            )
            showinfo("Info","Converting has been compleate\nPress Enter to continue!")
        elif param == "Audio":
            showinfo("Info","Converting...\nPress Enter to continue!")
            Audio_convert(
                name=name, audio_format=formate,
                file_path=file_dir, save_dir=save_dir
            )
            showinfo("Info","Converting has been compleate\nPress Enter to continue!")
    else:
        showwarning(title="Warning", message="Please, make sure all fields compleate!")

def save_path():
    """Выбрать и сохранить путь к директории"""
    global save_dir
    save_dir = filedialog.askdirectory()
    save_file_path(save_dir)
    dpg.configure_item("save_dir", default_value=save_dir)
    print(save_dir)
    return save_dir

def file_path():
    """Выбрать путь к файлу"""
    global file_dir
    file_dir = filedialog.askopenfilename()
    print(file_dir)
    dpg.configure_item("file", default_value=f"{file_dir}")
    return file_dir

def switch_combo(sender, app_data):
    """Обновить комбо-бокс на основе выбранного типа файла"""
    file_type = dpg.get_value(sender)
    dpg.configure_item("ch", items=formats[file_type])
    dpg.configure_item("name", hint=f"{file_type} file name")

def load_path(file_path):
    """Загрузить настройки из JSON файла"""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return {}

setting = load_path(PATH)

def save_file_path(file_path):
    """Сохранить путь к файлу в настройках"""
    if file_path is not None:
        setting["export_dir"] = file_path
        with open(PATH, 'w') as f:
            json.dump(setting, f, indent=4)

def load_file_path():
    """Загрузить сохраненный путь к файлу из настроек"""
    global save_dir
    if "export_dir" in setting:
        save_dir = setting["export_dir"]
        dpg.configure_item("save_dir", default_value=f"{setting['export_dir']}")
        return save_dir

# Настройка GUI
dpg.create_context()

# Загрузка иконок
width_save, height_save, channels_save, data_save = dpg.load_image(os.path.join('sprite', 'folder.png'))
width_pick, height_pick, channels_pick, data_pick = dpg.load_image(os.path.join("sprite", "pick.png"))

with dpg.texture_registry():
    """Регистрация текстур"""
    texture_id_save = dpg.add_static_texture(width_save, height_save, data_save)
    texture_id_pick = dpg.add_static_texture(width_pick, height_pick, data_pick)

with dpg.window(tag="conv_app"):
    """Главное окно GUI"""
    with dpg.menu_bar():
        """Верхнее меню"""
        with dpg.menu(label='File'):
            with dpg.group(horizontal=False):
                dpg.add_text("Choice dir/file!")
                with dpg.group(horizontal=True):
                    """Выбор директории сохранения"""
                    dpg.add_input_text(hint="Save dir", width=150, readonly=True, tag="save_dir")
                    dpg.add_image_button(texture_tag=texture_id_save, width=width_save, height=height_save, callback=save_path)
                with dpg.group(horizontal=True):
                    """Выбор файла"""
                    dpg.add_input_text(hint="File", width=150, readonly=True, tag="file")
                    dpg.add_image_button(texture_tag=texture_id_pick, width=width_pick, height=height_pick, callback=file_path)
        
        with dpg.menu(label="File type"):
            """Выбор типа файла"""
            with dpg.group(horizontal=False):
                dpg.add_text("Choice file type!")
                p = dpg.add_combo(items=file_type, default_value="Image", callback=switch_combo, tag="fff")
    
    with dpg.group(horizontal=False, tag='user_group'):
        """Группа взаимодействия с пользователем"""
        with dpg.group(horizontal=True):
            dpg.add_input_text(hint="Image file name", width=150, tab_input=False, no_spaces=True, tag="name")
            dpg.add_combo(items=formats["Image"], width=150, tag="ch", default_value="Choice format")
        
        with dpg.group(horizontal=True):
            dpg.add_input_int(default_value=1024, width=150, tag="w")
            dpg.add_input_int(default_value=1024, width=150, tag="h")
        
        dpg.add_button(label="Convert", width=308, callback=lambda: convert(dpg.get_value(p)))
        dpg.add_button(label="Quit", width=308, callback=lambda: dpg.destroy_context())
    
    # dpg.add_dummy(height=50)
    # state = dpg.add_checkbox(label="Автоматический путь", tag='stat', default_value=False)

# Инициализация
load_file_path()
dpg.create_viewport(title="Converter", width=345, height=100, resizable=False)
dpg.set_primary_window("conv_app", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()