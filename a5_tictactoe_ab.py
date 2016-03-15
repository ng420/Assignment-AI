import copy

class board:
    def __init__(self, h, v):
        self.h = h
        self.v = v
        self.matrix = [list('_' * 3) for i in range(3)]
        self.moves = [(x, y) for x in range(h)
                        for y in range(v)]
    def show(self):
        for x in range(self.h):
            for y in range(self.v):
                print self.matrix[x][y],
            print

    def make_move(self, player, move):
        self.matrix[move[0]][move[1]] = player
        self.moves.remove(move)

    def legal_moves(self):
        return self.moves

    def check_win(self, player):
        xs = [0, 1, 2, 0, 0, 0, 0, 0]
        ys = [0, 0, 0, 0, 1, 2, 0, 2]
        dx = [0, 0, 0, 1, 1, 1, 1, 1]
        dy = [1, 1, 1, 0, 0, 0, 1, -1]
        for i in range(len(xs)):
            x = xs[i]
            y = ys[i]
            ok = True
            for j in range(3):
                if self.matrix[x][y] != player:
                    ok = False
                x += dx[i]
                y += dy[i]
            if ok:
                return True
        return False

class tic_tac_toe:
    def make_move(self, player, move, board):
        newboard = copy.deepcopy(board)
        newboard.make_move(player, move)
        return newboard

    def utility(self, board, player):
        abstract

    def terminal_test(self, board):
        return not board.legal_moves

    def display(self, board):
        board.show()

    def successors(self, board):
        return [(move, self.make_move(move, board))
                for move in self.legal_moves(board)]
    
def play():
    t = tic_tac_toe()
    b = board(3, 3)
    player = ['X', 'O']
    to_play = 0
    game_over = False
    while not game_over and not t.terminal_test(b):
        x = input()
        y = input()
        while (x, y) not in b.legal_moves():
            print 'Invalid move. Try again.'
            x = input()
            y = input()
        b = t.make_move(player[to_play], (x,y), b)
        b.show()
        if b.check_win(player[to_play]):
            print player[to_play], 'won'
            game_over = True
        to_play = 1 - to_play
