from gurobipy import Model, GRB

def solve_diet(calories_needed, protein_needed, fat_needed, food_calories, food_protein, food_fat, food_cost):
  """
  This function solves a diet optimization problem.

  Args:
      calories_needed: The number of calories needed per day.
      protein_needed: The amount of protein needed per day.
      fat_needed: The amount of fat needed per day.
      food_calories: A list of calorie content per unit of food.
      food_protein: A list of protein content per unit of food.
      food_fat: A list of fat content per unit of food.
      food_cost: A list of cost per unit of food.

  Returns:
      A tuple containing:
          - A list of amount to consume for each food item (decision variables).
          - The total cost of the diet (objective function).
  """
  m = Model("diet")

  # Decision variables
  food_count = len(food_calories)
  x = m.addVars(food_count, lb=0, vtype=GRB.INTEGER, name="x")  # Enforce non-negative integer amounts

  # Objective function (Minimize total cost)
  m.setObjective(sum(food_cost[i] * x[i] for i in range(food_count)), GRB.MINIMIZE)

  # Constraints
  m.addConstr(sum(food_calories[i] * x[i] for i in range(food_count)) >= calories_needed, "Calories")
  m.addConstr(sum(food_protein[i] * x[i] for i in range(food_count)) >= protein_needed, "Protein")
  m.addConstr(sum(food_fat[i] * x[i] for i in range(food_count)) >= fat_needed, "Fat")

  # Solve model
  m.optimize()

  if m.status == GRB.OPTIMAL:
    return [x[i].X for i in range(food_count)], m.objVal
  else:
    return [0] * food_count, 0
  
def solve_production_planning(labor_available, materials_available):
  """
  This function solves a production planning problem to maximize total profit,
  considering labor and material constraints.

  Args:
      labor_available: The total amount of labor available for production (e.g., hours).
      materials_available: The total amount of materials available for production (e.g., units).

  Returns:
      A tuple containing:
          - A tuple with the optimal production quantities for product 1 (P1) and product 2 (P2).
          - The total profit achieved with this production plan.
          - The time taken by Gurobi to solve the model (in seconds).
  """

  # Create a Gurobi model instance named "production_planning"
  m = Model("production_planning")

  # Define decision variables
  #   - p1: Production quantity for product 1 (continuous variable)
  #   - p2: Production quantity for product 2 (continuous variable)
  p1 = m.addVar(name="P1")
  p2 = m.addVar(name="P2")

  # Define the objective function to maximize total profit
  #   - Profit per unit of product 1 = 20
  #   - Profit per unit of product 2 = 30
  m.setObjective(20 * p1 + 30 * p2, GRB.MAXIMIZE)

  # Define constraints
  #   - Labor constraint: Total labor required for production <= available labor
  #     - Each unit of P1 requires 2 units of labor.
  #     - Each unit of P2 requires 3 units of labor.
  m.addConstr(2 * p1 + 3 * p2 <= labor_available, "Labor")

  #   - Material constraint: Total materials required for production <= available materials
  #     - Each unit of P1 requires 3 units of material.
  #     - Each unit of P2 requires 2 units of material.
  m.addConstr(3 * p1 + 2 * p2 <= materials_available, "Materials")

  # Solve the model using Gurobi optimizer
  m.optimize()

  # Check if the solution is optimal (GRB.OPTIMAL status code)
  if m.status == GRB.OPTIMAL:
    # Extract optimal production quantities and total profit
    return (p1.X, p2.X), m.objVal, m.Runtime
  else:
    # If not optimal, return 0 for all values
    return (0, 0), 0


def solve_knapsack(capacity, values, weights):
    """
    This function solves a knapsack problem to maximize the total value of items,
    considering a weight constraint on the knapsack.

    Args:
        capacity: The maximum weight capacity of the knapsack.
        values: A list representing the value of each item.
        weights: A list representing the weight of each item.

    Returns:
        A tuple containing:
            - A list of indices representing the selected items to put in the knapsack.
            - The total value of the selected items.
            - The time taken by Gurobi to solve the model (in seconds).
    """
    # Create a Gurobi model instance named "knapsack"
    m = Model("knapsack")

    # Define the number of items based on the length of the values and weights lists
    item_count = len(values)

    # Define decision variables (x) as binary variables (0 or 1)
    #   - x[i] = 1 if item i is selected, 0 otherwise
    x = m.addVars(item_count, vtype=GRB.BINARY, name="x")

    # Define the objective function to maximize the total value of selected items
    m.setObjective(sum(values[i] * x[i] for i in range(item_count)), GRB.MAXIMIZE)

    # Define constraint: Total weight of selected items <= knapsack capacity
    #   - Each item i has weight weights[i].
    m.addConstr(sum(weights[i] * x[i] for i in range(item_count)) <= capacity, "Capacity")

    # Solve the model using Gurobi optimizer
    m.optimize()
    
    # Check if the solution is optimal (GRB.OPTIMAL status code)
    if m.status == GRB.OPTIMAL:
        # Extract indices of selected items (where x[i] is greater than 0.5 to account for rounding errors)
        selected_items = [i for i in range(item_count) if x[i].X > 0.5]
        # Return selected items, total value, and solution time
        return selected_items, m.objVal, m.Runtime
    else:
        # If not optimal, return empty list and 0 for all values
        return [], 0
