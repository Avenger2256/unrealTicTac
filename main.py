import sys
import random

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QMessageBox, QVBoxLayout, QComboBox, QLabel


class TicTacToe(QWidget):
    def __init__(self, size=3, level='Hard'):
        super().__init__()
        self.size = size
        self.level = level
        self.init_ui()
    def init_ui(self):
        self.setWindowTitle('Uɴʀᴇᴀʟ TɪᴄTᴀᴄTᴏᴇ')
        self.width = int( 1080 / 5  * self.size)
        self.height = int( 720 / 5 * self.size)
        self.setGeometry(500, 500, self.width, self.height)
        self.layout = QVBoxLayout()
        self.levelSelector = QComboBox()
        self.levelSelector.addItems(['Hard', 'Medium', 'Easy'])
        self.levelSelector.setCurrentText(self.level)
        self.levelSelector.currentTextChanged.connect(lambda lvl: setattr(self, 'level', lvl))
        self.layout.addWidget(QLabel('Выберите уровень сложности'))
        self.layout.addWidget(self.levelSelector)
        self.grid = QGridLayout()
        self.buttons = [[QPushButton(' ') for i in range(self.size)] for i in range(self.size)]
        self.board = [[None for i in range(self.size)] for i in range(self.size)]
        for a in range(self.size):
            for b in range(self.size):
                self.buttons[a][b].setFixedSize(int(self.width / self.size), int(self.height / self.size))
                self.buttons[a][b].clicked.connect(lambda _, x=a, y=b: self.playerMove(x,y))
                self.grid.addWidget(self.buttons[a][b], a, b)
        self.layout.addLayout(self.grid)
        self.setLayout(self.layout)
    def playerMove(self, x, y):
        if self.board[x][y] is None:
            self.board[x][y] = "X"
            self.buttons[x][y].setText("X")
            self.levelSelector.setEnabled(False)
            if self.check('X'):
                self.show_win('player')
                return
            if self.boardFull():
                self.show_win('tie')
                return
            self.aiMove()
    def aiMove(self):
        if self.level == 'Hard':
            self.hardMove()
        elif self.level == 'Medium':
            if random.random() < 0.5:
                self.randomMove()
            else:
                self.hardMove()
        else:
            self.randomMove()
    def hardMove(self):
        bestScore = -float("inf")
        bestMove = None
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] is None:
                    self.board[x][y] = "O"
                    score = self.miniMax(False)
                    self.board[x][y] = None
                    if score > bestScore:
                        bestScore = score
                        bestMove = (x,y)
        if bestMove:
            a, b = bestMove
            self.board[a][b] = 'O'
            self.buttons[a][b].setText("O")
            if self.check('O'):
                self.show_win('ai')
                return
            if self.boardFull():
                self.show_win('tie')
                return
    def randomMove(self):
        empty_cells = [(x, y) for x in range(self.size) for y in range(self.size) if self.board[x][y] is None]
        if empty_cells:
            x, y = random.choice(empty_cells)
            self.board[x][y] = 'O'
            self.buttons[x][y].setText('O')
            if self.check('O'):
                self.show_win('ai')
            elif self.boardFull():
                self.show_win('tie')
    def miniMax(self, isMaximazing):
        if self.check('X'):
            return -1
        elif self.check('O'):
            return 1
        if self.boardFull():
            return 0
        if isMaximazing:
            bestScore = -float("inf")
            for x in range(self.size):
                for y in range(self.size):
                    if self.board[x][y] is None:
                        self.board[x][y] = "O"
                        score = self.miniMax(False)
                        self.board[x][y] = None
                        bestScore = max(score, bestScore)
            return bestScore
        else:
            bestScore = float("inf")
            for x in range(self.size):
                for y in range(self.size):
                    if self.board[x][y] is None:
                        self.board[x][y] = "X"
                        score = self.miniMax(True)
                        self.board[x][y] = None
                        bestScore = min(score, bestScore)
            return bestScore
    def check(self, player):
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for column in range(self.size):
            if all(self.board[row][column] == player for row in range(self.size)):
                return True
        if all(self.board[x][x] == player for x in range(self.size)) or all(self.board[x][2-x] == player for x in range(self.size)):
            return True
        return False
    def boardFull(self):
        return all(all(cell is not None for cell in row) for row in self.board)
    def show_win(self, player):
        msg = QMessageBox()
        msg.setWindowTitle('Gᴀᴍᴇ Oᴠᴇʀ')
        if player == 'player':
            msg.setText('Pʟᴀʏᴇʀ ᴡᴏɴ')
        elif player == 'ai':
            msg.setText('AI ᴡᴏɴ')
        elif player == 'tie':
            msg.setText('Tɪᴇ')
        msg.setStyleSheet('QLabel{min-width: 200px; min-height: 100px}')
        msg.exec()
        self.reset_board()
    def reset_board(self):
        self.levelSelector.setEnabled(True)
        for a in range(self.size):
            for b in range(self.size):
                self.board[a][b] = None
                self.buttons[a][b].setText('')

def init_app():
    app = QApplication(sys.argv)
    game = TicTacToe(size=3)
    game.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    init_app()