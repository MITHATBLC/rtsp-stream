from PyQt5.QtWidgets import QApplication
from camera_window import CameraWindow
import sys

if sys.platform == 'win32':
    import ctypes
    myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    user = #"username"
    password = #"password"
    ip = #"ip.adress.of.camera"
    port = #stream port of camera
    stream_path = #stream path

    win = CameraWindow(user, password, ip, port, stream_path)
    win.show()
    sys.exit(app.exec_())
