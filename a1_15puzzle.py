import heapq

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
    return (-1, extended_node_count)

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
    return _rbfs(start, goal, 0, h(start), float('inf'), h)

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
        alt = sort_fs[1] 
        result, fs[best], n = _rbfs(best, goal, gval + 1, fs[best], min(bound, alt), h)
        nodes_generated += n
        if result != False:
            return result, fs[best], nodes_generated

if __name__ == '__main__':
    puzzle = str([[1, 2, 6, 3], [4, 9, 5, 7], [8, 13, 11, 15], [12, 14, 0, 10]])
    # puzzle = str([[4, 2, 7, 0], [14, 5, 3, 6], [1, 12, 10, 11], [9, 8, 15, 13]])
    # puzzle = str([[1, 2, 3, 7], [4, 5, 6, 11], [9, 10, 15, 14], [8, 12, 13, 0]])    #14
    # puzzle = str([[15, 8, 10, 4], [9, 12, 11, 3], [0, 5, 2, 14], [7, 1, 6, 13]])
    # puzzle = str([[1, 2, 0, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
    end = str([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
    exnodecount = astar(puzzle, end, man_dist)
    print exnodecount
    #opt = ida_star(puzzle, end, man_dist)
    #print opt
    rb = rbfs(puzzle, end, man_dist)
    print rb