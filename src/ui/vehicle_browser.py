from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, QHBoxLayout, QTextEdit, QLineEdit, QFileDialog, QMessageBox
from PySide6.QtCore import Qt
import csv
from datetime import datetime

class VehicleBrowser(QWidget):
    def __init__(self, repo):
        super().__init__()
        self.repo = repo
        self._init_ui()
        self.refresh_list()

    def _init_ui(self):
        layout = QHBoxLayout(self)

        self.list_widget = QListWidget()
        self.list_widget.itemSelectionChanged.connect(self.on_select)

        right = QVBoxLayout()
        self.details = QTextEdit()
        self.details.setReadOnly(True)
        right.addWidget(self.details)

        btn_layout = QHBoxLayout()
        add_btn = QPushButton('Add Sample')
        add_btn.clicked.connect(self.on_add_sample)
        import_btn = QPushButton('Import CSV')
        import_btn.clicked.connect(self.on_import)
        export_btn = QPushButton('Export CSV')
        export_btn.clicked.connect(self.on_export)
        delete_btn = QPushButton('Delete')
        delete_btn.clicked.connect(self.on_delete)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(import_btn)
        btn_layout.addWidget(export_btn)
        btn_layout.addWidget(delete_btn)

        right.addLayout(btn_layout)

        layout.addWidget(self.list_widget, 1)
        layout.addLayout(right, 2)

    def refresh_list(self):
        self.list_widget.clear()
        vehicles = self.repo.list_vehicles()
        for v in vehicles:
            self.list_widget.addItem(f"{v.name} ({v.tier or 'Unknown'})")

    def on_select(self):
        sel = self.list_widget.currentRow()
        if sel < 0:
            self.details.setText('')
            return
        vehicles = self.repo.list_vehicles()
        v = vehicles[sel]
        txt = '\n'.join([f'{k}: {v.to_dict()[k]}' for k in v.to_dict()])
        self.details.setText(txt)

    def on_add_sample(self):
        self.repo.seed_sample()
        self.refresh_list()
        QMessageBox.information(self, 'Sample Added', 'A sample vehicle was added to the database.')

    def on_import(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Import CSV', '', 'CSV Files (*.csv)')
        if not path:
            return
        count = 0
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    self.repo.add_vehicle(
                        name=row.get('name') or 'Unknown',
                        tier=row.get('tier'),
                        category=row.get('category'),
                        purchase_price=int(row['purchase_price']) if row.get('purchase_price') else None,
                        resale_price=int(row['resale_price']) if row.get('resale_price') else None,
                        repair_cost=int(row['repair_cost']) if row.get('repair_cost') else None,
                        junkyard_location=row.get('junkyard_location'),
                        availability_status=row.get('availability_status'),
                        collection_status=row.get('collection_status'),
                        data_source=row.get('data_source'),
                        last_verified=datetime.utcnow(),
                        notes=row.get('notes')
                    )
                    count += 1
                except Exception:
                    continue
        self.refresh_list()
        QMessageBox.information(self, 'Import Complete', f'Imported {count} vehicles.')

    def on_export(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Export CSV', '', 'CSV Files (*.csv)')
        if not path:
            return
        vehicles = self.repo.list_vehicles()
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name','tier','category','purchase_price','resale_price','repair_cost','junkyard_location','availability_status','collection_status','data_source','last_verified','notes'])
            for v in vehicles:
                d = v.to_dict()
                writer.writerow([d['name'], d['tier'], d['category'], d['purchase_price'] if isinstance(d['purchase_price'], int) else '', d['resale_price'] if isinstance(d['resale_price'], int) else '', d['repair_cost'] if isinstance(d['repair_cost'], int) else '', d['junkyard_location'], d['availability_status'], d['collection_status'], d['data_source'], d['last_verified'], d['notes']])
        QMessageBox.information(self, 'Export Complete', f'Exported {len(vehicles)} vehicles.')

    def on_delete(self):
        sel = self.list_widget.currentRow()
        if sel < 0:
            return
        vehicles = self.repo.list_vehicles()
        v = vehicles[sel]
        # simple delete via session
        from sqlalchemy import delete
        from src.database.models import Vehicle
        with self.repo.Session() as s:
            s.execute(delete(Vehicle).where(Vehicle.id == v.id))
            s.commit()
        self.refresh_list()
        QMessageBox.information(self, 'Deleted', f'Deleted {v.name}')
