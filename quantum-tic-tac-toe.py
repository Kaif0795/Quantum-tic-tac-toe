import tkinter as tk
from qiskit import QuantumCircuit, Aer, execute
import random

class QuantumTicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Tic-Tac-Toe")
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()
        self.turn = 'X'
        self.qc = QuantumCircuit(9, 9)
        self.simulator = Aer.get_backend('qasm_simulator')
        
    def create_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text='', font=('Arial', 24), height=2, width=5,
                                               command=lambda r=i, c=j: self.make_move(r, c))
                self.buttons[i][j].grid(row=i, column=j)
    
    def make_move(self, row, col):
        if self.board[row][col] is None:
            self.board[row][col] = self.turn
            self.buttons[row][col].config(text=self.turn)
            self.apply_quantum_logic(row, col)
            self.turn = 'O' if self.turn == 'X' else 'X'

    def apply_quantum_logic(self, row, col):
        qbit = row * 3 + col
        if random.choice([True, False]):
            self.qc.h(qbit)  # Apply Hadamard gate for superposition
        self.qc.measure(qbit, qbit)
        self.run_quantum_circuit()
        self.check_winner()
    
    def run_quantum_circuit(self):
        compiled_circuit = self.qc.compile(self.simulator)
        result = execute(compiled_circuit, backend=self.simulator, shots=1).result()
        counts = result.get_counts()
        print("Quantum Result:", counts)
    
    def check_winner(self):
        winning_states = [
            [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]
        ]
        for state in winning_states:
            values = [self.board[r][c] for r, c in state]
            if values[0] is not None and values.count(values[0]) == 3:
                self.display_winner(values[0])
                return
    
    def display_winner(self, winner):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state=tk.DISABLED)
        tk.Label(self.root, text=f"{winner} Wins!", font=('Arial', 20), fg='red').grid(row=3, column=0, columnspan=3)

if __name__ == "__main__":
    root = tk.Tk()
    game = QuantumTicTacToe(root)
    root.mainloop()
