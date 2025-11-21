import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from ui import LoginDialog, MainWindow
import database
from styles import STYLES

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(STYLES)  # Apply global styles

    # Initialize DB
    if not os.path.exists(database.DB_PATH):
        database.init_db()

    # Login
    login = LoginDialog()
    if login.exec() == LoginDialog.DialogCode.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
