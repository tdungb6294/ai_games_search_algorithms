from ortools.sat.python import cp_model

class CheckersSolver:
    def __init__(self, state):
        self.model = cp_model.CpModel()
        self.variables = []
        self.state = state

    def add_variables(self):
        self.variables = [self.model.NewBoolVar(f"{move}") for move in self.state.moves]  # all individual possible moves

    def add_constraints(self):
        self.model.Add(sum(self.variables) == 1)  # only one is selected

    def add_objective(self):
        self.model.Maximize(sum((self.variables[i] * self.evaluate_move(self.state.moves[i]) for i in
                                 range(len(self.state.moves)))))
        self.model.Minimize(sum((self.variables[i] * self.minimize_vulnerability(self.state.moves[i]) for i in
                                 range(len(self.state.moves)))))

    def evaluate_move(self, move):  # find the least risky move
        count_score = 0
        if len(move[2]) > 0:
            count_score += len(move[2])
        return count_score

    def minimize_vulnerability(self, move):
        directions = [(1, -1), (1, 1), (-1, -1), (-1, 1)]  # Possible move offsets for regular pieces
        board = self.state.board
        player = self.state.to_move
        count_vulnerability_rate = 2  # default when not the corner or share the borders
        (x, y) = move[1]
        first_element = list(board.keys())[0]
        last_element = list(board.keys())[-1]
        if (x, y) == first_element or (x, y) == last_element:
            count_vulnerability_rate = 0  # share the corner
        elif x == first_element[0] or y == first_element[1] or x == last_element[0] or y == last_element[1]:
            count_vulnerability_rate = 1  # share the border
        elif player == 'X':
            for dx, dy in directions:
                next_x, next_y = x + dx, y + dy
                if (next_x, next_y) in board and board[(next_x, next_y)] == 'O':
                    count_vulnerability_rate = 3  # share the diagonal with enemy
                    capture_x, capture_y = x - dx, y - dy
                    if (capture_x, capture_y) in board and board[(capture_x, capture_y)] is None:
                        count_vulnerability_rate = 4  # might be captured
        elif player == 'O':
            for dx, dy in directions:
                next_x, next_y = x + dx, y + dy
                if (next_x, next_y) in board and board[(next_x, next_y)] == 'X':
                    count_vulnerability_rate = 3
                    capture_x, capture_y = x - dx, y - dy
                    if (capture_x, capture_y) in board and board[(capture_x, capture_y)] is None:
                        count_vulnerability_rate = 4

        return count_vulnerability_rate

    def solve(self):
        solver = cp_model.CpSolver()
        status = solver.Solve(self.model)
        if status == cp_model.OPTIMAL:
            return self.get_selected_move(solver)

    def get_selected_move(self, solver):
        i = 0
        for var in self.variables:
            if solver.Value(var):
                return self.state.moves[i]
            i += 1
        return None
