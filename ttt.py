import copy

# def alphabeta(node, d, alp, bet, max):
#	if d = 0 or terminal:
#		return h val of node
#	if max:
#		v = -inf
#		for child of node
#			v = max(v, alphabeta(child, d - 1, alpha, beta, false))
#			alpha = max(alpha, v)
#			if beta <= alpha:
#				break # beta cutoff
#		return v
#	else:
#		v = inf
#		for each child of node:
#			v = min(v, alphabeta(child, d - 1, alpha, beta, True))
#			beta = min(beta, v)
#			if beta <= alpha:
#				break
#		return v

inf = float('inf')
def alphabeta(node, alpha, beta, player):
	is_over, win = terminal_test(node)	
	if is_over:
		return "O_X".find(win) - 1	# -1 for O, 1 for X, 0 for draw game
	if player == 'X':
		v = -inf
		for board in successors(node, player):
			v = max(v, alphabeta(board, alpha, beta, 'O'))
			alpha = max(alpha, v)
			if beta <= alpha:
				break # beta cutoff
		return v
	else:
		v = inf
		for board in successors(node, player):
			v = min(v, alphabeta(board, alpha, beta, 'X'))
			beta = min(beta, v)
			if beta <= alpha:
				break
		return v
# alphabeta(start, depth, -inf, inf, TRUE)

def init(n):
	return [list('_' * n) for i in range(n)]

def make_move(board, player, move):
	i, j = move
	newboard = copy.deepcopy(board)
	newboard[i][j] = player
	return newboard

def successors(board, player):
	out = []
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == '_':
				out.append(make_move(board, player, (i, j)))
	return out

def terminal_test(board):
	for player in ['X', 'O']: 
		if any(map(lambda row: all(map(lambda x: x == player, row)), board)): return (True, player)  
		if any(map(lambda row: all(map(lambda x: x == player, row)), map(list, zip(*board)))): return (True, player) 
		n = len(board[0])		
		d1 = [board[i][i] for i in range(n)]
		d2 = [board[n - 1 - i][i] for i in range(n - 1, -1, -1)]
		if all(map(lambda x: x == player, d1)): return (True, player) 
		if all(map(lambda x: x == player, d2)): return (True, player) 
	if not any('_' in row for row in board): return (True, '_') 
	return (False, '_') 	

def show(board):
	for row in board:
		print ' '.join(row)

def next_player(p):
	return 'X' if p == 'O' else 'O'

def human_move(board):
	n = len(board)
	x, y = -1, -1
	bounds = lambda x: x >= 0 and x < n 
	while True:  	
		line = map(int, raw_input().split())
		x, y = line[0] - 1, line[1] - 1
		if not bounds(x) or not bounds(y) or board[x][y] != '_':
			print 'Try Again!'
		else: return x, y
			
		
def play():
	board = init(3)
	p = 'X'
	while not terminal_test(board)[0]:
		if p == 'X':
			x, y = human_move(board)
			board = make_move(board, p, (x, y))
		else:
			board = min(successors(board, 'O'), key=lambda x:alphabeta(x, -inf, inf, 'X'))
		p = next_player(p)
		show(board)
	winner = terminal_test(board)[1]
	print 'Game Over!',
	if winner == '_': print 'Draw Game.'
	else : print winner, 'won.'

terminal_test		
play()
