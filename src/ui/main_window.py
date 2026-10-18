from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QHBoxLayout
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, repo):
        super().__init__()
        self.repo = repo
        self.setWindowTitle('Junkyard Mechanics — Smart Farm Assistant')
        self.setMinimumSize(1280, 800)
        self._apply_dark_theme()
        self._init_ui()

    def _apply_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(18, 18, 18))
        palette.setColor(QPalette.AlternateBase, QColor(30, 30, 30))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(45, 45, 45))
        palette.setColor(QPalette.ButtonText, Qt.white)
        self.setPalette(palette)

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)

        # Left navigation list
        nav = QListWidget()
        nav.addItems([
            'Overview Dashboard',
            'Target Car',
            'Smart Farm Planner',
            'Accessible Junkyards',
            'Vehicle Database',
            'Purchase Assistant',
            'My Collection',
            'Session History',
            'Settings'
        ])
        nav.setMaximumWidth(220)
        nav.currentRowChanged.connect(self._on_nav_changed)

        # Main panel
        self.main_panel = QWidget()
        self.main_layout = QVBoxLayout(self.main_panel)
        self.main_layout.addWidget(QLabel('<b>Welcome to Junkyard Mechanics Smart Farm Assistant</b>'))

        layout.addWidget(nav)
        layout.addWidget(self.main_panel, 1)

    def _on_nav_changed(self, idx):
        # Simple placeholder navigation handler
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        labels = [
            'Overview Dashboard',
            'Target Car',
            'Smart Farm Planner',
            'Accessible Junkyards',
            'Vehicle Database',
            'Purchase Assistant',
            'My Collection',
            'Session History',
            'Settings'
        ]
        label = QLabel(f'<h2>{labels[idx]}</h2>')
        self.main_layout.addWidget(label)
