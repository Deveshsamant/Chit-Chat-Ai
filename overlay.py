from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QWidget, QFrame, QHBoxLayout, QPushButton, QStackedLayout, QTextEdit, QDialog)
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QUrl, QSize
from PyQt6.QtGui import QFont, QDesktopServices, QPixmap, QPainter, QPainterPath, QCursor, QIcon
import os

class DeveloperPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(300, 470)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        # Container with gradient/dark bg
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: rgba(10, 10, 26, 250);
                border: 1px solid rgba(0, 229, 255, 50);
                border-radius: 20px;
            }
        """)
        layout.addWidget(container)
        
        cont_layout = QVBoxLayout()
        cont_layout.setContentsMargins(20, 30, 20, 30)
        cont_layout.setSpacing(15)
        container.setLayout(cont_layout)
        
        # Profile Image (Circular)
        img_label = QLabel()
        img_label.setFixedSize(120, 120)
        img_label.setStyleSheet("background: transparent; border: none;")
        
        # Load and mask image
        # Using absolute path for safety as requested
        photo_path = r"C:\Users\Abhay\Desktop\Chit_Chat\myphoto.jpg"
        pixmap = QPixmap(photo_path)
        
        if not pixmap.isNull():
             # Create circular mask
             rounded = QPixmap(120, 120)
             rounded.fill(Qt.GlobalColor.transparent)
             painter = QPainter(rounded)
             painter.setRenderHint(QPainter.RenderHint.Antialiasing)
             path = QPainterPath()
             path.addEllipse(0, 0, 120, 120)
             painter.setClipPath(path)
             # Scale properly
             painter.drawPixmap(0, 0, 120, 120, pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))
             painter.end()
             img_label.setPixmap(rounded)
             img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
             
             # Add a glowing border effect via another label or drawing (simplified here with simple style on parent if needed, but QPixmap handles visual)
        else:
            img_label.setText("No Image")
            img_label.setStyleSheet("color: white; border: 2px solid cyan; border-radius: 60px; padding: 10px;")
            
        # Center the image
        img_container = QHBoxLayout()
        img_container.addStretch()
        img_container.addWidget(img_label)
        img_container.addStretch()
        cont_layout.addLayout(img_container)
        
        # Name
        name_lbl = QLabel("Devesh Samant")
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_lbl.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        # Gradient text effect is hard in standard stylesheet, using solid cyan
        name_lbl.setStyleSheet("color: #00e5ff; background: transparent; border: none; margin-top: 10px;")
        cont_layout.addWidget(name_lbl)
        
        # Subtitle
        sub_lbl = QLabel("Space Explorer & Code Warrior")
        sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_lbl.setFont(QFont("Segoe UI", 10))
        sub_lbl.setStyleSheet("color: #a0a0a0; background: transparent; border: none; margin-bottom: 5px;")
        cont_layout.addWidget(sub_lbl)
        
        # Links
        links_layout = QVBoxLayout()
        links_layout.setSpacing(8)
        
        def make_link_btn(text, url, icon_name):
            btn = QPushButton(f"  {text}")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            
            # Load icon
            icon_path = fr"assets\icons\{icon_name}"
            # Check absolute path just in case
            if not os.path.exists(icon_path):
                 icon_path = os.path.join(os.getcwd(), "assets", "icons", icon_name)
            
            if os.path.exists(icon_path):
                btn.setIcon(QIcon(icon_path))
                btn.setIconSize(QSize(20, 20))
            
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 8px 15px;
                    color: #e0e0e0;
                    background-color: rgba(255, 255, 255, 5);
                    border-radius: 10px;
                    border: 1px solid rgba(255,255,255,10);
                    font-size: 13px;
                    font-family: 'Segoe UI';
                }
                QPushButton:hover {
                    background-color: rgba(0, 229, 255, 30);
                    color: #00e5ff;
                    border: 1px solid rgba(0, 229, 255, 100);
                }
            """)
            btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(url)))
            return btn
            
        links_layout.addWidget(make_link_btn("Instagram", "https://www.instagram.com/devesh.samant/", "instagram.png"))
        links_layout.addWidget(make_link_btn("X (Twitter)", "https://x.com/DeveshSama32978", "x.png"))
        links_layout.addWidget(make_link_btn("LinkedIn", "https://www.linkedin.com/in/devesh-samant-b78376258/", "linkedin.png"))
        links_layout.addWidget(make_link_btn("GitHub", "https://github.com/Deveshsamant", "github.png"))
        
        cont_layout.addLayout(links_layout)
        cont_layout.addStretch()

class TransparentOverlay(QMainWindow):
    request_model_switch = pyqtSignal(str) # "3B" or "1.5B"

    def __init__(self):
        super().__init__()
        self.oldPos = self.pos()
        self.initUI()

    def initUI(self):
        # Window setup
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Geometry: Right side of the screen
        screen = QApplication.primaryScreen().geometry()
        width = 400
        height = 600
        self.setGeometry(screen.width() - width - 20, 20, width, height)

        # Main Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.central_widget.setLayout(self.layout)

        # Styling & Container
        self.container = QFrame()
        self.container.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 80); 
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 20);
            }
        """)
        self.layout.addWidget(self.container)
        
        self.container_layout = QVBoxLayout()
        self.container_layout.setContentsMargins(0, 0, 0, 5) 
        self.container_layout.setSpacing(5)
        self.container.setLayout(self.container_layout)

        # --- Custom Title Bar ---
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(40)
        self.title_bar.setStyleSheet("background-color: rgba(255, 255, 255, 5); border-top-left-radius: 15px; border-top-right-radius: 15px; border-bottom: none;")
        self.title_bar_layout = QHBoxLayout()
        self.title_bar_layout.setContentsMargins(15, 0, 10, 0)
        self.title_bar.setLayout(self.title_bar_layout)

        # Title
        self.title_label = QLabel("Chit Chat AI")
        self.title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #00e5ff; background: transparent; border: none;")
        self.title_bar_layout.addWidget(self.title_label)
        
        self.title_bar_layout.addStretch()

        # Window Controls
        btn_style = """
            QPushButton {
                background-color: transparent; 
                color: white; 
                border: none; 
                font-size: 14px;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 30);
            }
        """
        
        # History Toggle
        self.history_active = False 
        self.btn_history = QPushButton("🕒")
        self.btn_history.setFixedSize(30, 30)
        self.btn_history.setStyleSheet(btn_style)
        self.btn_history.setToolTip("Toggle History")
        self.btn_history.clicked.connect(self.toggle_history)
        self.title_bar_layout.addWidget(self.btn_history)

        # Model Toggle (3B vs 1.5B)
        self.current_model = "3B"
        self.btn_model = QPushButton("🧠 3B")
        self.btn_model.setFixedSize(60, 30)
        self.btn_model.setStyleSheet(btn_style)
        self.btn_model.setToolTip("Switch Model (Smart vs Fast)")
        self.btn_model.clicked.connect(self.toggle_model)
        self.title_bar_layout.addWidget(self.btn_model)

        # Developer Profile
        self.btn_dev = QPushButton("👨‍💻")
        self.btn_dev.setFixedSize(30, 30)
        self.btn_dev.setStyleSheet(btn_style)
        self.btn_dev.setToolTip("Developer Profile")
        self.btn_dev.clicked.connect(self.show_developer_profile)
        self.title_bar_layout.addWidget(self.btn_dev)

        # Minimize
        self.btn_min = QPushButton("─")
        self.btn_min.setFixedSize(30, 30)
        self.btn_min.setStyleSheet(btn_style)
        self.btn_min.clicked.connect(self.showMinimized)
        self.title_bar_layout.addWidget(self.btn_min)

        # Maximize/Restore
        self.btn_max = QPushButton("□")
        self.btn_max.setFixedSize(30, 30)
        self.btn_max.setStyleSheet(btn_style)
        self.btn_max.clicked.connect(self.toggle_maximize)
        self.title_bar_layout.addWidget(self.btn_max)

        # Close
        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(30, 30)
        self.btn_close.setStyleSheet(btn_style + "QPushButton:hover { background-color: rgba(255, 0, 0, 150); }")
        self.btn_close.clicked.connect(self.close)
        self.title_bar_layout.addWidget(self.btn_close)

        self.container_layout.addWidget(self.title_bar)
        
        # --- Body Content ---
        # Status Label
        self.status_label = QLabel("Listening...")
        self.status_label.setFont(QFont("Segoe UI", 10))
        self.status_label.setStyleSheet("color: #aaaaaa; background: transparent; border: none; padding: 0 10px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.container_layout.addWidget(self.status_label)

        # Stacked Layout for Pages
        self.stacked_widget = QWidget()
        self.stacked_layout = QStackedLayout()
        self.stacked_widget.setLayout(self.stacked_layout)
        
        # Page 1: Live Chat (Latest Only)
        self.page_live = QTextEdit()
        self.page_live.setReadOnly(True)
        self.page_live.setFont(QFont("Segoe UI", 14)) # Larger font for live view
        self.page_live.setStyleSheet(self._get_text_style())
        self.stacked_layout.addWidget(self.page_live)
        
        # Page 2: History (Full Log)
        self.page_history = QTextEdit()
        self.page_history.setReadOnly(True)
        self.page_history.setFont(QFont("Segoe UI", 11))
        self.page_history.setStyleSheet(self._get_text_style())
        self.stacked_layout.addWidget(self.page_history)
        
        self.container_layout.addWidget(self.stacked_widget)
        
        # Start on Live Page
        self.stacked_layout.setCurrentIndex(0)

    def _get_text_style(self):
        return """
            QTextEdit {
                background-color: transparent; 
                color: white; 
                border: none; 
                padding: 10px;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(0,0,0,0);
                width: 8px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 50);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """

    def toggle_history(self):
        if self.stacked_layout.currentIndex() == 0:
            self.stacked_layout.setCurrentIndex(1)
            self.title_label.setText("Chit Chat AI - History")
        else:
            self.stacked_layout.setCurrentIndex(0)
            self.title_label.setText("Chit Chat AI")

    def toggle_model(self):
        if self.current_model == "3B":
            self.current_model = "1.5B"
            self.btn_model.setText("⚡ 1.5B")
            self.request_model_switch.emit("1.5B")
        else:
            self.current_model = "3B"
            self.btn_model.setText("🧠 3B")
            self.request_model_switch.emit("3B")

    # --- Window Dragging Logic ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition().toPoint()
            
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def update_status(self, text):
        self.status_label.setText(text)

    def show_developer_profile(self):
        dlg = DeveloperPopup(self)
        # Center on parent
        geo = self.geometry()
        x = geo.x() + (geo.width() - 300) // 2
        y = geo.y() + (geo.height() - 470) // 2
        dlg.move(x, y)
        dlg.exec()

    def process_markdown(self, text):
        import re
        import html
        
        # Split by code blocks
        parts = re.split(r'(```.*?```)', text, flags=re.DOTALL)
        formatted_parts = []
        
        for part in parts:
            if part.startswith('```') and part.endswith('```'):
                # Code Block
                content = part[3:-3].strip()
                # Remove language identifier if present
                if '\n' in content:
                    first_line, rest = content.split('\n', 1)
                    if ' ' not in first_line.strip() and len(first_line.strip()) < 15:
                        content = rest
                
                content = html.escape(content)
                code_html = f'<pre style="background-color: #2b2b2b; color: #a9b7c6; padding: 10px; border-radius: 5px; margin: 10px 0; font-family: Consolas, monospace;">{content}</pre>'
                formatted_parts.append(code_html)
            else:
                # Normal Text
                part = html.escape(part)
                part = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', part)
                part = part.replace('\n', '<br>')
                formatted_parts.append(part)
                
        return "".join(formatted_parts)

    def append_message(self, role, message):
         if role == "User":
             color = "#00ff9d" # Greenish cyan
             bg = "rgba(0, 255, 157, 20)"
             formatted_msg = self.process_markdown(message)
             
             # CLEAR Live page when user speaks new thing
             self.page_live.clear()
             
             # Also ensure we switch back to live view if automatic behavior is desired
             # self.stacked_layout.setCurrentIndex(0) 
         else:
             color = "#00e5ff" # Cyan
             bg = "rgba(0, 229, 255, 20)"
             formatted_msg = self.process_markdown(message)
         
         html_content = f"""
         <div style="margin-bottom: 15px;">
            <div style="color: {color}; font-weight: bold; font-size: 10pt; margin-bottom: 2px;">{role}</div>
            <div style="background-color: {bg}; padding: 8px; border-radius: 10px; color: white;">{formatted_msg}</div>
         </div>
         """
         
         # Append to BOTH views
         self.page_live.append(html_content)
         self.page_history.append(html_content)
         
         # Scroll both
         sb_live = self.page_live.verticalScrollBar()
         sb_live.setValue(sb_live.maximum())
         
         sb_hist = self.page_history.verticalScrollBar()
         sb_hist.setValue(sb_hist.maximum())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransparentOverlay()
    window.show()
    sys.exit(app.exec())
