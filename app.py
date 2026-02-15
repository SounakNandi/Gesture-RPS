import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import QTimer, Qt, QSize
from PyQt6.QtGui import QImage, QPixmap, QFont, QColor
from logic import RPSGameLogic

class ModernRPSApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logic = RPSGameLogic()
        self.cap = cv2.VideoCapture(0)
        
        self.setWindowTitle("Gesture RPS")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f172a;
            }
            QLabel {
                color: #f8fafc;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        sidebar = QFrame()
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border-radius: 20px;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 30, 20, 30)
        sidebar_layout.setSpacing(20)

        logo = QLabel("GESTURE RPS")
        logo.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(logo)

        tagline = QLabel("POWERED BY PYQT6")
        tagline.setFont(QFont("Segoe UI", 10))
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tagline.setStyleSheet("color: #94a3b8;")
        sidebar_layout.addWidget(tagline)

        sidebar_layout.addSpacing(30)

        self.player_card = self.create_score_card("PLAYER", "#3b82f6")
        self.player_score_label = self.player_card.findChild(QLabel, "score_label")
        sidebar_layout.addWidget(self.player_card)

        self.ai_card = self.create_score_card("AI OVERLORD", "#ef4444")
        self.ai_score_label = self.ai_card.findChild(QLabel, "score_label")
        sidebar_layout.addWidget(self.ai_card)

        sidebar_layout.addStretch()

        self.start_btn = QPushButton("START ROUND")
        self.start_btn.setFixedHeight(60)
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3b82f6;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        self.start_btn.clicked.connect(self.start_round)
        sidebar_layout.addWidget(self.start_btn)

        self.reset_btn = QPushButton("Reset Game")
        self.reset_btn.setFixedHeight(40)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #94a3b8;
                border: 2px solid #334155;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #334155;
                color: white;
            }
        """)
        self.reset_btn.clicked.connect(self.reset_game)
        sidebar_layout.addWidget(self.reset_btn)

        viewport = QFrame()
        viewport.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border-radius: 20px;
            }
        """)
        viewport_layout = QVBoxLayout(viewport)
        viewport_layout.setContentsMargins(10, 10, 10, 10)

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("border-radius: 15px; background-color: #000000;")
        viewport_layout.addWidget(self.video_label)

        self.status_bar = QLabel("READY TO PLAY")
        self.status_bar.setFixedHeight(80)
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_bar.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.status_bar.setStyleSheet("""
            background-color: #2563eb;
            color: white;
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;
            margin-top: -20px;
        """)
        viewport_layout.addWidget(self.status_bar)

        self.move_label = QLabel("Show your move when the countdown hits zero!")
        self.move_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.move_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
        self.move_label.setStyleSheet("color: #94a3b8; margin: 10px;")
        viewport_layout.addWidget(self.move_label)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(viewport, 1)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def create_score_card(self, title, color):
        card = QFrame()
        card.setFixedHeight(140)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 15px;
            }}
        """)

        layout = QVBoxLayout(card)
        name = QLabel(title)
        name.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name)

        score = QLabel("0")
        score.setObjectName("score_label")
        score.setFont(QFont("Segoe UI", 48, QFont.Weight.Bold))
        score.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(score)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 5)
        card.setGraphicsEffect(shadow)

        return card

    def start_round(self):
        self.logic.start_round()

    def reset_game(self):
        self.logic.reset_game()
        self.update_ui("", 0)

    def update_ui(self, status, countdown):
        self.player_score_label.setText(str(self.logic.player_score))
        self.ai_score_label.setText(str(self.logic.ai_score))

        if self.logic.is_counting_down:
            self.status_bar.setText(str(countdown))
            self.status_bar.setStyleSheet("background-color: #f59e0b; color: white; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px; margin-top: -20px;")
            self.move_label.setText("PREPARE YOUR MOVE...")
        else:
            self.status_bar.setText(status.upper() if status else "READY TO PLAY")
            
            color = "#2563eb" # Default blue
            if "YOU WIN" in status.upper(): color = "#10b981" # Green
            if "AI WINS" in status.upper(): color = "#ef4444" # Red
            if "TIE" in status.upper(): color = "#0ea5e9" # Light blue
            
            self.status_bar.setStyleSheet(f"background-color: {color}; color: white; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px; margin-top: -20px;")
            
            if self.logic.player_move:
                self.move_label.setText(f"YOU: {self.logic.player_move.upper()}  |  AI: {self.logic.ai_move.upper()}")
            else:
                self.move_label.setText("Show your move when the countdown hits zero!")

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame, status, countdown = self.logic.process_frame(frame)
            
            # BGR to RGB
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            
            # Scale to fit
            label_w = self.video_label.width()
            label_h = self.video_label.height()
            if label_w > 0 and label_h > 0:
                pixmap = QPixmap.fromImage(qt_image).scaled(label_w, label_h, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                self.video_label.setPixmap(pixmap)
            
            self.update_ui(status, countdown)

    def closeEvent(self, event):
        self.cap.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernRPSApp()
    window.show()
    sys.exit(app.exec())
