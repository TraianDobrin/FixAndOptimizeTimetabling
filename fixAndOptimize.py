import subprocess
import re
import numpy as np
from itertools import combinations
import math
from pysat.formula import WCNF

def n_choose_k(n, k):
    """
    Calculate the binomial coefficient C(n, k).

    Parameters:
    n (int): The total number of items.
    k (int): The number of items to choose.

    Returns:
    int: The binomial coefficient C(n, k).
    """
    if k > n or n < 0 or k < 0:
        return 0
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))
def evaluate(x,timeout):
    # Define the path to the instance file
    path_to_instance = r"C:\Users\Traian\Documents\GitHub\Timetabling-problem\encoding.dimacs"
    wcnf=WCNF(path_to_instance)
    for v in x:
        wcnf.append([v])

    path_to_formula=r"..\..\PycharmProjects\tentativa\current_formulab1.wcnf"
    with open("current_formulab1.wcnf", 'w') as file:
        # Write the header line
        file.write(wcnf.to_dimacs())

    # " | findstr /R /C:\"v..\(.*\)\"" +
    print("era lenx")
    command = r"cd ..\..\Pumpkin\pumpkin-private && target\release\pumpkin-cli.exe -t " + str(timeout) + " " + path_to_formula + " > " + r"..\..\PycharmProjects\tentativa\capture_sol.txt"

    starting_directory = r"C:"

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True, cwd="C:")
    process.wait()
    last_o_number = 1000000000
    print("done")
    output=[]
    with open("capture_sol.txt", "r") as file:
        for line in file:
            # Check if the line starts with 'o'
            if line.startswith("o"):
                # Split the line into individual elements
                elements = line.split()
                try:
                    # Attempt to convert the second element to an integer and store it
                    last_o_number = int(elements[1])
                except (IndexError, ValueError):
                    # Handle the case where the element is not found or not an integer
                    print(f"Skipping invalid 'o' line: {line.strip()}")
    return last_o_number
def read_numbers_from_file(file_path="capture_sol.txt"):
    numbers = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Split the line by whitespace and convert each part to a number
                # Assuming each line contains numbers separated by spaces
                for part in line.split():
                    numbers.append((int((part))))  # Use int(part) if you want integers
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except ValueError:
        print("File contains non-numeric data.")
    return numbers
def read_file_with_signs(file_path):
    dict={}
    with open(file_path, 'r') as file:
        for line in file:
        # Read the first line from the file
            linee = line.strip()
            #print(linee)
            # Check if the line starts with 'v'
            if linee.startswith('v'):
                # Split the line by spaces and skip the first element ('v')
                numbers_str = line.split()[1:]

                # Convert the remaining elements to integers
                for num  in numbers_str:
                    dict[abs(int(num))]=int(num)
                return dict
k=1
solution=read_numbers_from_file("sol.txt")
initnr=len(solution)
no_change=0
ind_perm=0
ind=0
arr=range(int(len(solution)/25))
subsets=[list(combination) for combination in combinations(arr, k)]
#print(solution)
cost=evaluate(solution,100000)
#print(len(solution))
print(cost)

while k<=len(arr):
    print((ind_perm))
    print(no_change)
    arr=subsets[ind_perm]
    #print(subsets)
    curr_sol=[]
    ind=0
    #print(arr)
    for i in range(int(initnr/25)):
        if i not in arr:
            for j in range(25):
#                 print(len(solution))
#                 print(ind)
#                 print(solution[ind])
                curr_sol.append(solution[ind])
                ind+=1
        else:
            ind+=25
    #print(curr_sol)
    with open("solution_memory.txt", 'w') as f:
        for item in curr_sol:
            f.write(str(item) + ' ')
    curr_cost=evaluate(curr_sol,20000)
    print(cost)
    if curr_cost<cost:
        cost=curr_cost
        ind=0
        dict=read_file_with_signs("capture_sol.txt")
        with open("best assignment.txt", 'w') as f:
            for item in curr_sol:
                f.write(str(item) + ' ')
        #print(dict)
        curr_sol=[]
        for x in solution:
            curr_sol.append(dict[abs(x)])
        solution=curr_sol
        #print(solution)
        no_change=0
        ind_perm=-1
    else:
        no_change+=1
    if no_change==n_choose_k(int(initnr/25), k):
        k+=1
        arr=range(int(len(solution)/25))
        subsets=[list(combination) for combination in combinations(arr, k)]
        ind_perm=0
        no_change=0
    else:
        ind_perm+=1