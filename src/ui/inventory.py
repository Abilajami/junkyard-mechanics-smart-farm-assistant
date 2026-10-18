from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, QMessageBox

class CollectionView(QWidget):
    def __init__(self, repo):
        super().__init__()
        self.repo = repo
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.refresh()
        layout.addWidget(QLabel('My Collection'))
        layout.addWidget(self.list_widget)
        btn = QPushButton('Refresh')
        btn.clicked.connect(self.refresh)
        layout.addWidget(btn)

    def refresh(self):
        self.list_widget.clear()
        vehicles = self.repo.list_vehicles()
        for v in vehicles:
            status = v.collection_status or 'Unknown'
            self.list_widget.addItem(f"{v.name} — {status}")
