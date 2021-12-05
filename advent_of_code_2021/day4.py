import typing

test_data = """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""


class Input(typing.TypedDict):
    numbers: dict
    boards: list


def _parse_row(row):
    return list(map(int, row.split()))


def _parse_board(board):
    return list(map(_parse_row, board))


def parse_input(input: str) -> Input:
    input = input.strip().split("\n\n")
    bingo_numbers = list(map(int, input[0].split(",")))
    raw_boards = list(map(lambda s: s.splitlines(), input[1:]))
    boards = list(map(_parse_board, raw_boards))
    return {"numbers": bingo_numbers, "boards": boards}


class State(typing.TypedDict):
    numbers: dict
    board_sums: list
    rows: list
    columns: list


def _sum_board(board):
    sum = 0
    for r in board:
        for x in r:
            sum += x
    return sum


def _numbers_from_board(numbers, board_num, board):
    for i, r in enumerate(board):
        for j, x in enumerate(r):
            if x in numbers:
                numbers[x].append([board_num, i, j])
            else:
                numbers[x] = [[board_num, i, j]]
    return numbers


def _add_board_to_state(state: State, board_num, board):
    """Modifies State in place. Sorry."""
    # Add new sum to board sums.
    bsum = _sum_board(board)
    state["board_sums"].append(bsum)
    # Add new empty rows and columns.
    rows = [[] for _ in range(len(board))]
    cols = [[] for _ in range(len(board))]
    state["rows"].append(rows)
    state["columns"].append(cols)
    # Add numbers from board.
    _numbers_from_board(state["numbers"], board_num, board)


def _initial_state() -> State:
    return {"numbers": {}, "board_sums": [], "rows": [], "columns": []}


def _load_input(input) -> State:
    state = _initial_state()
    for idx, board in enumerate(input["boards"]):
        _add_board_to_state(state, idx, board)
    return state


def _process_number(state, board_size, number, return_early=False):
    winners = []
    if number in state["numbers"]:
        data = state["numbers"][number]
        for board_num, i, j in data:
            # update board_sums
            state["board_sums"][board_num] -= number
            # add to rows
            state["rows"][board_num][i].append(number)
            # add to cols
            state["columns"][board_num][j].append(number)

            if (
                len(state["rows"][board_num][i]) == board_size
                or len(state["columns"][board_num][j]) == board_size
            ):
                if return_early:
                    return (board_num, number, state["board_sums"][board_num])
                else:
                    winners.append([board_num, number, state["board_sums"][board_num]])
    return winners


def _run_numbers(state, input, return_early=True):
    board_size = len(input["boards"][0])
    winners = []
    for i, n in enumerate(input["numbers"]):
        res = _process_number(state, board_size, n, return_early)
        if res:
            if return_early:
                return res[0]
            else:
                winners.extend(res)

    return winners


def part1(input):
    parsed_input = parse_input(input)
    state = _load_input(parsed_input)
    res = _run_numbers(state, parsed_input)
    return res[1] * res[2]


def _find_last_winner(num_boards, winners):
    boards = set(range(num_boards))
    for w in winners:
        boards.discard(w[0])
        if not boards:
            return w


def part2(input):
    parsed_input = parse_input(input)
    state = _load_input(parsed_input)
    winners = _run_numbers(state, parsed_input, return_early=False)
    winner = _find_last_winner(len(parsed_input["boards"]), winners)
    if winner:
        return winner[1] * winner[2]
