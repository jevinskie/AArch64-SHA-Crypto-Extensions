#!/usr/bin/env python3

import pulp
from pulp import LpBinary, LpMinimize, LpProblem, LpVariable, lpSum

# Data
instructions = ["i1", "i2", "i3", "i4"]
durations = {"i1": 2, "i2": 3, "i3": 1, "i4": 4}
dependencies = [("i1", "i2"), ("i1", "i3"), ("i2", "i4")]
M = 2  # Number of execution units

# Variables
start = {i: LpVariable(f"start_{i}", 0, cat="Integer") for i in instructions}
unit = {(i, j): LpVariable(f"unit_{i}_{j}", 0, 1, LpBinary) for i in instructions for j in range(M)}
makespan = LpVariable("makespan", 0, cat="Integer")

# Problem definition
problem = LpProblem("Instruction_Scheduling", LpMinimize)

# Objective: Minimize makespan
problem += makespan

# Dependency constraints
for i1, i2 in dependencies:
    problem += start[i2] >= start[i1] + durations[i1]

# Unit assignment constraint: Each instruction assigned to exactly one unit
for i in instructions:
    problem += lpSum(unit[i, j] for j in range(M)) == 1

# Non-overlapping constraints: Instructions on the same unit cannot overlap
for i1 in instructions:
    for i2 in instructions:
        if i1 != i2:
            for j in range(M):
                problem += (
                    start[i1] + durations[i1] <= start[i2] + (1 - unit[i1, j] - unit[i2, j]) * 1000
                )
                problem += (
                    start[i2] + durations[i2] <= start[i1] + (1 - unit[i1, j] - unit[i2, j]) * 1000
                )

# Makespan constraints
for i in instructions:
    problem += makespan >= start[i] + durations[i]

solver = pulp.HiGHS_CMD(msg=True, warmStart=True)
# Solve
problem.solve(solver)

# Output results
print(f"Makespan: {makespan.varValue}")
for i in instructions:
    print(f"Start time of {i}: {start[i].varValue}")
    for j in range(M):
        if unit[i, j].varValue == 1:
            print(f"  Assigned to unit {j}")
