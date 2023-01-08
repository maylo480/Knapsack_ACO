# C = knapsack_capacity
# W = weight of object
# P = profit of object
# S = subset of objects put into the knapsack

# W >= C
# Total weight cannot exceed capacity
# We'd like to maximize total profit

from antsys import AntWorld
from antsys import AntSystem
import numpy as np
import os
import argparse

samples_path = os.path.abspath("/home/kaszo5/Documents/Knapsack_ACO/Samples")
knapsack_capacity, knapsack_weights, knapsack_profits = [], [], []
items, res, outcome_weights, subset = [], [], [], []

def get_knapsack_capacity(sample):
    with open(os.path.join(samples_path, f"{sample}/capacity.txt")) as f:
        knapsack_capacity = f.read()
        return knapsack_capacity

def get_knapsack_weights(sample):
    with open(os.path.join(samples_path, f"{sample}/weights.txt")) as f:
        lines = f.readlines()
        for i in lines:
            knapsack_weights.append(int(i))
        return knapsack_weights

def get_knapsack_profits(sample):
    with open(os.path.join(samples_path, f"{sample}/profits.txt")) as f:
        lines = f.readlines()
        for i in lines:
            knapsack_profits.append(int(i))
        return knapsack_profits

def format_knapsack_items(knapsack_weights, knapsack_profits):
    for i in range(len(knapsack_weights)):
        items.append((i, knapsack_weights[i], knapsack_profits[i]))
    return items
    
def show_knapsack_params(capacity, weights, profits):
    print(f"knapsack_capacity = {capacity}")
    print(f"items_weights     = {weights}")
    print(f"items_profits     = {profits}")
    print("\n")

def knapsack_rules(start, end):
    return[0, 1]

def knapsack_cost(path):
    k_value = 0
    k_weight = 0
    for edge in path:
        if edge.info == 1:
            k_value += edge.end[2]
            k_weight += edge.end[1]
    cost = 5/k_value+1/k_weight
    if k_weight > knapsack_capacity:
        cost += 1
    else:
        for edge in path:
            if edge.info == 0 and edge.end[1] <= (knapsack_capacity-k_weight):
                cost += 1
    return cost

def knapsack_heuristic(path, candidate):
    k_weight = 0
    for edge in path:
        if edge.info == 1:
            k_weight += edge.end[1]
    if candidate.info == 1 and candidate.end[1] < (knapsack_capacity-k_weight):
        return 0
    elif candidate.info == 0:
        return 1
    else:
        return 2

def print_solution(path):
    value = 0
    weight = 0
    for edge in path:
        if(edge.info == 1):
            res.append(edge.end)
            value += edge.end[2]
            weight += edge.end[1]
    print(f"Total value of items in knapsack = {value}\n")
    return res

def get_subset(outcome):
    sum = 0
    for tuple in outcome:
        outcome_weights.append(tuple[1])
    
    for weight in outcome_weights:
        sum += weight
    print(f"Knapsack total capacity = {knapsack_capacity}") 
    print(f"Sum of all items weight = {sum}") 

    for weight in knapsack_weights:
        if weight in outcome_weights:
            subset.append(1)
        else:
            subset.append(0)
    return subset

def save_subset(subset, sample):
    with open(f"Results/result{sample}.txt", "w") as f:
        for el in subset:
            f.write(str(el))
            f.write("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("benchmark", help="name of the benchmark to run ACO on")
    args = parser.parse_args()
    sample = args.benchmark

    knapsack_capacity = int(get_knapsack_capacity(sample))
    knapsack_weights = (get_knapsack_weights(sample))
    knapsack_profits = (get_knapsack_profits(sample))
    items = format_knapsack_items(knapsack_weights, knapsack_profits)

    new_world = AntWorld(items, knapsack_rules, knapsack_cost, knapsack_heuristic, complete=False)
    ant_opt = AntSystem(world=new_world, n_ants=500)
    ant_opt.optimize(max_iter=1000)
    print("\n")

    outcome = print_solution(ant_opt.g_best[2])

    subset = get_subset(outcome)
    save_subset(subset, sample)
