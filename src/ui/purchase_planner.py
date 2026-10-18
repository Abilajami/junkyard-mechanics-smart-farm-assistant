from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from src.services.purchase_service import PurchaseService

class PurchasePlannerView(QWidget):
    def __init__(self, repo):
        super().__init__()
        self.repo = repo
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        self.selected_label = QLabel('Selected vehicle: None')
        cash_layout = QHBoxLayout()
        self.cash_input = QLineEdit()
        self.cash_input.setPlaceholderText('Enter your current cash')
        self.evaluate_btn = QPushButton('Evaluate Selected')
        self.evaluate_btn.clicked.connect(self.evaluate)
        cash_layout.addWidget(self.cash_input)
        cash_layout.addWidget(self.evaluate_btn)

        layout.addWidget(self.selected_label)
        layout.addLayout(cash_layout)
        self.advice_label = QLabel('Advice:')
        layout.addWidget(self.advice_label)

        # For MVP: select first vehicle as selected
        vehicles = self.repo.list_vehicles()
        if vehicles:
            self.selected = vehicles[0]
            self.selected_label.setText(f'Selected vehicle: {self.selected.name} ({self.selected.tier})')
        else:
            self.selected = None

    def evaluate(self):
        try:
            cash = int(self.cash_input.text())
        except Exception:
            QMessageBox.information(self, 'Invalid', 'Enter a numeric cash amount.')
            return
        advice = PurchaseService.evaluate_purchase(self.selected, current_cash=cash)
        txt = f"Vehicle: {advice.vehicle_name}\nPrice: {advice.asking_price}\nCurrent Cash: {advice.current_cash}\nShortfall: {advice.shortfall}\nAffordable: {advice.affordable}\nReason: {advice.reason}"
        self.advice_label.setText(txt)
