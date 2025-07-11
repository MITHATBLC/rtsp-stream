from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import time

class CameraWorker(QThread):
    new_frame = pyqtSignal(object)

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.running = False

    def run(self):
        self.running = True
        cap = cv2.VideoCapture(self.url)
        last = time.time()

        while self.running:
            ret, frame = cap.read()
            if ret:
                self.new_frame.emit(frame)
                last = time.time()
            else:
                time.sleep(0.1)

            if time.time() - last > 5:
                print("Reconnection...")
                cap.release()
                cap = cv2.VideoCapture(self.url)
                last = time.time()

        cap.release()

    def stop(self):
        self.running = False
        self.wait()
