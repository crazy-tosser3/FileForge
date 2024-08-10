import cv2
import soundfile as sf
from moviepy.editor import VideoFileClip
import os
import dearpygui.dearpygui as dpg
from PIL import Image

def Image_convert(path,save_dir,image_name,image_format,width,height):
    try:
        """Функция для конвертации изображения"""
        class ImageParam:
            """Класс с параметрами изображения"""
            def __init__(self):
                self.width = width
                self.height = height
                self.format = image_format
                self.im_label = image_name

            def size(self) -> tuple:
                """Функция получения кортежа с размером"""
                return (self.width, self.height)
            
            def label(self) -> str:
                """Функция для палучения имени изображения"""
                return os.path.join(f"{save_dir}", f"{self.im_label}.{self.format}")
            
            def extension(self) -> str:
                """Функция для получения расширения файла"""
                return self.format

        parameters = ImageParam()    
        
        img =  cv2.imread(path)
        image = cv2.resize(img, parameters.size())
        cv2.imwrite(parameters.label(),image)
    except Exception:
        with Image.open(path) as img:
            img = img.resize(parameters.size())
            img.save(parameters.label())

    finally:   
        print(parameters.label())


def Video_convert(video_path,name,save_dir,format):
    """Обрабатывает конвертацию видео в указанный формат."""
    try:
        class VideoParam:
            def __init__(self):
                self.video = video_path
                self.name = name
                self.format = format
                self.save = save_dir

            def label(self) -> str:
                return os.path.join(self.save, f"{self.name}.{self.format}")
            
            def videos(self):
                return self.video
        params = VideoParam()

        video = VideoFileClip(params.videos())
        video.write_videofile(params.label(), codec='libx264')

        print("Конвертация завершена успешно!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def Audio_convert(name, audio_format, file_path, save_dir):
    """Обрабатывает конвертацию аудио в указанный формат."""

    class AudioParam():
        def __init__(self):
            self.name = name
            self.format = audio_format 
            self.save = save_dir
            self.file = file_path
        
        def extension(self) -> str:
            return os.path.join(self.save,f"{self.name}.{self.format}")
        
        def file_pic(self) -> str:
            return self.file
        
    params = AudioParam()
    audio_data, samplerate = sf.read(params.file_pic())
    sf.write(params.extension(), audio_data, samplerate)
