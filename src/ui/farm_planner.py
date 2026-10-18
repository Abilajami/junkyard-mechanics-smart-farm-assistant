from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QListWidget, QSpinBox, QMessageBox
from src.services.farm_optimizer import filter_accessible, strategy_highest_tier, strategy_highest_price, strategy_best_estimated_profit, estimate_profit

class FarmPlannerView(QWidget):
    def __init__(self, repo):
        super().__init__()
        self.repo = repo
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        top = QHBoxLayout()
        self.strategy = QComboBox()
        self.strategy.addItems(['Highest-Tier Available', 'Highest-Priced Available', 'Best Estimated Profit'])
        self.budget_spin = QSpinBox()
        self.budget_spin.setRange(0, 10_000_000)
        self.budget_spin.setPrefix('Budget: ')
        run_btn = QPushButton('Run Strategy')
        run_btn.clicked.connect(self.run_strategy)
        top.addWidget(self.strategy)
        top.addWidget(self.budget_spin)
        top.addWidget(run_btn)

        self.results = QListWidget()
        layout.addLayout(top)
        layout.addWidget(QLabel('Recommendations:'))
        layout.addWidget(self.results)

    def run_strategy(self):
        vehicles = self.repo.list_vehicles()
        candidates = filter_accessible(vehicles)
        if not candidates:
            QMessageBox.information(self, 'No candidates', 'No accessible vehicles recorded.')
            return
        sel = self.strategy.currentText()
        budget = self.budget_spin.value()
        self.results.clear()
        if sel == 'Highest-Tier Available':
            ranked = strategy_highest_tier(candidates)
            for v in ranked[:5]:
                self.results.addItem(f"{v.name} — Tier {v.tier} — {v.junkyard_location} — {v.purchase_price}")
        elif sel == 'Highest-Priced Available':
            ranked = strategy_highest_price(candidates, budget if budget>0 else None)
            for v in ranked[:5]:
                self.results.addItem(f"{v.name} — {v.purchase_price}")
        else:
            ranked = strategy_best_estimated_profit(candidates)
            for entry in ranked[:5]:
                v = entry['vehicle']
                est = entry['estimate']
                missing = entry['missing']
                if est is None:
                    self.results.addItem(f"{v.name} — Estimate: Incomplete data ({', '.join(missing)})")
                else:
                    self.results.addItem(f"{v.name} — EstProfit: {est}")
