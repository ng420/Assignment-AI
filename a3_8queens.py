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

def num_non_attack(board):
    n = len(eval(board))
    total = (n * (n - 1)) / 2
    return total - num_attack(board)

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

def genetic_algorithm(population):
    def random_selection(population):
        max = sum(num_non_attack(individual) for individual in population)
        pick = random.uniform(0, max)
        current = 0
        for individual in population:
            current += num_non_attack(individual)
            if current > pick:
                return individual

    def reproduce(x, y):
        xm = eval(x)
        ym = eval(y)
        n = len(xm)
        i = random.randint(1, n - 1)
        return str(xm[:i] + ym[i:])

    def mutate(board):
        matrix = eval(board)
        n = len(matrix)
        col = random.randint(0, n - 1)
        row = random.randint(0, n - 1)
        matrix[col] = row
        return str(matrix)

    # print population
    prob_mutation = 0.005
    bestboard = max(population, key = lambda x: num_non_attack(x))
    bestvalue = num_non_attack(bestboard)
    for itr in range(100):
        new_population = []
        # print itr
        for i in range(len(population)):
            x = random_selection(population)
            y = random_selection(population)
            child = reproduce(x, y)
            if prob_mutation > random.random():
                child = mutate(child)
            new_population.append(child)
        population = new_population
        best = max(population, key = lambda x: num_non_attack(x))
        if num_non_attack(best) > bestvalue:
            bestvalue, bestboard = num_non_attack(best), best
        if num_attack(bestboard) == 0:
            return bestboard, 0
    return bestboard, num_attack(bestboard)

# print successors(str([0, 0, 0]))
# print num_attack(str([0, 1, 1]))
b = random_board(8)
# print b
# print random_restart_hill_climbing(b)
# print simulated_annealing(b)
print genetic_algorithm([random_board(8) for i in range(10)])