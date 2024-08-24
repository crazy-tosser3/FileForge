import dearpygui.dearpygui as dpg
from tkinter import filedialog
from tkinter.messagebox import showinfo, showwarning
from func import *
import json

class GraphicalUserInterface:
    def __init__(self, File_img, Save_img, w_save, h_save, w_file, h_file, types, formats, settings, export_dir, file_path):
        # Инициализация атрибутов класса с параметрами интерфейса
        self.File_img = File_img  # Texture for the file picker button
        self.Save_img = Save_img  # Texture for the save path button
        self.File_w = w_file  # Width of the file picker button
        self.File_h = h_file  # Height of the file picker button
        self.Save_w = w_save  # Width of the save path button
        self.Save_h = h_save  # Height of the save path button
        self.file_type = types  # List of file types
        self.formats = formats  # Supported formats for each file type
        self.setting = settings  # Loaded settings
        self.Save_path = export_dir  # Save directory path
        self.File_path = file_path  # File path to be converted

    def file_picker(self):
        """Open a dialog to select a file and update the displayed path"""
        self.File_path = filedialog.askopenfilename(title="Choose File!")
        dpg.configure_item("File path", default_value=f"{self.File_path}")  # Update the file path in the UI
        print(self.File_path)
        return self.File_path

    def load_file_path(self):
        """Load the saved file path from settings"""
        if "export_dir" in self.setting:
            self.Save_path = self.setting["export_dir"]  # Get the save directory from settings
            dpg.configure_item("Save path", default_value=f"{self.setting['export_dir']}")  # Update the save path in the UI
            return self.Save_path

    def export_pth_picker(self):
        """Open a dialog to select a save directory and update the displayed path"""
        self.Save_path = filedialog.askdirectory(title="Choose Directory!")
        print(self.Save_path)            

        self.setting["export_dir"] = self.Save_path
        with open(os.path.join("JSON","Setting.json"), 'w') as f:
            json.dump(self.setting, f, indent=4)

        dpg.configure_item("Save path", default_value=f"{self.Save_path}")  # Update the save directory path in the UI

    def switch_combo(self):
        """Update the combo box items based on the selected file type"""
        self.file_type = dpg.get_value("parametr")  # Get the current selected file type
        dpg.configure_item("format", items=self.formats[self.file_type])  # Update the available formats in the combo box
        dpg.configure_item("name", hint=f"{self.file_type} file name")  # Update the file name hint

    def menu_bar(self):
        """Create the menu bar with file path selection and file type selection"""
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                with dpg.group(horizontal=False):
                    dpg.add_text("Fill in all fields!")
                    with dpg.group(horizontal=True):
                        # Input field and button for selecting save directory
                        dpg.add_input_text(hint="Save path", readonly=True, width=150, tag="Save path")
                        dpg.add_image_button(texture_tag=self.Save_img, width=self.Save_w, height=self.Save_h, callback=lambda: self.export_pth_picker())
                
                    with dpg.group(horizontal=True):
                        # Input field and button for selecting the file to convert
                        dpg.add_input_text(hint="File path", readonly=True, width=150, tag="File path")
                        dpg.add_image_button(texture_tag=self.File_img, width=self.File_w, height=self.File_h, callback=lambda: self.file_picker())
                
            with dpg.menu(label="File Type"):
                with dpg.group(height=False):
                    dpg.add_text("Choose file type!")
                    dpg.add_combo(items=self.file_type, default_value="Image", tag="parametr", callback=lambda: self.switch_combo())
        
    def any_gui_ellement(self):
        """Create additional GUI elements for file parameters and actions"""
        with dpg.group(horizontal=False):
            with dpg.group(horizontal=True):
                # Input field for file name and combo box for selecting file format
                dpg.add_input_text(hint="File name", width=180, tag="name")
                dpg.add_combo(items=self.formats["Image"], width=175, tag="format", default_value="Choose format")

            with dpg.group(horizontal=True):
                # Input fields for entering image width and height
                dpg.add_input_int(default_value=1024, width=180, tag="width")
                dpg.add_input_int(default_value=1024, width=175, tag="height")
        
            # Buttons for converting the file and exiting the application
            dpg.add_button(label="Convert", width=380, callback=lambda:self.convert())
            dpg.add_button(label="Quit", width=380, callback=lambda: dpg.destroy_context())
    
    def convert(self):
        if self.File_path is None:
            self.file_picker()
        
        file_name = dpg.get_value("name")
        file_format = dpg.get_value("format")
        ImageWidth = dpg.get_value("width")
        ImageHeight = dpg.get_value("height")
        KEY = dpg.get_value("parametr")

        CONVERT(
            KEY=KEY , file_name=file_name , file_format=file_format,
            image_size_w=ImageWidth , image_size_h=ImageHeight,
            export_dir= self.Save_path , file_path=self.File_path)