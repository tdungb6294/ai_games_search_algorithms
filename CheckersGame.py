from Game import Game
from Game import GameState


class CheckersGame(Game):
    # konstruktorius saskes lentai inicializuoti
    def __init__(self, h=4, w=4):
        self.h = h  # height of the board
        self.w = w  # width of the board
        board = {}  # board state
        for x in range(1, h + 1):
            for y in range(1, w + 1):
                if (x + y) % 2 == 0:
                    if x < h / 2:
                        board[(x, y)] = 'X'
                    elif x > h / 2 + 1:
                        board[(x, y)] = 'O'
                    else:
                        board[(x, y)] = None
                else:
                    board[(x, y)] = None
        moves = self.get_all_moves(board, 'X')
        self.initial = GameState(to_move='X', utility=0, board=board, moves=moves)

    # surasti visus zingsnius, kur sugauname priesu saskes
    def find_capture_moves(self, board, legal_moves, initial_position, x, y, player, captured_pieces):
        directions = [(1, -1), (1, 1), (-1, -1), (-1, 1)]  # Possible move offsets for regular pieces

        if player == 'X':
            for dx, dy in directions:
                next_x, next_y = x + dx, y + dy
                capture_x, capture_y = next_x + dx, next_y + dy

                if (next_x, next_y) in board and (capture_x, capture_y) in board:
                    if board[(next_x, next_y)] == 'O' and board[(capture_x, capture_y)] is None:
                        if (next_x, next_y) in captured_pieces:
                            return
                        new_captured_pieces = captured_pieces[:]
                        new_captured_pieces.append((next_x, next_y))
                        self.find_capture_moves(board, legal_moves, initial_position, capture_x, capture_y, player, new_captured_pieces)
        elif player == 'O':
            for dx, dy in directions:
                next_x, next_y = x + dx, y + dy
                capture_x, capture_y = next_x + dx, next_y + dy

                if (next_x, next_y) in board and (capture_x, capture_y) in board:
                    if board[(next_x, next_y)] == 'X' and board[(capture_x, capture_y)] is None:
                        if (next_x, next_y) in captured_pieces:
                            return
                        new_captured_pieces = captured_pieces[:]
                        new_captured_pieces.append((next_x, next_y))
                        self.find_capture_moves(board, legal_moves, initial_position, capture_x, capture_y, player, new_captured_pieces)

        if captured_pieces:
            legal_moves.append((initial_position, (x, y), captured_pieces))

    # grazinam dabartines busenos zingsnius
    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        return state.moves

    # grazinam visus imanomus zingsnius
    def get_all_moves(self, board, player_to_move):
        legal_moves = []

        # iterate through  all piece on the board
        for position, piece in board.items():
            if piece == player_to_move:
                (x, y) = position

                # check legal moves for regular pieces
                if piece == 'X':  # Assuming 'X' moves upwards
                    # check forward left
                    if (x + 1, y - 1) in board and board[(x + 1, y - 1)] is None:
                        legal_moves.append((position, (x + 1, y - 1), []))
                    # check forward right
                    if (x + 1, y + 1) in board and board[(x + 1, y + 1)] is None:
                        legal_moves.append((position, (x + 1, y + 1), []))
                    self.find_capture_moves(board, legal_moves, position, x, y, piece, [])
                elif piece == 'O':  # Assuming 'O' moves downwards
                    # check forward left
                    if (x - 1, y - 1) in board and board[(x - 1, y - 1)] is None:
                        legal_moves.append((position, (x - 1, y - 1), []))
                    # check forward right
                    if (x - 1, y + 1) in board and board[(x - 1, y + 1)] is None:
                        legal_moves.append((position, (x - 1, y + 1), []))
                    # find all capture moves
                    self.find_capture_moves(board, legal_moves, position, x, y, piece, [])
        return legal_moves

    # grazinam busenos pakeitima, kai darom zingsni
    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        if move not in state.moves:
            return state
        board = state.board.copy()
        (initial_x, initial_y), (end_x, end_y), captured_pieces = move
        board[(initial_x, initial_y)] = None
        board[(end_x, end_y)] = state.to_move
        for captured_piece in captured_pieces:
            (x, y) = captured_piece
            board[(x, y)] = None
        new_player = ('O' if state.to_move == 'X' else 'X')
        moves = self.get_all_moves(board, new_player)
        return GameState(to_move=new_player,
                         utility=self.compute_utility(state, move),
                         board=board,
                         moves=moves)

    # grazinam reiksme, kuri nusako, kas laimejo
    def utility(self, state, player):
        """Return the value of this final state to player."""
        return state.utility if player == 'X' else -state.utility

    # skaiciuojam pergales reiksme
    def compute_utility(self, state, move):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        board = state.board
        count_x = 0
        count_o = 0
        for (x, y) in board:
            if board[(x, y)] == 'X':
                count_x += 1
            elif board[(x, y)] == 'O':
                count_o += 1
        if count_x > count_o:
            return 1
        elif count_o > count_x:
            return -1
        else:
            return 0

    # tikrinam, ar baigtas zaidimas
    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not state.moves

    # grazinam dabartini zaideja
    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    # rodom konsole, kaip atrodo saskes lenta
    def display(self, state):
        """Print or otherwise display the state."""
        print(state)
        print(state.moves)
        board = state.board
        for y in range(0, self.w + 1):
            print(f"{y}", end=" ")

        for x in range(1, self.h + 1):
            if x != 0: print('\n', end=f"{x} ")
            for y in range(1, self.w + 1):
                if (x, y) in board:
                    value = board[(x, y)]
                    if value is not None:
                        print(value, end=" ")
                    else:
                        print(" ", end=f" ")
        print()

    # rodom klase string formatu
    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    # suzaidziam zaidima
    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                self.display(state)
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))
