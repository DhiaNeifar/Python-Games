def find_positions(checkers, player):
    positions = []
    for i in range(len(checkers)):
        for j in range(len(checkers[i])):
            if checkers[i][j] == player:
                positions.append((i, j))
    return positions


def future_movements(checkers, curr_position):
    future_mvts = []
    eaten_pieces = []
    grid_size = len(checkers)
    x, y = curr_position[0], curr_position[1]
    player = checkers[x][y]


    # Go to Top-Left
    i = x - 1
    j = y - 1
    while 0 < i and 0 < j:
        if checkers[i][j] != player and checkers[i][j] != ' ':
            eaten_pieces.append((i, j))
            future_mvts.append((i - 1, j - 1))
            break
        i -= 1
        j -= 1

    # Go to Bottom-Right
    i = x + 1
    j = y + 1
    while i < grid_size - 1 and j < grid_size - 1:
        if checkers[i][j] != player and checkers[i][j] != ' ':
            eaten_pieces.append((i, j))
            future_mvts.append((i + 1, j + 1))
            break
        i += 1
        j += 1

    # Go to Top-Right
    i = x - 1
    j = y + 1
    while 0 < i and j < grid_size - 1:
        if checkers[i][j] != player and checkers[i][j] != ' ':
            eaten_pieces.append((i, j))
            future_mvts.append((i - 1, j + 1))
            break
        i -= 1
        j += 1

    # Go to Bottom-Left
    i = x + 1
    j = y - 1

    while i < grid_size - 1 and 0 < j:
        if checkers[i][j] != player and checkers[i][j] != ' ':
            eaten_pieces.append((i, j))
            future_mvts.append((i + 1, j - 1))
            break
        i += 1
        j -= 1
    return future_mvts, eaten_pieces


def best_outcome(checkers, position):
    def BackTrack(_checkers, curr_position, max_eaten):
        future_mvts, eaten_pieces = future_movements(_checkers, curr_position)
        if len(future_mvts) == 0:
            results.append(max_eaten)
            return
        for index, future_mvt in enumerate(future_mvts):
            eaten_piece = eaten_pieces[index]
            _checkers[eaten_piece[0]][eaten_piece[1]] = ' '
            BackTrack(_checkers, future_mvt, max_eaten + 1)

    results = []
    BackTrack(checkers, position, 0)
    return max(results)


def main():

    checkers = \
        [
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B'],
            [' ', 'B', ' ', ' ', ' ', ' ', 'B', ' '],
            ['W', ' ', 'B', ' ', 'B', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'W', ' ', ' '],
            [' ', ' ', 'B', ' ', 'B', ' ', 'B', ' '],
            [' ', 'B', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', 'B', ' ', 'B', ' '],
            [' ', 'B', ' ', ' ', ' ', ' ', ' ', ' '],

        ]

    White_positions = find_positions(checkers, 'W')
    all_best_outcomes = []
    for white_position in White_positions:
        copied_checkers = [[checkers[i][j]for j in range(len(checkers))] for i in range(len(checkers))]
        all_best_outcomes.append(best_outcome(copied_checkers, white_position))
    print(max(all_best_outcomes))


if __name__ == '__main__':
    main()
