#!/usr/bin/env python3

import pulp
from pulp import LpMinimize, LpProblem, LpVariable

# Data
instructions = ["i1", "i2", "i3", "i4"]
dependencies = []
add_instructions = ["i1", "i3"]  # i1 and i3 are add
mul_instructions = ["i2", "i4"]  # i2 and i4 are mul

# Variables
s = {i: LpVariable(f"s_{i}", lowBound=0, cat="Integer") for i in instructions}
makespan = LpVariable("makespan", lowBound=0, cat="Integer")

# Problem definition
problem = LpProblem("Instruction_Scheduling", LpMinimize)
problem += makespan  # Objective: Minimize makespan

# Dependency constraints
# for i, j in dependencies:
# problem += s[j] >= s[i] + 2  # Dependency plus data transfer time

# Makespan constraints
for i in instructions:
    problem += s[i] + 1 <= makespan  # 1 cycle execution time

# Execution unit constraints
# for t in range(0, len(instructions)):  # Time range guess
# problem += lpSum([1 if s[i] == t else 0 for i in add_instructions]) <= 1
# problem += lpSum([1 if s[i] == t else 0 for i in mul_instructions]) <= 1

# Solve
print(problem)
solver = pulp.HiGHS_CMD(msg=True, warmStart=True)
# solver = pulp.GLPK_CMD(msg=True)
# solver = pulp.PULP_CBC_CMD(msg=True, warmStart=True)
# solver = pulp.COIN_CMD(msg=True, warmStart=True)
problem.solve(solver)
print(problem)
# problem.solve()

# Output results
print(f"Makespan: {makespan.varValue}")
for i in instructions:
    print(f"Start time of {i}: {s[i].varValue}")
