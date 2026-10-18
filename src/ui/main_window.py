from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QHBoxLayout, QMessageBox
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt
from src.ui.vehicle_browser import VehicleBrowser
from src.ui.farm_planner import FarmPlannerView
from src.ui.purchase_planner import PurchasePlannerView
from src.ui.inventory import CollectionView

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
        self.nav = QListWidget()
        self.nav.addItems([
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
        self.nav.setMaximumWidth(220)
        self.nav.currentRowChanged.connect(self._on_nav_changed)

        # Main panel
        self.main_panel = QWidget()
        self.main_layout = QVBoxLayout(self.main_panel)
        self.main_layout.addWidget(QLabel('<b>Welcome to Junkyard Mechanics Smart Farm Assistant</b>'))

        layout.addWidget(self.nav)
        layout.addWidget(self.main_panel, 1)

    def _on_nav_changed(self, idx):
        # Clear
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        label = self.nav.item(idx).text()
        if label == 'Vehicle Database':
            view = VehicleBrowser(self.repo)
            self.main_layout.addWidget(view)
        elif label == 'Smart Farm Planner':
            view = FarmPlannerView(self.repo)
            self.main_layout.addWidget(view)
        elif label == 'Purchase Assistant':
            view = PurchasePlannerView(self.repo)
            self.main_layout.addWidget(view)
        elif label == 'My Collection':
            view = CollectionView(self.repo)
            self.main_layout.addWidget(view)
        else:
            self.main_layout.addWidget(QLabel(f'<h2>{label}</h2>'))
