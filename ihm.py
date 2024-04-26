import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QMessageBox, QGridLayout, QTextEdit, QHBoxLayout, QFormLayout)
from PyQt5.QtGui import QFont
from optimization_solver import solve_diet, solve_production_planning, solve_knapsack

class OptimizationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window setup
        self.setWindowTitle("Optimization Solver")
        self.setGeometry(100, 100, 1000, 500)  # Increased width for diet section
        self.setFont(QFont("Arial", 10))

        # Layout
        main_layout = QHBoxLayout()
        pp_layout = QFormLayout()
        kp_layout = QFormLayout()
        diet_layout = QFormLayout()


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

        # Diet Section
        self.calories_needed_input = QLineEdit(self)
        self.protein_needed_input = QLineEdit(self)
        self.fat_needed_input = QLineEdit(self)
        self.food_calories_input = QLineEdit(self)
        self.food_protein_input = QLineEdit(self)
        self.food_fat_input = QLineEdit(self)
        self.food_cost_input = QLineEdit(self)

        diet_layout.addRow(QLabel("Calories Needed:"), self.calories_needed_input)
        diet_layout.addRow(QLabel("Protein Needed (grams):"), self.protein_needed_input)
        diet_layout.addRow(QLabel("Fat Needed (grams):"), self.fat_needed_input)
        diet_layout.addRow(QLabel("Food Calories (comma-separated):"), self.food_calories_input)
        diet_layout.addRow(QLabel("Food Protein (grams, comma-separated):"), self.food_protein_input)
        diet_layout.addRow(QLabel("Food Fat (grams, comma-separated):"), self.food_fat_input)
        diet_layout.addRow(QLabel("Food Cost (comma-separated):"), self.food_cost_input)

        self.solve_diet_btn = QPushButton('Solve Diet Problem', self)
        self.solve_diet_btn.clicked.connect(self.solve_diet)
        diet_layout.addRow(self.solve_diet_btn)
        self.diet_results_label = QTextEdit()
        self.diet_results_label.setReadOnly(True)
        diet_layout.addRow(self.diet_results_label)

        # Set central widget and layout
        central_widget = QWidget()
        main_layout.addLayout(pp_layout)
        main_layout.addLayout(kp_layout)
        main_layout.addLayout(diet_layout)
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

    def solve_diet(self):
      try:
        calories_needed = float(self.calories_needed_input.text())
        protein_needed = float(self.protein_needed_input.text())
        fat_needed = float(self.fat_needed_input.text())

        food_calories = list(map(float, self.food_calories_input.text().split(',')))
        food_protein = list(map(float, self.food_protein_input.text().split(',')))
        food_fat = list(map(float, self.food_fat_input.text().split(',')))
        food_cost = list(map(float, self.food_cost_input.text().split(',')))

        optimal_quantities, total_cost = solve_diet(calories_needed, protein_needed, fat_needed, food_calories, food_protein, food_fat, food_cost)
        food_names = ["Food {}".format(i+1) for i in range(len(optimal_quantities))]  # Assuming food names are in this format

        # Display results
        food_list = []
        for i, quantity in enumerate(optimal_quantities):
          if quantity > 0:  # Only show foods included in the diet
            food_list.append(f"{food_names[i]}: {quantity:.2f} units")
        food_display = "\n".join(food_list)
        self.diet_results_label.setText(f"Selected Foods:\n{food_display}\nTotal Cost: ${total_cost:.2f}")
      except ValueError:
        QMessageBox.warning(self, "Input Error", "Please ensure all inputs are numerical and formatted correctly (comma-separated lists for food data).")
        
# Main function to run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OptimizationApp()
    ex.show()
    sys.exit(app.exec_())