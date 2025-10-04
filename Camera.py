import flet as ft
import cv2
import time
import base64
from threading import Thread
import os

class CameraStream:
    def __init__(self, url):
        self.cap = cv2.VideoCapture(url)
        self.running = True
        self.frame = None
        self.recording = False
        self.video_writer = None

    def start(self):
        def run():
            while self.running:
                ret, frame = self.cap.read()
                if ret:
                    self.frame = frame
                    if self.recording and self.video_writer:
                        self.video_writer.write(frame)
                time.sleep(0.03)
        Thread(target=run, daemon=True).start()

    def get_frame_base64(self):
        if self.frame is None:
            return None
        _, buffer = cv2.imencode('.jpg', self.frame)
        return base64.b64encode(buffer).decode('utf-8')

    def take_photo(self):
        if self.frame is not None:
            os.makedirs("ESP32_WROVER", exist_ok=True)
            filename = f"ESP32_WROVER/photo_{int(time.time())}.jpg"
            cv2.imwrite(filename, self.frame)
            return filename
        return None

    def start_recording(self):
        if self.frame is not None:
            os.makedirs("ESP32_WROVER", exist_ok=True)
            h, w = self.frame.shape[:2]
            filename = f"ESP32_WROVER/video_{int(time.time())}.mp4"
            self.video_writer = cv2.VideoWriter(
                filename, cv2.VideoWriter_fourcc(*'XVID'), 20, (w, h)
            )
            self.recording = True
            return filename
        return None

    def stop_recording(self):
        self.recording = False
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None

    def stop(self):
        self.running = False
        self.cap.release()
        self.stop_recording()
