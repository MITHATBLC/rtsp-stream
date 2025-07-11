from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSystemTrayIcon
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from gl_widget import GlWidget

class CameraWindow(QWidget):
	def __init__(self, user, password, ip, port, stream_path):
		super().__init__()
		self.tray_icon = QSystemTrayIcon(self)
		self.tray_icon.setIcon(QIcon("icon_path/tray_icon.png")) #add your icon for toolbar
		self.tray_icon.show()
		self._is_fullscreen = False
		
		self.setWindowTitle("Camera Stream")
		self.setWindowIcon(QIcon("icon_path/window_icon.png")) #add your icon for window
		
		#gl_widget
		self.label = GlWidget(user, password, ip, port, stream_path)
		
		#close button
		self.close_btn = QPushButton()
		self.close_btn.setFixedSize(70, 70)
		self.close_btn.setIcon(QIcon("icons/close.png"))
		self.close_btn.setIconSize(QSize(50,50))
		self.close_btn.clicked.connect(self.close)
		#self.close_btn.setStyleSheet("border: none;")
		
		#zoom in button
		self.zoomIn_btn = QPushButton()
		self.zoomIn_btn.setFixedSize(70, 70)
		self.zoomIn_btn.setIcon(QIcon("icons/plus.png"))
		self.zoomIn_btn.setIconSize(QSize(50,50))
		self.zoomIn_btn.clicked.connect(self.label.zoom_in)
		
		#zoom out button
		self.zoomOut_btn = QPushButton()
		self.zoomOut_btn.setFixedSize(70, 70)
		self.zoomOut_btn.setIcon(QIcon("icons/minus.png"))
		self.zoomOut_btn.setIconSize(QSize(50,50))
		self.zoomOut_btn.clicked.connect(self.label.zoom_out)
		
		#full screen 
		self.fullScreen_btn = QPushButton()
		self.fullScreen_btn.setFixedSize(70, 70)
		self.fullScreen_btn.setIcon(QIcon("icons/full.png"))
		self.fullScreen_btn.setIconSize(QSize(50,50))
		self.fullScreen_btn.clicked.connect(self.fullScreen)
		
		#preset layout for buttons
		button_layout = QVBoxLayout()
		button_layout.addWidget(self.close_btn)
		button_layout.addWidget(self.zoomIn_btn)
		button_layout.addWidget(self.zoomOut_btn)
		button_layout.addWidget(self.fullScreen_btn)
		button_layout.addStretch()
		button_layout.addSpacing(10)
		button_layout.setContentsMargins(0,0,0,0)
		
		#main layout
		main_layout = QHBoxLayout()
		main_layout.addWidget(self.label)
		main_layout.addLayout(button_layout)
		main_layout.addSpacing(0)
		main_layout.setContentsMargins(0,0,0,0)
		
		self.setLayout(main_layout)
		
	def closeEvent(self, event):
		self.label.worker.stop()
		event.accept()
		
	def fullScreen(self):
		if self._is_fullscreen:
			self.showNormal()
			self._is_fullscreen = False
		else:
			self.showFullScreen()
			self._is_fullscreen = True
