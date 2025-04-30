import tkinter as tk
from qiskit import QuantumCircuit, Aer, execute
import random

class QuantumTicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Quantum Tic-Tac-Toe")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.board = [[[] for _ in range(3)] for _ in range(3)]
        self.player = "X"
        self.superpositions = []  # Stores tuples like (row, col, player)
        self.selection = []

        self.label = tk.Label(self.window, text="Player X's turn", font=('Arial', 16))
        self.label.pack()

        self.frame = tk.Frame(self.window)
        self.frame.pack()
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.frame, text="", width=6, height=3,
                                   font=('Arial', 24), command=lambda r=i, c=j: self.make_move(r, c))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

        self.collapse_btn = tk.Button(self.window, text="Collapse Superpositions", font=('Arial', 14), command=self.collapse_board)
        self.collapse_btn.pack(pady=10)

        self.window.mainloop()

    def make_move(self, row, col):
        if len(self.board[row][col]) < 2:
            self.board[row][col].append(self.player)
            self.superpositions.append((row, col, self.player))
            self.buttons[row][col].config(text=self.get_cell_text(row, col))
            self.selection.append((row, col))
            if len(self.selection) == 2:
                self.player = "O" if self.player == "X" else "X"
                self.label.config(text=f"Player {self.player}'s turn")
                self.selection = []

    def get_cell_text(self, row, col):
        if self.board[row][col]:
            return "/".join(self.board[row][col]) + "~"
        return ""

    def collapse_board(self):
        backend = Aer.get_backend('qasm_simulator')
        collapsed_board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                if len(self.board[i][j]) == 2:
                    qc = QuantumCircuit(1, 1)
                    qc.h(0)
                    qc.measure(0, 0)
                    result = execute(qc, backend, shots=1).result()
                    outcome = int(list(result.get_counts().keys())[0])
                    collapsed_board[i][j] = self.board[i][j][outcome]
                elif len(self.board[i][j]) == 1:
                    collapsed_board[i][j] = self.board[i][j][0]

        self.board = collapsed_board
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=self.board[i][j])

        winner = self.check_winner()
        if winner:
            self.label.config(text=f"Player {winner} wins!")
            self.disable_buttons()
        else:
            self.label.config(text="Game collapsed. No winner.")

    def disable_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return self.board[0][2]
        return None

# Run the game
QuantumTicTacToe()
