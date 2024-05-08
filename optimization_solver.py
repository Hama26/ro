from gurobipy import Model, GRB
from gurobipy import quicksum

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
  
def solve_production_planning(labor_avail, materials_avail, products):
    """
    Solves a  production planning problem focusing on maximizing profit with basic labor and material constraints.

    Parameters:
    - labor_avail (float): Total available labor hours.
    - materials_avail (float): Total available material units.
    - products (list of dicts): Information about each product, including profit, labor requirement, and material requirement.

    Returns:
    - A dictionary with production levels and the total profit.
    """
    m = Model("Simplified Production Planning")

    # Decision variables for production levels of each product
    x = {p['name']: m.addVar(vtype=GRB.INTEGER, name=f"prod_{p['name']}") for p in products}

    # Objective: Maximize profit
    m.setObjective(quicksum(p['profit'] * x[p['name']] for p in products), GRB.MAXIMIZE)

    # Constraints
    # Labor constraint
    m.addConstr(quicksum(p['labor'] * x[p['name']] for p in products) <= labor_avail, "Labor")

    # Material constraint
    m.addConstr(quicksum(p['materials'] * x[p['name']] for p in products) <= materials_avail, "Materials")

    # Minimum production requirements
    for p in products:
        m.addConstr(x[p['name']] >= p['min_production'], f"MinProd_{p['name']}")
    
    # Solve model
    m.optimize()

    # Extract solution
    if m.status == GRB.OPTIMAL:
        production_levels = {v.varName: v.x for v in m.getVars()}
        total_profit = m.getObjective().getValue()
        return {
            'production_levels': production_levels,
            'total_profit': total_profit
        }
    else:
        return None


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
    