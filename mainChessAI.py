
#%% Imports

import board, pieces, ai

#%% Get user move

# Returns a move object based on the users input. Does not check if the move is valid.
def get_user_move(move_str):
    if move_str == "":
        move_str = input("Your Move: ")
    move_str = move_str.replace(" ", "")

    try:
        xfrom = letter_to_xpos(move_str[0:1])
        yfrom = 8 - int(move_str[1:2]) # The board is drawn "upside down", so flip the y coordinate.
        xto = letter_to_xpos(move_str[2:3])
        yto = 8 - int(move_str[3:4]) # The board is drawn "upside down", so flip the y coordinate.
        return ai.Move(xfrom, yfrom, xto, yto, True)
    except ValueError:
        print("Invalid format. Example: A2 A4")
        return get_user_move()

#%% Get Chess move

# Returns a valid move based on the users input.
def get_valid_user_move(board, move_str):
    while True:
        move = get_user_move(move_str)
        valid = False
        possible_moves = board.get_possible_moves(pieces.Piece.WHITE)
        # No possible moves
        if (not possible_moves):
            return 0

        for possible_move in possible_moves:
            if (move.equals(possible_move)):
                move.castling_move = possible_move.castling_move
                valid = True
                break

        if (valid):
            break
        else:
            print("Invalid move.")
    return move

#%% Converts a letter (A-H) to the x position on the chess board.
def letter_to_xpos(letter):
    letter = letter.upper()
    if letter == 'A':
        return 0
    if letter == 'B':
        return 1
    if letter == 'C':
        return 2
    if letter == 'D':
        return 3
    if letter == 'E':
        return 4
    if letter == 'F':
        return 5
    if letter == 'G':
        return 6
    if letter == 'H':
        return 7
    raise ValueError("Invalid letter.")
    
#%% Castling

def castling(board, move_str):
    if move_str =='O-O':
        # King
        board.chesspieces[4][7], board.chesspieces[6][7] = (
            board.chesspieces[6][7], board.chesspieces[4][7])
        board.chesspieces[6][7].x = 6
        
        # Rook
        board.chesspieces[7][7], board.chesspieces[5][7] = (
            board.chesspieces[5][7], board.chesspieces[7][7])
        board.chesspieces[5][7].x = 5
        
    if move_str == 'O-O-O':
        # King
        board.chesspieces[4][7], board.chesspieces[2][7] = (
            board.chesspieces[2][7], board.chesspieces[4][7])
        board.chesspieces[2][7].x = 2
        
        # Rook
        board.chesspieces[0][7], board.chesspieces[3][7] = (
            board.chesspieces[3][7], board.chesspieces[0][7])
        board.chesspieces[3][7].x = 3
    return board
    
#%% Get Board

def getBoard(board=board):
    import board
    board = board.Board.new()
    print(board.to_string())
    return board

#%% AI Move

def AIHumanMove(board, move_str=""):
    # Human
    board = humanMove(board, move_str)
    
    # AI
    board, xfrom, yfrom, xto, yto = AIMove(board)
    return board, xfrom, yfrom, xto, yto

# Human move
def humanMove(board, move_str=''):
    if move_str in ['O-O', 'O-O-O']:
        board = castling(board, move_str)
    else:
        move = get_valid_user_move(board, move_str)
        board.perform_move(move)
        print("User move: " + move.to_string())
    print(board.to_string())
    return board

# AI Move
def AIMove(board):
    ai_move = ai.AI.get_ai_move(board, [])
    board.perform_move(ai_move)
    print("AI move: " + ai_move.to_string())
    print(board.to_string())
    return board, ai_move.xfrom, ai_move.yfrom, ai_move.xto, ai_move.yto
    
        
