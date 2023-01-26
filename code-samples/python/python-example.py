def explode_game(row):
    
    import chess
    from chess import pgn
    import io
    import pandas as pd

    # There is a neuron for each position on a chess board
    NEURON_LABELS = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8', 
                     'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7', 
                     'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6', 
                     'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5', 
                     'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4', 
                     'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3', 
                     'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2', 
                     'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
    
    # String representations of each chess piece
    PIECE_TYPES = ['K', 'Q', 'R', 'B', 'N', 'P', 'k', 'q', 'r', 'b', 'n', 'p']

    # Load the game into memory using the 'moves' column
    pgn = io.StringIO(row['moves'])
    game = chess.pgn.read_game(pgn)
    board = game.board()
    
    # Keep track of the current move
    current_move_number = 0

    column_dtypes = {}

    # add to the column types each of the board locations (and set the dtype
    # to "category")
    for label in NEURON_LABELS:
        column_dtypes[label] = 'category'
    
    # Add piece type columns for each state, to count the number of different
    # piece types present on the board
    for piece_type in PIECE_TYPES:
        column_dtypes[piece_type] = 'int8'
    
    # stores the list of different game states that will be generated
    # for this row
    game_states = []
    
    for move in game.mainline_moves():
        board.push(move)
        
        # update the move number
        current_move_number += 1
        
        # remove any spaces and newlines in the board
        board_state = str(board)#.replace(' ', '').replace('\n', '')
        
        # keep track of the pieces on the board
        neuron_values = list()
        
        # keep track of how many pieces each player has
        white_pieces = 0
        black_pieces = 0
        
        # creates a dictionary where the key is the piece type and the value
        # is set to zero. This is used to track how many of each piece are
        # on the board. As an independent datatype to *where* such pieces
        # are placed, these counts provide an additional input vector for
        # our neural network to work with
        piece_counts = dict(zip(PIECE_TYPES, [0] * len(PIECE_TYPES)))
        
        # See documentation for python-chess to see what board_state looks
        # like, but it's basically 8 lines of text, where a period indicates
        # the absence of a piece, and a lower or upper case letter indicates
        # the piece that is at that position
        for str_index in range(0, len(board_state)):
            neuron_value = board_state[str_index]
            
            if (neuron_value == '\n' or neuron_value == ' '):
                continue
            
            if (neuron_value == '.'):
                neuron_value = ''
            
            # if the value is a letter
            if neuron_value.isalpha():
                # update the count of each piece type
                piece_counts[neuron_value] += 1
                # if it's upper case, then it's a white piece
                if neuron_value.isupper():
                    white_pieces += 1
                else: # otherwise it's a black piece
                    black_pieces += 1
            
            # add the value
            neuron_values.append(neuron_value)
        
        # zip the neuron labels and neuron values into a dictionary
        board_state_table = dict(zip(NEURON_LABELS, neuron_values))
        
        # load other state data
        game_state = dict({
            'winner': row['winner'],
            'current_move': current_move_number,
            'total_moves': row['move_count'],
            'black_pieces': black_pieces,
            'white_pieces': white_pieces,
            'next_move': 'W' if board.turn else 'B'
        })
    
        # add the board state table and the piece counts to the game state
        game_state = (game_state | board_state_table | piece_counts)
        
        # add the current game state to our list of game states
        game_states.append(game_state)
    
    # Create the dataframe
    df_game_states = pd.DataFrame(game_states, copy=False)
             
    # enforce the types for the dataframe
    df_game_states = df_game_states.astype(column_dtypes)
    
    return game_states