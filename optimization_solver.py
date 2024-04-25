from gurobipy import Model, GRB

def solve_production_planning(labor_available, materials_available):
    m = Model("production_planning")

    # Decision variables
    p1 = m.addVar(name="P1")
    p2 = m.addVar(name="P2")

    # Objective function
    m.setObjective(20 * p1 + 30 * p2, GRB.MAXIMIZE)

    # Constraints
    m.addConstr(2 * p1 + 3 * p2 <= labor_available, "Labor")
    m.addConstr(3 * p1 + 2 * p2 <= materials_available, "Materials")

    # Solve model
    m.optimize()

    if m.status == GRB.OPTIMAL:
        return (p1.X, p2.X), m.objVal
    else:
        return (0, 0), 0

def solve_knapsack(capacity, values, weights):
    m = Model("knapsack")

    # Decision variables
    item_count = len(values)
    x = m.addVars(item_count, vtype=GRB.BINARY, name="x")

    # Objective function
    m.setObjective(sum(values[i] * x[i] for i in range(item_count)), GRB.MAXIMIZE)

    # Constraint
    m.addConstr(sum(weights[i] * x[i] for i in range(item_count)) <= capacity, "Capacity")

    # Solve model
    m.optimize()

    if m.status == GRB.OPTIMAL:
        selected_items = [i for i in range(item_count) if x[i].X > 0.5]
        return selected_items, m.objVal
    else:
        return [], 0
