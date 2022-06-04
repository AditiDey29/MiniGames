import pygame
import sys
import time
import copy

class TTT:
    X = "X"
    O = "O"
    EMPTY = ""

    def initial_state(self):  # Returns starting state of the board
        return [["", "", ""], ["", "", ""], ["", "", ""]]

    def player(self,board):  # Returns which player plays next

        # Checking if there are any blank boxes remaining
        blank = False
        for row in board:
            if "" in row:
                blank = True
                break

        if blank:
            countX = 0
            countO = 0
            for row in board:
                for entry in row:
                    if entry == "X":
                        countX += 1
                    elif entry == "O":
                        countO += 1

            if countO == countX:
                return "X"
            else:
                return "O"
        else:
            return

    def actions(self,board):  # Returns all unique possible actions (row, col) available on the board.
        possible = set()
        flag = False
        for row in range(3):
            for col in range(3):
                if (board[row][col] == ""):
                    flag = True
                    possible.add((row, col))

        if (flag == False):
            return -1

        else:
            return possible

    def result(self,board, action):  # Returns the board that results from making move (row, col) on the board.

        new = copy.deepcopy(board)
        row = action[0]
        col = action[1]
        if new[row][col] == "":
            next_turn = self.player(new)
            new[row][col] = next_turn
            return new

        else:
            raise Exception("Not possible")

    def winner(self,board):  # Returns the winner of the game

        # Rows
        if board[0].count("X") == 3 or board[1].count("X") == 3 or board[2].count("X") == 3:
            return "X"
        if board[0].count("O") == 3 or board[1].count("O") == 3 or board[2].count("O") == 3:
            return "O"

        # Columns
        if board[0][0] == "X" and board[1][0] == "X" and board[2][0] == "X":
            return "X"
        if board[0][1] == "X" and board[1][1] == "X" and board[2][1] == "X":
            return "X"
        if board[0][2] == "X" and board[1][2] == "X" and board[2][2] == "X":
            return "X"
        if board[0][0] == "O" and board[1][0] == "O" and board[2][0] == "O":
            return "O"
        if board[0][1] == "O" and board[1][1] == "O" and board[2][1] == "O":
            return "O"
        if board[0][2] == "O" and board[1][2] == "O" and board[2][2] == "O":
            return "O"

        # Main Diagonal
        if board[0][0] == "X" and board[1][1] == "X" and board[2][2] == "X":
            return "X"
        if board[0][0] == "O" and board[1][1] == "O" and board[2][2] == "O":
            return "O"

        # Anti Diagonal
        if board[0][2] == "X" and board[1][1] == "X" and board[2][0] == "X":
            return "X"
        if board[0][2] == "O" and board[1][1] == "O" and board[2][0] == "O":
            return "O"
        return None

    def game_over(self,board):  # Returns True if game is over, False otherwise.

        if self.winner(board) is not None:
            return True

        blanks = sum([row.count("") for row in board])

        if blanks == 0:
            return True
        else:
            return False

    def utility(self,board):  # Returns 1 if X has won the game, -1 if O has won, 0 otherwise.

        if self.winner(board) == "X":
            return 1
        elif self.winner(board) == "O":
            return -1
        else:
            return 0

    def MAX(self,board):
        if self.game_over(board):
            return self.utility(board)

        m = -2
        moves = self.actions(board)
        for move in moves:
            m = max(m, self.MIN(self.result(board, move)))
            if m == 1:
                return m
        return m

    def MIN(self,board):

        if self.game_over(board):
            return self.utility(board)

        m = 2
        moves = self.actions(board)
        for move in moves:
            m = min(m, self.MAX(self.result(board, move)))
            if (m == -1):
                return m
        return m

    def minimax(self,board):  # Returns the optimal action for the current player on the board.

        if self.game_over(board):
            return None
        elif board==self.initial_state() and self.player(board)== "X":
            return (1,1)
        elif self.player(board) == "X":
            best = -2
            bestMove = tuple()
            moves = self.actions(board)
            for move in moves:
                move_val = self.MIN(self.result(board, move))
                if (move_val == 1):
                    return move
                elif (move_val > best):
                    best = move_val
                    bestMove = move
            return bestMove
        elif self.player(board) == "O":
            best = 2
            bestMove = tuple()
            moves = self.actions(board)
            print(moves)
            for move in moves:

                move_val = self.MAX(self.result(board, move))
                if (move_val == -1):
                    return move
                elif (move_val < best):
                    best = move_val
                    bestMove = move
            return bestMove


ttt = TTT()
pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# black = (255, 253, 208)
# white = (165, 42, 42)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("freesansbold.ttf", 28)
largeFont = pygame.font.Font("freesansbold.ttf", 40)
moveFont = pygame.font.Font("freesansbold.ttf", 60)

user = None
board = ttt.initial_state()
ai_turn = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    # Let user choose a player.
    if user is None:

        # Draw title
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O

    else:

        # Draw game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.game_over(board)
        player = ttt.player(board)

        # Show title
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            title = f"Play as {user}"
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False

    pygame.display.flip()