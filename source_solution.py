import argparse
import os

samples_path = os.path.abspath("/home/kaszo5/Documents/Knapsack_ACO/Samples")

def read_subset(sample):
    subset = []
    with open(f"{samples_path}/{sample}/subset.txt") as f:
        for line in f:
            subset.append(int(line))
    return subset

def read_weights(sample):
    weights = []
    with open(f"{samples_path}/{sample}/weights.txt") as f:
        for line in f:
            weights.append(int(line))
    return weights

def read_profits(sample):
    profits = []
    with open(f"{samples_path}/{sample}/profits.txt") as f:
        for line in f:
            profits.append(int(line))
    return profits

def sum_profits(subset, profits, weights):
    sum_of_profits = 0
    sum_of_weights = 0
    j = 0
    for i in subset:
        if i == 1:
            sum_of_profits += profits[j]
            sum_of_weights += weights[j]
        j += 1
    return sum_of_profits, sum_of_weights

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("benchmark", help="name of the benchmark to run ACO on")
    args = parser.parse_args()
    sample = args.benchmark

    res_subset = read_subset(sample)
    res_weights = read_weights(sample)
    res_profits = read_profits(sample)
    print(f"Subset  = {res_subset}")
    print(f"Weights = {res_weights}")
    print(f"Profit  = {res_profits}")

    sum_of_profits, sum_of_weights = sum_profits(res_subset, res_profits, res_weights)
    print(f"\nSum of profits = {sum_of_profits}\nSum of weights = {sum_of_weights}")
