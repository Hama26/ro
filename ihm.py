from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QMessageBox, QTextEdit, QHBoxLayout, QComboBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from optimization_solver import solve_diet, solve_production_planning, solve_knapsack
import sys
from PyQt5.QtWidgets import QSpinBox

class OptimizationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window setup
        self.setWindowTitle("Optimization Solver")
        self.setGeometry(200, 200, 1000, 600)  # Increased height for better layout
        self.setFont(QFont("Arial", 10))
        self.setStyleSheet("QMainWindow { background-color: #f0f0f0; }"
                           "QPushButton { background-color: #0078d7; color: white; font-size: 11pt; border-radius: 5px; }"
                           "QPushButton:hover { background-color: #005fa3; }"
                           "QLabel, QLineEdit, QTextEdit, QComboBox { font-size: 10pt; }"
                           "QTextEdit { background-color: #ffffff; }"
                           "QLineEdit { border-radius: 3px; padding: 2px; background-color: #ffffff; }")

        # Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setSpacing(10)  # Spacing between widgets

        # ComboBox to select problem
        self.problem_selector = QComboBox(self)
        self.problem_selector.addItems(["Select Problem", "Production Planning", "Knapsack Problem", "Diet Problem"])
        self.problem_selector.currentIndexChanged.connect(self.display_selected_problem)
        self.layout.addWidget(self.problem_selector)

        # Common Back Button (used across different layouts)
        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.go_back_to_selection)
        self.back_button.hide()  # Initially hidden

    # Each init_*_layout method now includes the back button directly, and specific UI enhancements.

    def display_selected_problem(self):
        # Method modified to handle layouts more cleanly and ensure back button functionality.
        index = self.problem_selector.currentIndex()
        if index == 0:  # Select Problem
            self.clear_current_layout()
            self.problem_selector.show()
        else:
            self.problem_selector.hide()
            self.back_button.show()
            if index == 1:
                self.init_production_planning_layout()
            elif index == 2:
                self.init_knapsack_layout()
            elif index == 3:
                self.init_diet_layout()

    def clear_current_layout(self, keep_back_button=True,keep_selector=True):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
            # Check if the widget is the back button and if we should keep it
                if (widget == self.back_button and keep_back_button) or (widget == self.problem_selector and keep_selector):
                    widget.hide()  # Hide it instead of deleting
                else:
                    widget.deleteLater()
            else:
                layout = item.layout()
                if layout:
                    self.clear_layout(layout)


    def init_production_planning_layout(self):
        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.go_back_to_selection)
    # Clear the layout
        self.clear_current_layout()

        self.pp_layout = QVBoxLayout()

    # SpinBox to select the number of products
        self.pp_layout.addWidget(QLabel("Number of Products:"))
        self.num_products_spinbox = QSpinBox(self)
        self.num_products_spinbox.setMinimum(1)
        self.num_products_spinbox.setMaximum(4)
        self.num_products_spinbox.valueChanged.connect(self.update_product_inputs)
        self.pp_layout.addWidget(self.num_products_spinbox)

    # Container for product inputs
        self.product_inputs = []
        self.products_layout = QVBoxLayout()
        self.pp_layout.addLayout(self.products_layout)
     # Add inputs for total labor and materials available
        self.pp_layout.addWidget(QLabel("Total Labor Available (hours):"))
        self.total_labor_input = QLineEdit(self)
        self.total_labor_input.setPlaceholderText("Enter total available labor hours")
        self.pp_layout.addWidget(self.total_labor_input)

        self.pp_layout.addWidget(QLabel("Total Materials Available (units):"))
        self.total_material_input = QLineEdit(self)
        self.total_material_input.setPlaceholderText("Enter total available material units")
        self.pp_layout.addWidget(self.total_material_input)
    # Initial setup for product inputs
        self.update_product_inputs(1)

    # Button to solve the production planning problem
        self.solve_pp_btn = QPushButton('Solve Production Planning', self)
        self.solve_pp_btn.clicked.connect(self.solve_production_planning)
        self.pp_layout.addWidget(self.solve_pp_btn)

    # Results display
        self.pp_results_label = QTextEdit()
        self.pp_results_label.setReadOnly(True)
        self.pp_layout.addWidget(self.pp_results_label)

    # Back button
        self.pp_layout.addWidget(self.back_button)
        self.back_button.show()
        self.central_widget.setLayout(self.pp_layout)
    
    def update_product_inputs(self, num_products):
    # Calculate the current count of product layouts in the products_layout
        current_count = len(self.product_inputs)

    # Remove excess widgets if current count is greater than required
        if current_count > num_products:
            for i in range(current_count - 1, num_products - 1, -1):  # Iterate backwards to remove from the end
            # Retrieve and delete each widget in the layout
                layout_to_remove = self.products_layout.itemAt(i).layout()
                while layout_to_remove.count():
                    item = layout_to_remove.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()

            # Remove the layout from the products_layout and delete it
                layout_item = self.products_layout.takeAt(i)
                if layout_item.layout() is not None:
                    layout_item.layout().deleteLater()
            
            # Remove the tuple from product_inputs
                self.product_inputs.pop(i)

    # Add new widgets if the current count is less than the required number
        if current_count < num_products:
            for i in range(current_count, num_products):
                product_layout = QHBoxLayout()

                name_input = QLineEdit(self)
                name_input.setPlaceholderText("Enter product name")
                labor_input = QLineEdit(self)
                labor_input.setPlaceholderText("Enter labor required(hours)")
                material_input = QLineEdit(self)
                material_input.setPlaceholderText("Enter materials required(units)")
                profit_input = QLineEdit(self)
                profit_input.setPlaceholderText("Enter profit(per unit)")
                min_production_input = QLineEdit(self)
                min_production_input.setPlaceholderText("Enter minimum production")

                product_layout.addWidget(QLabel(f"Product {i + 1} Name:"))
                product_layout.addWidget(name_input)
                product_layout.addWidget(QLabel("Labor:"))
                product_layout.addWidget(labor_input)
                product_layout.addWidget(QLabel("Material:"))
                product_layout.addWidget(material_input)
                product_layout.addWidget(QLabel("Profit:"))
                product_layout.addWidget(profit_input)
                product_layout.addWidget(QLabel("Minimum Production:"))
                product_layout.addWidget(min_production_input)

                self.products_layout.addLayout(product_layout)
                self.product_inputs.append((name_input, labor_input, material_input, profit_input,min_production_input))




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
        self.solve_diet_btn = QPushButton('Solve Diet Problem', self)
        self.solve_diet_btn.clicked.connect(self.solve_diet)
        self.diet_layout.addWidget(self.solve_diet_btn)
        self.diet_results_label = QTextEdit()
        self.diet_results_label.setReadOnly(True)
        self.diet_layout.addWidget(self.diet_results_label)
        self.diet_layout.addWidget(self.back_button)


    def display_selected_problem(self):
        index = self.problem_selector.currentIndex()
        if index == 0:  # Select Problem
            self.problem_selector.show()
            self.layout.removeItem(self.layout.itemAt(1))
            self.layout.removeItem(self.layout.itemAt(1))
        elif index == 1:  # Production Planning
                    # Initialize layouts
            self.problem_selector.hide()
            self.init_production_planning_layout()
            self.back_button.show()  # Show back button on problem-solving screens
            self.layout.removeItem(self.layout.itemAt(1))
            self.layout.removeItem(self.layout.itemAt(1))
            self.layout.addLayout(self.pp_layout)
        elif index == 2:  # Knapsack Problem
            self.problem_selector.hide()
            self.init_knapsack_layout()
            self.back_button.show()  # Show back button on problem-solving screens
            self.layout.removeItem(self.layout.itemAt(1))
            self.layout.removeItem(self.layout.itemAt(1))
            self.layout.addLayout(self.kp_layout)
        elif index == 3:  # Diet Problem
            self.problem_selector.hide()
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
        # Convert input text to floats and validate
            total_labor_avail = float(self.total_labor_input.text().strip())
            total_materials_avail = float(self.total_material_input.text().strip())
            products = []

            for name_input, labor_input, material_input, profit_input,min_production_input in self.product_inputs:
                name = name_input.text().strip()
                labor = float(labor_input.text().strip())
                material = float(material_input.text().strip())
                profit = float(profit_input.text().strip())
                min_production =float(min_production_input.text().strip())
            
                products.append({'name': name, 'labor': labor, 'materials': material, 'profit': profit, 'min_production': min_production})

        # Call backend solver
            result = solve_production_planning(total_labor_avail, total_materials_avail, products)

            if result:
            # Format and display results
                result_message = "Optimal Production Levels:\n"
                for varName, quantity in result['production_levels'].items():
                    result_message += f"{varName}: {quantity:.0f} units\n"  # Format for integer quantities
                result_message += f"Total Profit: ${result['total_profit']:.2f}"
                self.pp_results_label.setText(result_message)
            else:
                QMessageBox.warning(self, "Solution Error", "No feasible solution was found.")

        except ValueError as e:
            QMessageBox.warning(self, "Input Error", f"Please enter valid numbers. Error: {str(e)}")


    def solve_knapsack(self):
        try:
            capacity = int(self.capacity_input.text())
            if capacity < 0:
                raise ValueError("Capacity must be non-negative.")
            values = list(map(int, self.values_input.text().split(',')))
            weights = list(map(int, self.weights_input.text().split(',')))
            if any(v < 0 for v in values) or any(w < 0 for w in weights):
                raise ValueError("Values and weights must be non-negative.")
            selected_items, total_value = solve_knapsack(capacity, values, weights)
            item_display = ", ".join(f"Item {i+1}" for i in selected_items)
            self.kp_results_label.setText(f"Selected Items: {item_display}\nTotal Value: ${total_value:.2f}")
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))


    
    def solve_diet(self):
        try:
            calories_needed = float(self.calories_needed_input.text())
            protein_needed = float(self.protein_needed_input.text())
            fat_needed = float(self.fat_needed_input.text())
            if calories_needed < 0 or protein_needed < 0 or fat_needed < 0:
                raise ValueError("Nutritional needs must be non-negative.")
            food_calories = list(map(float, self.food_calories_input.text().split(',')))
            food_protein = list(map(float, self.food_protein_input.text().split(',')))
            food_fat = list(map(float, self.food_fat_input.text().split(',')))
            food_cost = list(map(float, self.food_cost_input.text().split(',')))
            if any(f < 0 for f in food_calories + food_protein + food_fat + food_cost):
                raise ValueError("Food data must be non-negative.")
            optimal_quantities, total_cost = solve_diet(calories_needed, protein_needed, fat_needed, food_calories, food_protein, food_fat, food_cost)
            food_names = ["Food {}".format(i+1) for i in range(len(optimal_quantities))]
            food_list = [f"{food_names[i]}: {optimal_quantities[i]:.2f} units" for i in range(len(optimal_quantities)) if optimal_quantities[i] > 0]
            food_display = "\n".join(food_list)
            self.diet_results_label.setText(f"Selected Foods:\n{food_display}\nTotal Cost: ${total_cost:.2f}")
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OptimizationApp()
    ex.show()
    sys.exit(app.exec_())