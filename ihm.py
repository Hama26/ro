import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QMessageBox, QGridLayout, QTextEdit, QHBoxLayout, QFormLayout)
from PyQt5.QtGui import QFont
from optimization_solver import solve_production_planning, solve_knapsack

class OptimizationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window setup
        self.setWindowTitle("Optimization Solver")
        self.setGeometry(100, 100, 800, 500)
        self.setFont(QFont("Arial", 10))

        # Layout
        main_layout = QHBoxLayout()
        pp_layout = QFormLayout()
        kp_layout = QFormLayout()

        # Production Planning Section
        self.labor_input = QLineEdit(self)
        self.material_input = QLineEdit(self)
        pp_layout.addRow(QLabel("Labor Available:"), self.labor_input)
        pp_layout.addRow(QLabel("Materials Available:"), self.material_input)
        self.solve_pp_btn = QPushButton('Solve Production Planning', self)
        self.solve_pp_btn.clicked.connect(self.solve_production_planning)
        pp_layout.addRow(self.solve_pp_btn)
        self.pp_results_label = QTextEdit()
        self.pp_results_label.setReadOnly(True)
        pp_layout.addRow(self.pp_results_label)

        # Knapsack Section
        self.capacity_input = QLineEdit(self)
        self.values_input = QLineEdit(self)
        self.weights_input = QLineEdit(self)
        kp_layout.addRow(QLabel("Knapsack Capacity (kg):"), self.capacity_input)
        kp_layout.addRow(QLabel("Item Values (comma-separated):"), self.values_input)
        kp_layout.addRow(QLabel("Item Weights (comma-separated):"), self.weights_input)
        self.solve_kp_btn = QPushButton('Solve Knapsack Problem', self)
        self.solve_kp_btn.clicked.connect(self.solve_knapsack)
        kp_layout.addRow(self.solve_kp_btn)
        self.kp_results_label = QTextEdit()
        self.kp_results_label.setReadOnly(True)
        kp_layout.addRow(self.kp_results_label)

        # Set central widget and layout
        central_widget = QWidget()
        main_layout.addLayout(pp_layout)
        main_layout.addLayout(kp_layout)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def solve_production_planning(self):
        try:
            labor = float(self.labor_input.text())
            material = float(self.material_input.text())
            optimal_production, total_profit = solve_production_planning(labor, material)
            self.pp_results_label.setText(f"Optimal Production Levels:\nProduct 1: {optimal_production[0]:.2f} units\nProduct 2: {optimal_production[1]:.2f} units\nTotal Profit: ${total_profit:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numerical values for labor and materials.")

    def solve_knapsack(self):
        try:
            capacity = int(self.capacity_input.text())
            values = list(map(int, self.values_input.text().split(',')))
            weights = list(map(int, self.weights_input.text().split(',')))
            selected_items, total_value = solve_knapsack(capacity, values, weights)
            item_display = ", ".join(f"Item {i+1}" for i in selected_items)
            self.kp_results_label.setText(f"Selected Items: {item_display}\nTotal Value: ${total_value:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please ensure all inputs are integers and formatted correctly.")

# Main function to run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OptimizationApp()
    ex.show()
    sys.exit(app.exec_())
