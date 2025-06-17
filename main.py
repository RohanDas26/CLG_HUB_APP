import sys
import json
import os
import random
import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QFileDialog, QInputDialog, QLabel, QMessageBox, QLineEdit, QSplashScreen,
    QMenu, QScrollArea, QCheckBox, QDialog, QGraphicsOpacityEffect
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl, QTimer, QPropertyAnimation
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor

STORAGE_PATH = os.path.join(os.getcwd(), "ClgBuddyFiles")
os.makedirs(STORAGE_PATH, exist_ok=True)

WEB_LINKS = {
    "Academics": "https://academics.klef.in/login",
    "ERP": "https://newerp.kluniversity.in/",
    "LMS": "https://bmp-lms.klh.edu.in/login/index.php?testsession=1014"
}

WELCOME_MESSAGES = [
    "What's on the agenda today?", "Ready to rule the day!", "Let's get things done 🔥",
    "Time to hustle 📚", "Another day, another victory!", "Focus mode: ON ✅"
]

QA_PAIRS = {
    "How to upload file?": "Go to the left panel, select subject and click Upload File.",
    "How to login ERP?": "Click ERP button on left.",
    "Where is subject folder?": "In the Subjects section you can create/select folders."
}

ROAST_LINES = [
    "Nee thalli ki cheppu tho kodatha",
    "Dengutha ni logic ni",
    "Neekenduku ra education",
    "Ni brain lo vacuum undi anta",
    "Puku gathi ledu, advice istunnavu",
    "Bokka ni work cheyyi ra",
    "Nee logic choosi lanja kodaka compiler ni rape chesav emo.",
    "Erri puka lo podichey thoughts tho code rasav enti ra bokka.",
    "Nee thalli pempaka kastalu telusthunnayi ra niku chadivinchadam tho.",
    "RCB gelichindani anukoni lanja la reels vestunnav ra munda.",
    "Nee brain open chesthe andulo lanja ni karra dantlo petti unnattu undi.",
    "Puka mida code rasina better output vastadi ra neeku kanna.",
    "Dengutha ani cheppina code ni kaadhu ra – ni ammagari asha lu kuda.",
    "Nee logic choosi Thanos kuda snap chesadu second time.",
    "Bokka kodaka, ni IQ choosthe loading ane word ki kooda bejaar vasthundi.",
    "Ni function run kakapote ok, kani ni existence kuda unnecessary ra.",
    "Ni ammagari chaduvu kosam boku debbalu kodithe correct avutav ra.",
    "Oka sari ni code chusi AI suicide chesindi ra lanjakodaka.",
    "Nee brain lo vacuum kaadhu ra – akkad erri puka memes circulate avutunnayi.",
    "Mundara ni face choosi chatbot kuda ‘error 404: purpose not found’ antundi.",
    "Nee presence tho GitHub repo kuda private ayipoyindi ra bokka."
]

def get_text_splash_pixmap():
    pixmap = QPixmap(500, 250)
    pixmap.fill(Qt.white)
    painter = QPainter(pixmap)
    font = QFont("Arial", 32, QFont.Bold)
    painter.setFont(font)
    painter.setPen(QColor("#1E90FF"))
    painter.drawText(pixmap.rect(), Qt.AlignCenter, "✨ CLG HUB ✨")
    painter.end()
    return pixmap

def show_splash(app):
    pixmap = get_text_splash_pixmap()
    splash = QSplashScreen(pixmap)
    splash.setWindowFlags(Qt.FramelessWindowHint | Qt.SplashScreen)
    splash.setMask(pixmap.mask())
    splash.show()
    QTimer.singleShot(1500, splash.close)

def fade_widget(widget):
    effect = QGraphicsOpacityEffect()
    widget.setGraphicsEffect(effect)
    anim = QPropertyAnimation(effect, b"opacity")
    anim.setDuration(300)
    anim.setStartValue(0)
    anim.setEndValue(1)
    anim.start()

class ChatWindow(QWidget):
    def __init__(self, dark_mode=False):
        super().__init__()
        self.setWindowTitle("AI Chat ✨")
        self.setGeometry(250, 120, 700, 700)
        self.dark_mode = dark_mode
        self.layout = QVBoxLayout()

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.chat_area = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_area.setLayout(self.chat_layout)
        self.scroll.setWidget(self.chat_area)
        self.layout.addWidget(self.scroll)

        self.show_welcome()

        sug_layout = QHBoxLayout()
        for q in QA_PAIRS.keys():
            b = QPushButton(q)
            b.clicked.connect(lambda _, txt=q: self.ask_question(txt))
            sug_layout.addWidget(b)
        self.layout.addLayout(sug_layout)

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Ask anything...")
        self.input_line.textChanged.connect(self.toggle_send)
        self.input_line.returnPressed.connect(self.handle_user_input)
        self.send_btn = QPushButton("➤")
        self.send_btn.clicked.connect(self.handle_user_input)
        self.send_btn.setEnabled(False)
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_line)
        input_layout.addWidget(self.send_btn)
        self.layout.addLayout(input_layout)
        self.setLayout(self.layout)

    def show_welcome(self):
        msg = random.choice(WELCOME_MESSAGES)
        label = QLabel(msg)
        label.setFont(QFont("Arial", 18))
        label.setAlignment(Qt.AlignCenter)
        self.chat_layout.addWidget(label)

    def toggle_send(self):
        self.send_btn.setEnabled(bool(self.input_line.text().strip()))

    def ask_question(self, q):
        self.input_line.setText(q)
        self.handle_user_input()

    def handle_user_input(self):
        question = self.input_line.text().strip()
        if not question: return
        self.add_bubble(question, user=True)
        self.input_line.clear()
        self.send_btn.setEnabled(False)
        response = QA_PAIRS.get(question, random.choice(ROAST_LINES))
        self.simulate_typing(response)

    def simulate_typing(self, reply):
        typing_label = QLabel("Bot is typing...")
        self.chat_layout.addWidget(typing_label)
        QTimer.singleShot(800, lambda: (typing_label.deleteLater(), self.add_bubble(reply, user=False)))

    def add_bubble(self, text, user):
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setMargin(10)
        bubble.setMaximumWidth(450)
        style = ("background-color: #1E90FF; color: white; border-radius: 10px;"
                 if user else "background-color: #E5E5EA; color: black; border-radius: 10px;")
        if self.dark_mode and not user:
            style = "background-color: #444; color: white; border-radius: 10px;"
        bubble.setStyleSheet(style)
        effect = QGraphicsOpacityEffect()
        bubble.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(400)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.start()
        align = Qt.AlignRight if user else Qt.AlignLeft
        wrapper = QHBoxLayout()
        if user:
            wrapper.addStretch()
        wrapper.addWidget(bubble)
        if not user:
            wrapper.addStretch()
        self.chat_layout.addLayout(wrapper)
        QTimer.singleShot(100, lambda: self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum()))

class SettingsDialog(QDialog):
    def __init__(self, parent, dark_mode):
        super().__init__(parent)
        self.setWindowTitle("Settings ⚙️")
        self.setGeometry(400, 200, 400, 200)
        self.dark_mode = dark_mode
        layout = QVBoxLayout()

        self.dark_toggle = QCheckBox("🌙 Enable Dark Mode")
        self.dark_toggle.setChecked(self.dark_mode)
        layout.addWidget(self.dark_toggle)

        about_label = QLabel("Clg Hub\nVersion 2.0\n")
        about_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(about_label)

        btn_save = QPushButton("Save")
        btn_save.clicked.connect(self.accept)
        layout.addWidget(btn_save)
        self.setLayout(layout)

class ClgBuddy(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KL Clg Hub ✨")
        self.setGeometry(150, 80, 1300, 750)
        self.dark_mode = False
        main_layout = QHBoxLayout()
        left_panel = QVBoxLayout()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://academics.klef.in/login"))

        for name, url in WEB_LINKS.items():
            btn = QPushButton(f"🌐 {name}")
            btn.setStyleSheet("QPushButton { background-color: #1E90FF; color: white; padding: 6px; border-radius: 5px; }")
            btn.clicked.connect(lambda _, u=url: self.browser.setUrl(QUrl(u)))
            left_panel.addWidget(btn)

        ai_btn = QPushButton("🤖 AI Chat")
        ai_btn.setStyleSheet("background-color: purple; color: white; padding: 6px; border-radius: 5px;")
        ai_btn.clicked.connect(self.open_chat)
        left_panel.addWidget(ai_btn)

        setting_btn = QPushButton("⚙️ Settings")
        setting_btn.clicked.connect(self.open_settings)
        left_panel.addWidget(setting_btn)

        self.folder_list = QListWidget()
        self.folder_list.setFixedWidth(250)
        self.folder_list.itemClicked.connect(self.display_files)
        self.folder_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.folder_list.customContextMenuRequested.connect(self.folder_context_menu)
        left_panel.addWidget(QLabel("📁 Subjects"))
        left_panel.addWidget(self.folder_list)

        btn_add_folder = QPushButton("➕ Add Folder")
        btn_add_folder.clicked.connect(self.add_folder)
        btn_upload = QPushButton("📄 Upload File")
        btn_upload.clicked.connect(self.upload_file)
        left_panel.addWidget(btn_add_folder)
        left_panel.addWidget(btn_upload)
        left_panel.addWidget(QLabel("🗂️ Files"))

        self.file_list = QListWidget()
        self.file_list.setFixedHeight(150)
        self.file_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_list.customContextMenuRequested.connect(self.file_context_menu)
        left_panel.addWidget(self.file_list)

        main_layout.addLayout(left_panel, 1)
        main_layout.addWidget(self.browser, 3)
        self.setLayout(main_layout)
        self.load_folders()

    def open_chat(self):
        self.chat_window = ChatWindow(self.dark_mode)
        self.chat_window.setWindowOpacity(0)
        self.chat_window.show()
        anim = QPropertyAnimation(self.chat_window, b"windowOpacity")
        anim.setDuration(600)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.start()

    def open_settings(self):
        dlg = SettingsDialog(self, self.dark_mode)
        if dlg.exec_():
            self.dark_mode = dlg.dark_toggle.isChecked()
            self.toggle_dark_mode()

    def toggle_dark_mode(self):
        if self.dark_mode:
            self.setStyleSheet("background-color: #222; color: white;")
        else:
            self.setStyleSheet("")

    def load_folders(self):
        self.folder_list.clear()
        for folder in os.listdir(STORAGE_PATH):
            if os.path.isdir(os.path.join(STORAGE_PATH, folder)):
                self.folder_list.addItem(folder)
        fade_widget(self.folder_list)

    def add_folder(self):
        name, ok = QInputDialog.getText(self, "New Subject", "Enter subject name:")
        if ok and name:
            path = os.path.join(STORAGE_PATH, name)
            if not os.path.exists(path):
                os.mkdir(path)
                self.load_folders()
            else:
                QMessageBox.information(self, "Exists", "Subject already exists.")

    def folder_context_menu(self, pos):
        item = self.folder_list.itemAt(pos)
        if not item: return
        menu = QMenu()
        rename_action = menu.addAction("✏️ Rename Folder")
        delete_action = menu.addAction("🗑️ Delete Folder")
        action = menu.exec_(self.folder_list.mapToGlobal(pos))
        if action == rename_action:
            new_name, ok = QInputDialog.getText(self, "Rename Folder", "Enter new name:")
            if ok and new_name:
                os.rename(os.path.join(STORAGE_PATH, item.text()), os.path.join(STORAGE_PATH, new_name))
                self.load_folders()
        elif action == delete_action:
            folder_path = os.path.join(STORAGE_PATH, item.text())
            for f in os.listdir(folder_path):
                os.remove(os.path.join(STORAGE_PATH, f))
            os.rmdir(folder_path)
            self.load_folders()
            self.file_list.clear()

    def upload_file(self):
        current = self.folder_list.currentItem()
        if not current:
            QMessageBox.warning(self, "No Subject", "Please select a subject.")
            return
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose File")
        if file_path:
            folder = current.text()
            topic, ok_topic = QInputDialog.getText(self, "Topic", "Enter topic name:")
            if not ok_topic or not topic:
                QMessageBox.warning(self, "Cancelled", "Upload cancelled.")
                return
            today = datetime.date.today().strftime("%Y-%m-%d")
            _, ext = os.path.splitext(file_path)
            new_filename = f"{folder}_{topic}_{today}{ext}"
            dest = os.path.join(STORAGE_PATH, folder, new_filename)
            with open(file_path, 'rb') as src, open(dest, 'wb') as dst:
                dst.write(src.read())
            self.display_files()

    def display_files(self):
        self.file_list.clear()
        current = self.folder_list.currentItem()
        if current:
            path = os.path.join(STORAGE_PATH, current.text())
            for f in os.listdir(path):
                self.file_list.addItem(f)
            fade_widget(self.file_list)

    def file_context_menu(self, pos):
        current_folder = self.folder_list.currentItem()
        item = self.file_list.itemAt(pos)
        if not current_folder or not item: return
        menu = QMenu()
        rename_action = menu.addAction("✏️ Rename File")
        delete_action = menu.addAction("🗑️ Delete File")
        action = menu.exec_(self.file_list.mapToGlobal(pos))
        file_path = os.path.join(STORAGE_PATH, current_folder.text(), item.text())
        if action == rename_action:
            new_name, ok = QInputDialog.getText(self, "Rename File", "Enter new name:")
            if ok and new_name:
                os.rename(file_path, os.path.join(STORAGE_PATH, current_folder.text(), new_name))
                self.display_files()
        elif action == delete_action:
            os.remove(file_path)
            self.display_files()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    show_splash(app)
    win = ClgBuddy()
    win.show()
    sys.exit(app.exec_()) 