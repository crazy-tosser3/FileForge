import cv2
import soundfile as sf
from moviepy.editor import *
import os
from PIL import Image
import aspose.words as aw
from tkinter.messagebox import *

def Image_convert(path, save_dir, ImageSize, ImageExt):
    """Функция для конвертации изображения в указанный формат и размер."""
    export_path = os.path.join(f"{save_dir}", f"{ImageExt}")
    try:
        # Чтение изображения и его конвертация с использованием OpenCV
        img = cv2.imread(path)
        image = cv2.resize(img, ImageSize)
        cv2.imwrite(export_path, image)
    except Exception:
        # В случае ошибки, использует PIL для выполнения операции
        with Image.open(path) as img:
            img = img.resize(ImageSize)
            img.save((export_path))
    finally:   
        # Выводит путь сохраненного изображения
        print(f"Изображение сохранено по пути: {export_path}")

def Video_convert(video_path, VideoEXT, save_dir):
    """Функция для конвертации видео в указанный формат."""
    try:
        # Проверка формата и выполнение конвертации
        if VideoEXT != 'gif': 
            video = VideoFileClip(video_path)
            video.write_videofile(os.path.join(save_dir, f"{VideoEXT}"), codec='libx264')
        else:
            clip = (VideoFileClip(video_path).subclip(3, 7).resize(0.5))
            clip.write_gif(os.path.join(save_dir, f"{os.path.splitext(os.path.basename(video_path))[0]}.{VideoEXT}"))

        print("Конвертация завершена успешно!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        showerror(title="Ошибка!",message=e)

def Audio_convert(AudioEXT ,file_path, save_dir):
    """Функция для конвертации аудио в указанный формат."""
    try:
        # Чтение аудиофайла и его конвертация
        audio_data, samplerate = sf.read(file_path)
        output_path = os.path.join(save_dir, f"{AudioEXT}")
        sf.write(output_path, audio_data, samplerate)
        print(f"Аудиофайл сохранен по пути: {output_path}")
    except Exception as e:
        print(f"Произошла ошибка при конвертации аудио: {e}")
        showerror(title="Ошибка!",message=e)

def Document_convert(DocumentEXT,file_path, save_dir):
    """Функция для конвертации документа в указанный формат."""
    try:
        # Загрузка и конвертация документа
        doc = aw.Document(file_path)
        output_path = os.path.join(save_dir, f"{DocumentEXT}")
        doc.save(output_path)
        print(f"Документ сохранен по пути: {output_path}")
    except Exception as e:
        showerror(title="Ошибка!",message=e)
        print(f"Произошла ошибка при конвертации документа: {e}")

def CONVERT(KEY, file_name, file_format, image_size_w, image_size_h, export_dir, file_path):
    """Основная функция для управления конвертацией файлов."""
    
    # Класс для хранения параметров файлов для конвертации
    class FileParams:
        def __init__(self):
            self.file_name = file_name
            self.file_format = file_format
            self.image_size_w = image_size_w
            self.image_size_h = image_size_h

        def EXT(self):
            return f"{self.file_name}.{self.file_format}"
        
        def IM_SIZE(self):
            return (self.image_size_w, self.image_size_h)

    PARAMS = FileParams()

    if PARAMS.EXT() and PARAMS.IM_SIZE() is not None:
        
        match KEY:
            case "Image":
                """Конвертация Фото"""
                showinfo(title="Ожидайте!",message="Ожидайте, как только ваш файл будет готов, вы получите подобное уведомление!")
                Image_convert(path=file_path, save_dir=export_dir,ImageSize=PARAMS.IM_SIZE(), ImageExt=PARAMS.EXT())
                showinfo(title="Успех!",message=f"Ваш файл успешно конвертирован.\n {export_dir}")  
            case "Video":
                """Конвертация Видео"""
                showinfo(title="Ожидайте!",message="Ожидайте, как только ваш файл будет готов, вы получите подобное уведомление!")
                Video_convert(video_path=file_path, VideoEXT=PARAMS.EXT(), save_dir=export_dir) 
                showinfo(title="Успех!",message=f"Ваш файл успешно конвертирован.\n {export_dir}")  
            case "Audio":
                """Конвертация Аудио"""
                showinfo(title="Ожидайте!",message="Ожидайте, как только ваш файл будет готов, вы получите подобное уведомление!")
                Audio_convert(AudioEXT=PARAMS.EXT(), file_path=file_path, save_dir=export_dir)        
                showinfo(title="Успех!",message=f"Ваш файл успешно конвертирован.\n {export_dir}")  
            case "Document":
                """Конвертация Документов"""
                showinfo(title="Ожидайте!",message="Ожидайте, как только ваш файл будет готов, вы получите подобное уведомление!")
                Document_convert(DocumentEXT=PARAMS.EXT(), file_path=file_path, save_dir=export_dir)
                showinfo(title="Успех!",message=f"Ваш файл успешно конвертирован.\n {export_dir}")  