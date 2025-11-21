# Modern Blue Theme Colors
# Primary: #2563eb (Blue 600)
# Hover: #1d4ed8 (Blue 700)
# Background: #f8fafc (Slate 50)
# Surface: #ffffff (White)
# Text: #1e293b (Slate 800)
# Border: #cbd5e1 (Slate 300)

STYLES = """
QWidget {
    font-family: 'Malgun Gothic', 'Segoe UI', sans-serif;
    font-size: 14px;
    color: #1e293b;
    background-color: #f8fafc;
}

/* --- Main Window & Containers --- */
QMainWindow {
    background-color: #f8fafc;
}

QFrame, QWidget#white_bg {
    background-color: #ffffff;
    border-radius: 8px;
}

/* --- Buttons --- */
QPushButton {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1d4ed8;
}

QPushButton:pressed {
    background-color: #1e40af;
}

QPushButton:disabled {
    background-color: #94a3b8;
}

/* --- Inputs --- */
QLineEdit, QTextEdit, QComboBox, QDateEdit {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 6px;
    selection-background-color: #2563eb;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus {
    border: 2px solid #2563eb;
}

/* --- List Widget --- */
QListWidget {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 5px;
    outline: none;
}

QListWidget::item {
    padding: 8px;
    border-radius: 4px;
    margin-bottom: 2px;
}

QListWidget::item:selected {
    background-color: #eff6ff;
    color: #2563eb;
    border: 1px solid #bfdbfe;
}

QListWidget::item:hover {
    background-color: #f1f5f9;
}

/* --- Scroll Area --- */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    border: none;
    background: #f1f5f9;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #cbd5e1;
    border-radius: 4px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* --- Splitter --- */
QSplitter::handle {
    background-color: #e2e8f0;
}

/* --- Custom Log Card --- */
QFrame#log_card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 10px;
}

QLabel#date_label {
    color: #64748b;
    font-size: 12px;
    font-weight: bold;
}

QLabel#category_label {
    color: #2563eb;
    font-weight: bold;
    background-color: #eff6ff;
    padding: 2px 6px;
    border-radius: 4px;
}

QLabel#important_label {
    color: #ef4444;
    font-weight: bold;
}
"""
