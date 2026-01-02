from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QWidget, QFrame, QHBoxLayout, QPushButton, QStackedLayout, QTextEdit, QDialog, QInputDialog)
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QUrl, QSize
from PyQt6.QtGui import QFont, QDesktopServices, QPixmap, QPainter, QPainterPath, QCursor, QIcon, QTextCursor
import os
import ctypes
from ctypes import wintypes

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
    correction_ready = pyqtSignal(str)     # Signal for corrected text

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

        # Prevent screen capture
        try:
            # WDA_EXCLUDEFROMCAPTURE = 0x00000011
            hwnd = int(self.winId())
            result = ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, 0x00000011)
            if result == 0:
                print("Warning: SetWindowDisplayAffinity failed.")
            else:
                print("Screen capture protection enabled.")
        except Exception as e:
            print(f"Error setting display affinity: {e}")
        
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



        # Developer Profile
        self.btn_dev = QPushButton("👨‍💻")
        self.btn_dev.setFixedSize(30, 30)
        self.btn_dev.setStyleSheet(btn_style)
        self.btn_dev.setToolTip("Developer Profile")
        self.btn_dev.clicked.connect(self.show_developer_profile)
        self.title_bar_layout.addWidget(self.btn_dev)

        # Edit Last Input (Correction)
        self.btn_edit = QPushButton("✏️")
        self.btn_edit.setFixedSize(30, 30)
        self.btn_edit.setStyleSheet(btn_style)
        self.btn_edit.setToolTip("Edit Last Input")
        self.btn_edit.clicked.connect(self.edit_last_input)
        self.title_bar_layout.addWidget(self.btn_edit)

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
        # Enable Robust Interaction
        self.page_live.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.page_live.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu) # standard right click
        self.page_live.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction) # Full interaction minus editing (since readonly)
        self.page_live.setFont(QFont("Segoe UI", 12)) # Reduced font size
        self.page_live.setStyleSheet(self._get_text_style())
        self.stacked_layout.addWidget(self.page_live)
        
        # Page 2: History (Full Log)
        self.page_history = QTextEdit()
        self.page_history.setReadOnly(True)
        # Enable Robust Interaction
        self.page_history.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.page_history.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.page_history.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.page_history.setFont(QFont("Segoe UI", 10))
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



    # --- Window Dragging Logic ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # ONLY drag if clicked on Title Bar
            child = self.childAt(event.position().toPoint())
            # We check if the child is part of title bar hierarchy
            if child:
                # Naive check: if child or its parent is the title bar
                # Better: Check if the click is within the title bar geometry relative to window
                if self.title_bar.geometry().contains(event.position().toPoint()):
                    self.oldPos = event.globalPosition().toPoint()
                    self.dragging = True
                else:
                    self.dragging = False

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, 'dragging') and self.dragging:
            delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition().toPoint()
            
    def mouseReleaseEvent(self, event):
        self.dragging = False
            
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

    def edit_last_input(self):
        last_text = getattr(self, 'last_user_text', "")
        if not last_text:
            return

        # Simple Input Dialog
        from PyQt6.QtWidgets import QInputDialog, QLineEdit
        text, ok = QInputDialog.getText(self, "Correct Input", "Edit last message:", text=last_text)
        
        if ok and text:
            self.correction_ready.emit(text)

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
                content = content.replace('\n', '<br>')
                
                # Use Table for Code Box (Qt supports this better than div/pre styling)
                code_html = f"""
                <table width="100%" cellpadding="10" cellspacing="0" style="background-color: #2b2b2b; color: #a9b7c6; border-radius: 5px; margin-top: 10px; margin-bottom: 10px;">
                    <tr>
                        <td>
                            <pre style="font-family: Consolas, monospace; margin: 0;">{content}</pre>
                        </td>
                    </tr>
                </table>
                """
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
             # Save for editing
             self.last_user_text = message
             
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

    # --- Streaming Support ---
    def start_streaming_message(self, role):
        """Prepares the UI for a new incoming streamed message."""
        if role == "User":
             color = "#00ff9d" 
             bg = "rgba(0, 255, 157, 20)"
             self.page_live.clear() 
        else:
             color = "#00e5ff"
             bg = "rgba(0, 229, 255, 20)"

        self.current_stream_role = role
        self.current_stream_content = ""
        
        # 1. Capture Start Positions for final replacement
        # We need to know where this message started to replace it with the formatted block later.
        self.live_start_pos = self.page_live.document().characterCount() - 1
        self.hist_start_pos = self.page_history.document().characterCount() - 1
        
        # 2. Append Header (Visual only for now)
        header_html = f'<div style="color: {color}; font-weight: bold; margin-top: 10px;">{role}</div>'
        self.page_live.append(header_html)
        self.page_history.append(header_html)
        
        # 3. Force "Normal White" style for the subsequent streaming text
        # If we don't do this, it might inherit the Bold/Color of the header
        from PyQt6.QtGui import QTextCharFormat, QColor, QFont
        import hashlib
        
        fmt = QTextCharFormat()
        fmt.setForeground(QColor("white"))
        fmt.setFontWeight(QFont.Weight.Normal)
        fmt.setFontPointSize(10) # Match normal size
        
        self.page_live.setCurrentCharFormat(fmt)
        self.page_history.setCurrentCharFormat(fmt)

    def stream_token(self, token):
        """Appends a token to the current message."""
        if not hasattr(self, 'current_stream_content'):
            self.current_stream_content = ""
            
        self.current_stream_content += token
        
        # Update Live View (Fast)
        self.page_live.moveCursor(QTextCursor.MoveOperation.End)
        self.page_live.insertPlainText(token)
        self.page_live.verticalScrollBar().setValue(self.page_live.verticalScrollBar().maximum())
        
        # Update History View
        self.page_history.moveCursor(QTextCursor.MoveOperation.End)
        self.page_history.insertPlainText(token)
        self.page_history.verticalScrollBar().setValue(self.page_history.verticalScrollBar().maximum())

    def end_streaming_message(self):
        """Finalize the message by replacing raw text with formatted HTML (Bubbles + Code)."""
        full_text = getattr(self, 'current_stream_content', "")
        role = getattr(self, 'current_stream_role', "Assistant")
        
        # Save text for copying/editing
        if role == "User":
            self.last_user_text = full_text
        else:
            self.last_assistant_text = full_text

        if not full_text:
            return

        # Helper to replace range with formatted message
        def replace_range(text_edit, start_pos, new_html):
            cursor = text_edit.textCursor()
            cursor.setPosition(start_pos)
            cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
            cursor.removeSelectedText()
            # Now append the nice formatted message
            # But wait, append() adds to end. insertHtml inserts at cursor.
            # Using insertHtml might be inline. 
            # We want to use append_message logic but putting it HERE.
            # actually append_message calculates the HTML.
            
            # Let's manually generate HTML and insert it.
            # We use the LOGIC from append_message but we insert it.
            
            if role == "User":
                 color = "#00ff9d" 
                 bg = "rgba(0, 255, 157, 20)"
            else:
                 color = "#00e5ff"
                 bg = "rgba(0, 229, 255, 20)"
                 
            formatted_msg = self.process_markdown(full_text)
            
            html_content = f"""
             <div style="margin-bottom: 15px;">
                <div style="color: {color}; font-weight: bold; font-size: 10pt; margin-bottom: 2px;">{role}</div>
                <div style="background-color: {bg}; padding: 8px; border-radius: 10px; color: white;">{formatted_msg}</div>
             </div>
             """
            
            cursor.insertHtml(html_content)
            
            # Scroll to bottom
            sb = text_edit.verticalScrollBar()
            sb.setValue(sb.maximum())

        # Apply to both
        if hasattr(self, 'live_start_pos'):
            replace_range(self.page_live, self.live_start_pos, full_text)
        if hasattr(self, 'hist_start_pos'):
            replace_range(self.page_history, self.hist_start_pos, full_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransparentOverlay()
    window.show()
    sys.exit(app.exec())
