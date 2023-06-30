from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.camera import Camera
from kivy.logger import Logger
from PIL import Image
import csv
from kivy.utils import platform
from kivy.uix.label import Label
from jnius import autoclass
from datetime import datetime
import time
import logging





if platform == 'android':
    from android.permissions import request_permissions, Permission, check_permission

logging.basicConfig(level=logging.DEBUG)
logging.debug('Corretor: This message should go to the log file')
logging.info('Corretor: So should this')
logging.warning('Corretor: And this, too')

Builder.load_string('''
<Corretor>:
    orientation: 'vertical'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
    Button:
        text: 'Play'
        size_hint_y: None
        height: '48dp'
        on_press: root.toggle()
    Label:
        id: lbl
        text: 'Number of grades: 0'
        size_hint_y: None
        height: '48dp'
''')

def process_image(image_path):
    try:
        image = Image.open(image_path)
    except Exception as e:
        Logger.info(f"Corretor: An error occurred when processing the image: {e}")
        return {"grade": 0, "identified": False, "new": False}
    return {"grade": 0, "identified": True, "new": True}

def save_to_gallery(image_path):
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    MediaScannerConnection = autoclass('android.media.MediaScannerConnection')
    MediaScannerConnection.scanFile(PythonActivity.mActivity, 
                                    [image_path], 
                                    None,
                                    None)

class Corretor(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grades = []
        self.is_running = False
        # Request permissions on Android
        if platform == 'android':
            request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE], self.callback_permissions)
        Logger.info("Corretor: Starting the camera.")

    def callback_permissions(self, permissions, grants):
        Logger.info("Corretor: Checking permissions.")
        if all(grants):
            Logger.info("Corretor: Permissions granted. Trying to initialize camera.")
            Clock.schedule_once(self.init_camera, 0)  # Schedule camera initialization
        else:
            Logger.info("Corretor: Camera or Storage permission not granted")

    def toggle(self, *args):
        if not hasattr(self, 'camera'):
            return
        self.camera.play = not self.camera.play
        if self.camera.play:
            Clock.schedule_interval(self.capture, 0.5)
        else:
            Clock.unschedule(self.capture)
            self.save_grades()

    def capture(self, *args):
        Logger.info("Corretor: Capturing image.")
        if not hasattr(self, 'camera'):
            return
        timestr = time.strftime("%Y%m%d_%H%M%S")
        file_path = f"IMG_{timestr}.png"
        self.camera.export_to_png(file_path)
        save_to_gallery(file_path)
        result = process_image(file_path)
        if result["identified"] and result["new"]:
            self.grades.append(result["grade"])
        self.ids.lbl.text = f"Number of grades: {len(self.grades)}"
        return result

    def save_grades(self):
        try:
            Logger.info("Corretor: Saving grades.")
            Environment = autoclass('android.os.Environment')
            downloads_dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS).getAbsolutePath()
            file_path = os.path.join(downloads_dir, 'grades.csv')
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Grade - teste'])
                for grade in self.grades:
                    writer.writerow([grade])
            Logger.info("Corretor: Grades saved to CSV file.")
        except Exception as e:
            Logger.info(f"Corretor: An error occurred when saving the grades: {e}")

    def init_camera(self, dt):
        try:
            self.camera = Camera(resolution=(640, 480), play=False)
            self.add_widget(self.camera, index=0)
            Logger.info("Corretor: Camera initialized.")
        except Exception as e:
            Logger.error(f"Corretor: Failed to initialize the camera. Error: {str(e)}")

class MyApp(App):
    def build(self):
        return Corretor()

if __name__ == '__main__':
    MyApp().run()