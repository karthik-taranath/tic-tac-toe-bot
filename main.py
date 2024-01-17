import pygame

pygame.init()
screen = pygame.display.set_mode((500, 700))
clock = pygame.time.Clock()


def draw_board():
    screen.fill("#ffffff")
    pygame.draw.line(screen, "black", (175, 25), (175, 475), 2)
    pygame.draw.line(screen, "black", (325, 25), (325, 475), 2)
    pygame.draw.line(screen, "black", (25, 175), (475, 175), 2)
    pygame.draw.line(screen, "black", (25, 325), (475, 325), 2)
    pygame.draw.rect(screen, "black", (25, 500, 450, 175), 1)


def draw_x(square):
    x = square % 3
    y = square // 3
    pygame.draw.line(screen, "black", (x * 150 + 50, y * 150 + 50), (x * 150 + 150, y * 150 + 150), 2)
    pygame.draw.line(screen, "black", (x * 150 + 150, y * 150 + 50), (x * 150 + 50, y * 150 + 150), 2)


def draw_o(square):
    x = square % 3
    y = square // 3
    pygame.draw.circle(screen, "black", (x * 150 + 100, y * 150 + 100), 50, 2)


def pos_to_square(pos):
    x, y = [(i - 25) // 150 for i in pos]
    if 0 <= x <= 2 and 0 <= y <= 2:
        return x + 3 * y
    return -1


def state(board):
    win_table = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    for x, y, z in win_table:
        if board[x] == board[y] == board[z] != 0:
            return board[x]
    return 0


def minimax(board, depth, is_max):
    if depth == 0 or 0 not in board:
        return -1, state(board)

    if is_max:
        best_eval = float('-inf')
        best_move = -1
        for i, square in enumerate(board):
            if square == 0:
                copy = board.copy()
                copy[i] = 1

                if state(copy) == 1:
                    return i, 1

                _, new_eval = minimax(copy, depth - 1, False)
                if new_eval > best_eval:
                    best_eval = new_eval
                    best_move = i
        return best_move, best_eval

    else:
        best_eval = float('inf')
        best_move = -1
        for i, square in enumerate(board):
            if square == 0:
                copy = board.copy()
                copy[i] = -1

                if state(copy) == -1:
                    return i, -1

                _, new_eval = minimax(copy, depth - 1, True)
                if new_eval < best_eval:
                    best_eval = new_eval
                    best_move = i
        return best_move, best_eval


def main():
    turn = 0
    while True:
        pygame.event.clear(pygame.MOUSEBUTTONDOWN)
        draw_board()
        pygame.display.update()

        board = [0] * 9

        while 0 in board and state(board) == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if turn % 2 == 0:
                        square = pos_to_square(pygame.mouse.get_pos())
                        if square != -1 and board[square] == 0:
                            board[square] = 1
                            turn += 1

                            draw_x(square)
                            pygame.display.update()

            if turn % 2 == 1:
                square, evaluation = minimax(board, 10, False)
                board[square] = -1
                turn += 1

                pygame.time.wait(500)
                draw_o(square)
                pygame.display.update()

            # flip() the display to put your work on screen
            clock.tick(60)

        result = state(board)

        if result == 1:
            text = "X wins!"
            turn = 1
        elif result == -1:
            text = "O wins!"
            turn = 0
        else:
            text = "Draw!"

        font = pygame.font.Font(None, 100)
        text_surface = font.render(text, True, "black")
        pos = (25 + (450 - text_surface.get_width()) // 2, 500 + (175 - text_surface.get_height()) // 2)
        screen.blit(text_surface, pos)

        pygame.display.update()

        pygame.time.wait(1000)


if "__main__" == __name__:
    main()
