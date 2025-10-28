from ui import QApplication, NavManager
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NavManager()
    window.show()
    sys.exit(app.exec())