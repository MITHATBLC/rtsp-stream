from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt, QPoint
from camera_stream_worker import CameraWorker
import cv2

class GlWidget(QWidget):
    def __init__(self, user, password, ip, port, stream_path, parent=None):
        super().__init__(parent)
        self.setFixedSize(720, 480)
        self._image = None
        self._zoom = 1.0
        self._initial_zoom = 1.0
        self._offset = QPoint(0, 0)
        self._dragging = False
        self._last_pos = QPoint()

        url = f"rtsp://{user}:{password}@{ip}:{port}/{stream_path}"
        self.worker = CameraWorker(url)
        self.worker.new_frame.connect(self.display_frame)
        self.worker.start()

    def display_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.set_image(img)

    #def close(self):
        #self.worker.stop()
        #super().close()

    def set_image(self, image: QImage):
        self._image = QPixmap.fromImage(image)
        if self._image and self._initial_zoom == 1.0:
            w_ratio = self.width() / self._image.width()
            h_ratio = self.height() / self._image.height()
            self._initial_zoom = min(w_ratio, h_ratio) * 1.065
            self._zoom = self._initial_zoom
            self._offset = QPoint(0, 0)
        self.update()

    def zoom_in(self):
        self._zoom = min(5.0, self._zoom * 1.1)
        self._constrain_offset()
        self.update()

    def zoom_out(self):
        self._zoom = max(self._initial_zoom, self._zoom / 1.1)
        self._constrain_offset()
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self._dragging:
            delta = event.pos() - self._last_pos
            self._offset += delta
            self._last_pos = event.pos()
            self._constrain_offset()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = False

    def _constrain_offset(self):
        if not self._image:
            return
        scaled_width = self.width() * self._zoom
        scaled_height = self.height() * self._zoom
        max_x = max(0, (scaled_width - self.width()) / 2)
        max_y = max(0, (scaled_height - self.height()) / 2)
        self._offset.setX(int(max(-max_x, min(self._offset.x(), max_x))))
        self._offset.setY(int(max(-max_y, min(self._offset.y(), max_y))))

    def paintEvent(self, event):
        if self._image:
            painter = QPainter(self)
            painter.fillRect(self.rect(), Qt.black)
            scaled = self._image.scaled(
                self.size() * self._zoom,
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation
            )
            top_left_x = int(((self.width() - scaled.width()) / 2 + self._offset.x()) * 1.1)
            top_left_y = int(((self.height() - scaled.height()) / 2 + self._offset.y()) * 1.1)
            painter.drawPixmap(top_left_x, top_left_y, scaled)
        else:
            super().paintEvent(event)
