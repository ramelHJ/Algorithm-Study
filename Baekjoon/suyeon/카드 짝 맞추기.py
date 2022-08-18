from collections import defaultdict, deque

# 상 하 좌 우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]


def get_ctrl(board, current, direct):
    x, y = current

    while True:
        nx = x + dx[direct]
        ny = y + dy[direct]

        if nx < 0 or nx >= 4 or ny < 0 or ny >= 4:
            return x, y

        if board[nx][ny]:
            return nx, ny

        x, y = nx, ny


def get_min_move(board, start, end):
    visited = [[False] * 4 for _ in range(4)]

    sx, sy = start
    ex, ey = end

    queue = deque([(sx, sy, 0)])
    visited[sx][sy] = True

    while queue:
        x, y, move = queue.popleft()

        if x == ex and y == ey:
            return move

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            if nx < 0 or nx >= 4 or ny < 0 or ny >= 4:
                continue

            if not visited[nx][ny]:
                queue.append((nx, ny, move + 1))
                visited[nx][ny] = True

            nx, ny = get_ctrl(board, (x, y), i)

            if not visited[nx][ny]:
                queue.append((nx, ny, move + 1))
                visited[nx][ny] = True


def get_match_card(card_dict, card, current):
    if tuple(card_dict[card][:2]) == current:
        return tuple(card_dict[card][2:])

    return tuple(card_dict[card][:2])


def get_nearest_cards(board, card_set, start):
    if board[start[0]][start[1]]:
        return [(start, 0)]

    cards = [(end, get_min_move(board, start, end)) for end in card_set]
    min_move = min(list(zip(*cards))[1])

    return [(end, move) for end, move in cards if move == min_move]


def get_min_operation(board, card_dict, card_set, current, count):
    if not card_set:
        return count

    min_count = int(1e9)

    for start, start_move in get_nearest_cards(board, card_set, current):
        card = board[start[0]][start[1]]

        end = get_match_card(card_dict, card, start)
        end_move = get_min_move(board, start, end)

        board[start[0]][start[1]] = 0
        board[end[0]][end[1]] = 0

        operation = start_move + end_move + 2
        min_operation = get_min_operation(board, card_dict, card_set - {start, end}, end, count + operation)

        min_count = min(min_count, min_operation)

        board[start[0]][start[1]] = card
        board[end[0]][end[1]] = card

    return min_count


def solution(board, r, c): 
    card_set, card_dict = set(), defaultdict(list)

    for i in range(len(board)):
        for j in range(len(board[0])):
            card = board[i][j]

            if card:
                card_set.add((i, j))
                card_dict[card].extend([i, j])

    return get_min_operation(board, card_dict, card_set, (r, c), 0)