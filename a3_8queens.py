import random
from math import exp

def successors(board):
    out = []
    m = eval(board)
    n = len(m)
    for i in range(n):
        temp = m[i]
        for j in range(n):
            if m[i] != j:
                m[i] = j
                out.append(str(m))
        m[i] = temp
    return out

def random_board(n):
    return str([random.randint(0, n-1) for i in range(n)])

def num_attack(board):
    m = eval(board)
    r = 0
    dx = [-1, -1, -1, 0, 0, 1, 1, 1]
    dy = [-1, 0, 1, -1, 1, -1, 0, 1]
    for i in range(len(m)):
        for j in range(1, len(m)):
            for k in range(len(dx)):
                if i + (j * dx[k]) >= 0 and i + (j * dx[k]) < len(m) and m[i] + (j * dy[k]) >= 0 and m[i] + (j * dy[k]) < len(m) and m[i + (j * dx[k])] == m[i] + (j * dy[k]):
                    r += 1
    return r / 2

def random_restart_hill_climbing(board):
    bestvalue = num_attack(board)
    bestboard = board
    for i in range(1000):
        solution, value = hill_climbing(board)
        if value == 0:
            return solution, 0, i
        if value < bestvalue:
            bestvalue = value
            bestboard = board
        board = random_board(len(eval(board)))
    return bestboard, bestvalue, 1000

def hill_climbing(state):
    while True:
        neighbour = min(successors(state), key = lambda x : num_attack(x))
        if num_attack(state) <= num_attack(neighbour):
            return state, num_attack(state)
        state = neighbour

def simulated_annealing(state):
    kmax = 5000
    for k in range(1, kmax):
        T = float(k) / kmax
        snew = random.choice(successors(state))
        dE = num_attack(state) - num_attack(snew)
        if dE > 0 or exp(dE / T) > random.random():
            state = snew
    return state, num_attack(state)

# print successors(str([0, 0, 0]))
# print num_attack(str([0, 1, 1]))
b = random_board(8)
print b
print random_restart_hill_climbing(b)
print simulated_annealing(b)