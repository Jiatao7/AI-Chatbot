import tkinter as tk
from tkinter import messagebox
import chess
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
API_KEY = os.getenv("API_KEY")

# dimensions, change to adjust this is fine for my computer but idk the design
# also very important, image scaling is flat so just resize the images themselves, easier this way
WIDTH, HEIGHT = 600, 600
CELL_SIZE = WIDTH // 8

# colour scheme copied from online lol
WHITE = "#FFFFFF"
BLACK = "#000000"
GREEN = "#AAFF00"
LIGHT_BROWN = "#F0D9B5"
DARK_BROWN = "#B58863"

# all images of the pieces in resources, just reference that 
# k is king n is knight everything else is first letter of piece (b = black w = white second character varies based on piece name)
PIECES = {
    'P': 'chess_game/resources/wp.png',
    'p': 'chess_game/resources/bp.png',
    'R': 'chess_game/resources/wr.png',
    'r': 'chess_game/resources/br.png',
    'N': 'chess_game/resources/wn.png',
    'n': 'chess_game/resources/bn.png',
    'B': 'chess_game/resources/wb.png',
    'b': 'chess_game/resources/bb.png',
    'Q': 'chess_game/resources/wq.png',
    'q': 'chess_game/resources/bq.png',
    'K': 'chess_game/resources/wk.png',
    'k': 'chess_game/resources/bk.png'
}

board = chess.Board()
aiplayer = OpenAI(api_key= API_KEY) 



class ChessGame:
    def __init__(self, root):
        self.root = root
        # change
        self.root.title("chess")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT + 50)
        self.canvas.pack()
        self.input_text = tk.StringVar()
        self.valid_move = True
        
        # failsafe
        self.player_side = "white"
        self.ai_side = "black"
        self.is_ai_turn = False

        self.piece_images = {}
        for key, path in PIECES.items():
            self.piece_images[key] = tk.PhotoImage(file=path).subsample(8, 8)

        self.draw_board()
        self.update_pieces()

        # input box, the green thing, delete this later
        self.input_box = tk.Entry(root, textvariable=self.input_text, font=("Arial", 24), bg=GREEN, fg=BLACK)
        self.canvas.create_window(WIDTH // 2, HEIGHT + 25, window=self.input_box, width=WIDTH - 20, height=40)
        self.input_box.bind("<Return>", self.process_move)

        # you can now choose the side
        self.side_choice = tk.StringVar(value="Choose Side")
        self.side_menu = tk.OptionMenu(root, self.side_choice, "white", "black", command=self.set_player_side)
        self.side_menu.pack()

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
                x1, y1 = col * CELL_SIZE, row * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def update_pieces(self):
        self.canvas.delete("piece")
        for row in range(8):
            for col in range(8):
                piece = board.piece_at(row * 8 + col)
                if piece:
                    piece_symbol = piece.symbol()
                    x = col * CELL_SIZE + CELL_SIZE // 2
                    y = row * CELL_SIZE + CELL_SIZE // 2
                    self.canvas.create_image(x, y, image=self.piece_images[piece_symbol], tags="piece")

        self.check_game_state()

    def check_game_state(self):
        if board.is_checkmate():
            winner = "AI" if board.turn == (self.player_side == "white") else "Player"
            messagebox.showinfo("Game Over", f"Checkmate! {winner} wins.")
        elif board.is_stalemate():
            messagebox.showinfo("Game Over", "Stalemate!")
        elif board.is_check():
            messagebox.showinfo("Alert", "In Check!")

    # def process_move(self, event=None):
    #     global board
    #     move = self.input_text.get()
    #     try:
    #         board.push_san(move)
    #         self.valid_move = True
    #         self.update_pieces()
    #         self.input_text.set("")

    #         # self explanatory
    #         if board.turn == (self.ai_side == "white"):
    #             self.ai_make_move()
    #     except ValueError:
    #         self.valid_move = False
    #         messagebox.showerror("Error", "Illegal move!")
    #         self.input_text.set("")
    
    def process_move(self, event=None):
        global board
        move = self.input_text.get().strip()
        try:
            # parse input (e.g., "e1 e2" or "Nh4 Nf3")
            parts = move.split()
            if len(parts) != 2:
                raise ValueError("Invalid move format. (e.g. these are valid moves, (pawn from e1 to e2 is) 'e1 e2' or (knight from h4 to f3 is) 'Nh4 Nf3').")

            start_pos = parts[0]
            end_pos = parts[1]

            # validation
            if len(start_pos) < 2 or len(end_pos) < 2:
                raise ValueError("Invalid positions. Use valid chess squares like 'e1' or 'f3'.")
            
            start_square = chess.parse_square(start_pos[-2:])
            end_square = chess.parse_square(end_pos[-2:])
            piece_at_start = board.piece_at(start_square)

            if piece_at_start is None:
                raise ValueError(f"No piece at position '{start_pos}'.")
            if board.turn and piece_at_start.color != chess.WHITE:
                raise ValueError(f"You are playing as black, but selected a white piece.")
            elif not board.turn and piece_at_start.color != chess.BLACK:
                raise ValueError(f"You are playing as black, but selected a white piece.")

            # generate UCI move (to prevent conflicts)
            uci_move = chess.Move(start_square, end_square)
            if uci_move not in board.legal_moves:
                raise ValueError("Illegal move. Try again.")

            board.push(uci_move)
            self.valid_move = True
            self.update_pieces()
            self.input_text.set("")

            # trigger ai move if it's the ai's turn
            if board.turn == (self.ai_side == "white"):
                self.ai_make_move()
        except ValueError as e:
            self.valid_move = False
            messagebox.showerror("Error", f"Invalid move: {e}")
            self.input_text.set("")


    def set_player_side(self, side):
        self.player_side = side
        self.ai_side = "white" if side == "black" else "black"
        self.is_ai_turn = self.ai_side == "white"
        # to prevent flip flopping and other garbage that might happen
        self.side_menu.config(state="disabled")

        # if ai is white
        if self.is_ai_turn:
            self.ai_make_move()

    # def ai_make_move(self):
    #     global board
    #     try:
    #         prompt = f"The current board position in FEN notation is: {board.fen()}. You are playing as {self.ai_side}. Provide the move in standard chess notation where the notation is only the piece and where the piece moves to (example, pawn that was on e1 to e2 = e1 e2, knight from h4 to f3 = Nh4 Nf3, queen a1 to a5 = Qa1 Qa5). Be decent at the game, but not an completely optimized player. Play like a 1600 elo player."
    #         response = openai.ChatCompletion.create(
    #             model="gpt-4",
    #             messages=[
    #                 {"role": "system", "content": "You are a chess bot. Provide the move in standard chess notation where the notation is only the piece and where the piece moves to (example, pawn that was on e1 to e2 = e1 e2, knight from h4 to f3 = Nh4 Nf3, queen a1 to a5 = Qa1 Qa5). Be decent at the game, but not an completely optimized player. Play like a 1600 elo player."},
    #                 {"role": "user", "content": prompt}
    #             ]
    #         )
    #         ai_move = response['choices'][0]['message']['content'].strip()
    #         board.push_san(ai_move)
    #         self.update_pieces()
    #     except Exception as e:
    #         # should never happen, its not like depth 24 stockfish
    #         messagebox.showerror("Error", f"AI move failed: {e}")

    def ai_make_move(self):
        global board
        try:
            prompt = f"The current board position in FEN notation is: {board.fen()}. You are playing as {self.ai_side}. Provide the move in the format: 'StartPosition EndPosition' (e.g., 'e2 e4' or 'Nh4 Nf3'). The format must include only the starting and ending positions of the move in standard chess notation. Be decent at the game, but not overly optimized. Make the first available move that you konw is valid in the format aforementioned"
            response = aiplayer.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a chess bot. Provide moves in the format: 'StartPosition EndPosition'. For example: 'e2 e4' or 'Nh4 Nf3'. Play the first avaiable move that you are certain is valid. Make sure that the piece is able to move to that square, and ensure the piece's identity (knight, pawn, king) allows the piece to move to the specific location that is output."},
                    {"role": "user", "content": prompt}
                ]
                
            )
            print(response)
            ai_move = response.choices[0].message.content.strip()

            # parse into process_move esque segmentation
            parts = ai_move.split()
            if len(parts) != 2:
                raise ValueError("AI provided an invalid move format.")

            start_pos = parts[0]
            end_pos = parts[1]

            # validate
            start_square = chess.parse_square(start_pos[-2:])
            end_square = chess.parse_square(end_pos[-2:])
            uci_move = chess.Move(start_square, end_square)

            if uci_move not in board.legal_moves:
                # shouldnt happen contingency
                raise ValueError("AI provided an illegal move.")

            board.push(uci_move)
            self.update_pieces()

        except Exception as e:
            # shouldnt happen contingency
            messagebox.showerror("Error", f"AI move failed: {e}")



    # def ai_process_human(self):
    #     global board
    #     try:
    #         prompt = f"You are recording the chess match of a certain player. This is the current board state in FEN notation: {board.fen()}. Process the user's move to algebraic notation, given that the user's side is {self.player_side}. Respond with the exact move in the form of the piece name, where the piece was and where it would go to (example, pawn that was on e1 to e2 = e1 e2, knight from h4 to f3 = Nh4 Nf3, queen a1 to a5 = Qa1 Qa5). If the player simply says a piece to a certain position and there are no conflicting moves, reference the board state to derive the position of the piece that was played. If there are conflicting moves from the same piece that can move to the same position, where the user does not specify the exact position where the piece was, analyze the board and output the better move for the player."
    #         response = openai.ChatCompletion.create(
    #             model="gpt-4",
    #             messages=[
    #                 {"role": "system", "content": "You are recording the chess match of a certain player. Process the user's move to algebraic notation. Respond with the exact move in the form of the piece name, where the piece was and where it would go to (example, pawn that was on e1 to e2 = e1 e2, knight from h4 to f3 = Nh4 Nf3, queen a1 to a5 = Qa1 Qa5)."},
    #                 {"role": "user", "content": prompt}
    #             ]
    #         )
    #         the_move = response['choices'][0]['message']['content'].strip()
    #         board.push_san(the_move)
    #         self.update_pieces()
    #     except Exception as e:
    #         # should never happen, they should process it fine
    #         messagebox.showerror("Error", f"Player move failed: {e}")

    def ai_process_human(self):
        global board
        try:
            prompt = f"You are recording the chess match of a certain player. This is the current board state in FEN notation: {board.fen()}. Process the user's move to algebraic notation, given that the user's side is {self.player_side}. Respond with the exact move in the form of the piece name, where the piece was and where it would go to (example, pawn that was on e1 to e2 = e1 e2, knight from h4 to f3 = Nh4 Nf3, queen a1 to a5 = Qa1 Qa5). If the player simply says a piece to a certain position and there are no conflicting moves, reference the board state to derive the position of the piece that was played. If there are conflicting moves from the same piece that can move to the same position, where the user does not specify the exact position where the piece was, analyze the board and output the better move for the player. If the player does not explicitly state a move, tell the player to enter the move in the green box."

            response = aiplayer.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are analyzing a chess match. Process the player's move in the format: 'StartPosition EndPosition'. Ensure the move is legal, if not, error out by saying 'The AI determined that the move provided was invalid, please enter the move in the green box below' and respects the board state. For example, valid moves include 'e2 e4' or 'Nb1 Nc3' as opening moves for white, as the first group of characters represents the piece and where the piece currently is, and the second group of characters represents where the move would be moved to."},
                    {"role": "user", "content": prompt}
                ]
            )

            print(response)
            player_move = response.choices[0].message.content.strip()

            parts = player_move.split()
            if len(parts) != 2:
                raise ValueError("AI provided an invalid processed move format, type the move on the green box below.")
     
            start_pos = parts[0]
            end_pos = parts[1]

            start_square = chess.parse_square(start_pos[-2:])
            end_square = chess.parse_square(end_pos[-2:])
            uci_move = chess.Move(start_square, end_square)

            if uci_move not in board.legal_moves:
                raise ValueError("AI processed an illegal move made by the player.")

            board.push(uci_move)
            self.update_pieces()

        except Exception as e:
            messagebox.showerror("Error", f"Player move processing by voice failed, type the move on the green box below: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGame(root)
    root.mainloop()
