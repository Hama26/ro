import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QMessageBox, QTextEdit, QHBoxLayout, QComboBox
)
from PyQt5.QtGui import QFont
from optimization_solver import solve_diet, solve_production_planning, solve_knapsack

class OptimizationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window setup
        self.setWindowTitle("Optimization Solver")
        self.setGeometry(200, 200, 1000, 500)
        self.setFont(QFont("Arial", 10))

        # Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # ComboBox to select problem
        self.problem_selector = QComboBox(self)
        self.problem_selector.addItems(["Select Problem", "Production Planning", "Knapsack Problem", "Diet Problem"])
        self.problem_selector.currentIndexChanged.connect(self.display_selected_problem)
        self.layout.addWidget(self.problem_selector)

    def init_production_planning_layout(self):
        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.go_back_to_selection)

        self.pp_layout = QVBoxLayout()
        self.labor_input = QLineEdit(self)
        self.material_input = QLineEdit(self)
        self.pp_layout.addWidget(QLabel("Labor Available:"))
        self.pp_layout.addWidget(self.labor_input)
        self.pp_layout.addWidget(QLabel("Materials Available:"))
        self.pp_layout.addWidget(self.material_input)
        self.solve_pp_btn = QPushButton('Solve Production Planning', self)
        self.solve_pp_btn.clicked.connect(self.solve_production_planning)
        self.pp_layout.addWidget(self.solve_pp_btn)
        self.pp_results_label = QTextEdit()
        self.pp_results_label.setReadOnly(True)
        self.pp_layout.addWidget(self.pp_results_label)
        self.pp_layout.addWidget(self.back_button)


    def init_knapsack_layout(self):
        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.go_back_to_selection)

        self.kp_layout = QVBoxLayout()
        self.capacity_input = QLineEdit(self)
        self.values_input = QLineEdit(self)
        self.weights_input = QLineEdit(self)
        self.kp_layout.addWidget(QLabel("Knapsack Capacity (kg):"))
        self.kp_layout.addWidget(self.capacity_input)
        self.kp_layout.addWidget(QLabel("Item Values (comma-separated):"))
        self.kp_layout.addWidget(self.values_input)
        self.kp_layout.addWidget(QLabel("Item Weights (comma-separated):"))
        self.kp_layout.addWidget(self.weights_input)
        self.solve_kp_btn = QPushButton('Solve Knapsack Problem', self)
        self.solve_kp_btn.clicked.connect(self.solve_knapsack)
        self.kp_layout.addWidget(self.solve_kp_btn)
        self.kp_results_label = QTextEdit()
        self.kp_results_label.setReadOnly(True)
        self.kp_layout.addWidget(self.kp_results_label)
        self.kp_layout.addWidget(self.back_button)


    def init_diet_layout(self):

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.go_back_to_selection)
        
        self.diet_layout = QVBoxLayout()
        self.calories_needed_input = QLineEdit(self)
        self.protein_needed_input = QLineEdit(self)
        self.fat_needed_input = QLineEdit(self)
        self.food_calories_input = QLineEdit(self)
        self.food_protein_input = QLineEdit(self)
        self.food_fat_input = QLineEdit(self)
        self.food_cost_input = QLineEdit(self)
        self.diet_layout.addWidget(QLabel("Calories Needed:"))
        self.diet_layout.addWidget(self.calories_needed_input)
        self.diet_layout.addWidget(QLabel("Protein Needed (grams):"))
        self.diet_layout.addWidget(self.protein_needed_input)
        self.diet_layout.addWidget(QLabel("Fat Needed (grams):"))
        self.diet_layout.addWidget(self.fat_needed_input)
        self.diet_layout.addWidget(QLabel("Food Calories (comma-separated):"))
        self.diet_layout.addWidget(self.food_calories_input)
        self.diet_layout.addWidget(QLabel("Food Protein (grams, comma-separated):"))
        self.diet_layout.addWidget(self.food_protein_input)
        self.diet_layout.addWidget(QLabel("Food Fat (grams, comma-separated):"))
        self.diet_layout.addWidget(self.food_fat_input)
        self.diet_layout.addWidget(QLabel("Food Cost (comma-separated):"))
        self.diet_layout.addWidget(self.food_cost_input)
        self.solve_diet_btn = QPushButton('XXXXXXXXX', self)
        self.solve_diet_btn.clicked.connect(self.solve_diet)
        self.diet_layout.addWidget(self.solve_diet_btn)
        self.diet_results_label = QTextEdit()
        self.diet_results_label.setReadOnly(True)
        self.diet_layout.addWidget(self.diet_results_label)
        self.diet_layout.addWidget(self.back_button)


    def display_selected_problem(self):
        index = self.problem_selector.currentIndex()
        if index == 0:  # Select Problem
            self.layout.removeItem(self.layout.itemAt(1))
            self.layout.removeItem(self.layout.itemAt(1))
        elif index == 1:  # Production Planning
                    # Initialize layouts
            self.init_production_planning_layout()
            self.back_button.show()  # Show back button on problem-solving screens
            self.layout.removeItem(self.layout.itemAt(1))
            self.layout.removeItem(self.layout.itemAt(1))
            self.layout.addLayout(self.pp_layout)
        elif index == 2:  # Knapsack Problem
            self.init_knapsack_layout()
            self.back_button.show()  # Show back button on problem-solving screens
            self.layout.removeItem(self.layout.itemAt(1))
            self.layout.removeItem(self.layout.itemAt(1))
            self.layout.addLayout(self.kp_layout)
        elif index == 3:  # Diet Problem
            self.init_diet_layout()
            self.back_button.show()  # Show back button on problem-solving screen
            self.layout.removeItem(self.layout.itemAt(1))
            self.layout.removeItem(self.layout.itemAt(1))
            self.layout.addLayout(self.diet_layout)

    def go_back_to_selection(self):
      current_index = self.problem_selector.currentIndex()
      if current_index == 1:
        self.delete_layout_widgets(self.pp_layout)
      elif current_index == 2:
        self.delete_layout_widgets(self.kp_layout)
      elif current_index == 3:
        self.delete_layout_widgets(self.diet_layout)
      self.problem_selector.setCurrentIndex(0)

    def delete_layout_widgets(self, layout):
        # Delete widgets within the layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                sublayout = item.layout()
                if sublayout:
                    self.delete_layout_widgets(sublayout)
                    
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
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OptimizationApp()
    ex.show()
    sys.exit(app.exec_())
