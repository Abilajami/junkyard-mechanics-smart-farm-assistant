from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.database.repository import Repository, init_db
import sys

DB_PATH = 'data.db'


def main():
    # Initialize DB
    engine = init_db(DB_PATH)
    repo = Repository(engine)

    app = QApplication(sys.argv)
    win = MainWindow(repo)
    win.resize(1280, 800)
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
