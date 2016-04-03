import heapq, random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

H = 4
B = 4

def successors(puzzle):
    matrix = eval(puzzle)
    zx = 0
    while 0 not in matrix[zx]:
        zx += 1
    zy = matrix[zx].index(0)

    ret = []
    # up, down, left, right
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    for i in range(4):
        if zx + dx[i] >= 0 and zx + dx[i] < H and zy + dy[i] >= 0 and zy + dy[i] < B:
            matrix[zx][zy], matrix[zx + dx[i]][zy + dy[i]] = matrix[zx + dx[i]][zy + dy[i]], matrix[zx][zy]
            ret.append(str(matrix))
            matrix[zx + dx[i]][zy + dy[i]], matrix[zx][zy] = matrix[zx][zy], matrix[zx + dx[i]][zy + dy[i]]
    
    return ret

def random_board(goal):
    # generate random number of moves
    num_moves = random.randint(10, 40)
    board = goal
    for i in range(num_moves):
        board = random.choice(successors(board))
    return board

def astar(start, goal, h):
    frontier = []
    heapq.heappush(frontier, (h(start), h(start), start))
    extended_list = set()
    generated_node_count = 0 
    while frontier: 
        fval, hval, front = heapq.heappop(frontier)
        depth = fval - hval
        #print front
        if front == goal:
            return (depth, generated_node_count)
        if front in extended_list:
            continue

        extended_list.add(front) 
        for state in successors(front):
            generated_node_count += 1
            if state in extended_list: 
                continue
            newh = h(state)
            heapq.heappush(frontier, (depth + 1 + newh, newh, state))
    return (-1, generated_node_count)

def ida_star(root, goal, h):
    bound = h(root)
    nodes_generated = 0
    while True:
        # print bound
        t, n = search(root, goal, 0, bound, h)
        nodes_generated += n
        if t == -1:
            return bound, nodes_generated
        if t == float('inf'):
            return inf, nodes_generated
        bound = t
 
def search(node, goal, g, bound, h):
    nodes_generated = 0
    f = g + h(node)
    if f > bound:
        return f, 0
    if node == goal:
        return -1, 0
    min = float('inf')
    for succ in successors(node):
        t, n = search(succ, goal, g + 1, bound, h)
        nodes_generated += n + 1
        if t == -1:
            return (-1, nodes_generated)
        if t < min:
            min = t
    return (min, nodes_generated)

def man_dist(puzz):
    d = 0
    m = eval(puzz)          
    for i in range(4):
        for j in range(4):
            if m[i][j] == 0: continue
            d += abs(i - (m[i][j] / 4)) + abs(j -  (m[i][j] % 4));
    return d

def rbfs(start, goal, h):
    ok, fval, gen_count = _rbfs(start, goal, 0, h(start), float('inf'), h)
    return fval, gen_count

def _rbfs(node, goal, gval, fval, bound, h):
    if node == goal:
        return True, gval, 0
    nodes_generated = 0
    fs = {}
    for state in successors(node):
        fs[state] = max(gval + 1 + h(state), fval)
        nodes_generated += 1
    while True:
        sort_fs = sorted(fs.keys(), key = fs.get)
        best = sort_fs[0]
        if fs[best] > bound: 
            return False, fs[best], nodes_generated
        alt = fs[sort_fs[1]]
        new_bound = min(bound, alt)
        result, fs[best], n = _rbfs(best, goal, gval + 1, fs[best], new_bound, h)
        nodes_generated += n
        if result != False:
            return result, fs[best], nodes_generated

def plot(data1, data2):
    x1, y1 = zip(*data1)
    x2, y2 = zip(*data2)
    blue_patch = mpatches.Patch(color='blue', label='RBFS')
    green_patch = mpatches.Patch(color='green', label='IDA*')
    plt.legend(bbox_to_anchor=(1, 1), handles=[blue_patch, green_patch])
    plt.plot(x1, y1, 'bs', x2, y2, 'g^')
    plt.show()

def bad_h(board):
    h = man_dist(board)
    v = min(h, 28 - h) # h * h - 24 * h + 144
    return v

if __name__ == '__main__':
    ### a few test boards with known answers
    # puzzle = str([[1, 2, 6, 3], [4, 9, 5, 7], [8, 13, 11, 15], [12, 14, 0, 10]])
    # puzzle = str([[4, 2, 7, 0], [14, 5, 3, 6], [1, 12, 10, 11], [9, 8, 15, 13]])
    # puzzle = str([[1, 2, 3, 7], [4, 5, 6, 11], [9, 10, 15, 14], [8, 12, 13, 0]])    #14
    # puzzle = str([[1, 8, 2, 3], [4, 5, 11, 7], [12, 9, 6, 10], [0, 13, 14, 15]])    #21
    # puzzle = str([[15, 8, 10, 4], [9, 12, 11, 3], [0, 5, 2, 14], [7, 1, 6, 13]])
    # puzzle = str([[1, 2, 0, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
    goal = str([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])

    rb_data = []
    ida_data = []

    for it in range(20):
        puzzle = random_board(goal)
        rb = rbfs(puzzle, goal, man_dist)
        ida_res = ida_star(puzzle, goal, man_dist)
        # ida_res2 = ida_star(puzzle, goal, bad_h)
        # rb2 = rbfs(puzzle, goal, bad_h)
        rb_data.append(rb)
        ida_data.append(ida_res)
        print puzzle, ida_res, rb #, ida_res2, rb2

    plot(rb_data, ida_data)
