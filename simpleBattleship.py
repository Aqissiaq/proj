# coding=utf-8
from random import randrange
from time import sleep
# making a small batleship game... yea,let's try that

class Board():

	# the printed borad only prints *, and Xes, O if a ship has been found there
	# the ships set contains tuple coordinates of where the 1x1 ships are
	# need a better way tos store ships... dicts?
	# key as a coordinate for the "first" tile?
	# tuppes of tuppels in the set? --> gives double forloops
	#   Yes can do
	#   t = ((x,y),) for a tuple containing one tuple
	# NO LIST IN ANY SETS AT ANY LEVEL --> gives TypeError

	#TODO - make changes to the actual board

	def __init__(self, size):
		self.size = size
		self.board = [(["*" for x in range(self.size)][:])for y in range(self.size)]
		self.ships = set()

	def __str__(self):
		return self.make_print_board()

	def make_print_board(self):
		board_str = ""

		rowNumbStr = "  "
		for j in range(self.size):	rowNumbStr += " " + str(j+1) + " "
		# print(rowNumbStr)
		board_str += rowNumbStr + "\n"

		sepline = " |-" + "---"*self.size
		# print(sepline)
		board_str += sepline + "\n"

		for rowIndex in range(self.size):
			row = self.board[rowIndex]
			# print(rowIndex+1, end = "| ")
			board_str += str(rowIndex + 1) + "| "

			for colIndex in range(self.size):
				tile = row[colIndex]
				tile = " " + tile if colIndex != 0 else tile
				# print(tile, end = " ")
				board_str += tile + " "

			# print("\n" + sepline)
			board_str += "\n" + sepline + "\n"

		# print(rowNumbStr)
		board_str += rowNumbStr + "\n"

		return board_str

	def placeShip(self, row, col):
		row,col = int(row), int(col)
		if not (row,col) in self.ships:
			self.ships.add((row,col))
			return True
		else:
			print("There is already a ship here")
			return False

	def guessShip(self,guess): #guess here is a rowcol tuple
		isHit = False
		if self.board[guess[0]][guess[1]] != "*":
			print("You found have already guessed that tile!")

		elif guess in self.ships:
			self.board[guess[0]][guess[1]] = "O"
			print("Congratulations! You found a ship!")
			isHit = True

		else:
			self.board[guess[0]][guess[1]]= "X"
			print("You missed!")

		return isHit

	def validate_dim(self, row, col):
		try:
			_row = int(row)
			_col = int(col)

		except ValueError or SyntaxError or TypeError:
			print("You have to give integers, separated by ','")
			return False

		if _row not in range(1,self.size + 1) or _col not in range(1,self.size + 1):
			print("Index out of range")
			return False

		return True

	@staticmethod
	def convertRowColTupleToSTR(_tuple):
		return "(" + str(_tuple[0] + 1) + ", " + str(_tuple[1] + 1) + ")"


class Player():

	total_players = 0

	def __init__(self, boardSize, name = ""):
		Player.total_players += 1
		self.name = name if name != "" else "Player" + str(Player.total_players)
		self.myBoard = Board(boardSize)
		self.numShipsFound = 0

	def place1x1Ship(self):
		print("Where do you want to place your 1x1 ship?")
		r,c = self.getRowCol()
		while not self.myBoard.placeShip(r, c):
			print("Choose another place for your 1x1 ship!")
			r,c = self.getRowCol()

	def makeGuess(self):
		print("Guess where the other player has placed a ship!")
		return self.getRowCol()

	def getRowCol(self):
		rowcol = input("Give (row, col):\n").replace(" ", '').split(',')

		while len (rowcol) < 2:
			rowcol = input("Give both row and col as (row, col):\n").replace(" ", '').split(',')

		row,col = rowcol[0],rowcol[1]

		while not self.myBoard.validate_dim(row,col):
			rowcol = input("Try again, format row, col:\n").replace(" ", '').split(',')
			row,col = rowcol[0],rowcol[1]

		rowI = int(row) - 1
		colI = int(col) - 1
		return rowI,colI


class ComputerPlayer(Player):

	totalPlayers = 0

	def __init__(self, boardSize):
		ComputerPlayer.totalPlayers += 1
		Player.__init__(self, boardSize=boardSize, name = "Autoplayer" + str(ComputerPlayer.totalPlayers))
		self.placements = set()
		self.guesses = set()

	def place1x1Ship(self):
		print("Placing a 1x1 ship...")
		rctuple = self.getRandomRowCol()
		while rctuple in self.placements:
			rctuple = self.getRandomRowCol()
		self.placements.add(rctuple)
		r,c = rctuple
		self.myBoard.placeShip(r, c)
		sleep(.4)

	def makeGuess(self):
		guess = self.getRandomRowCol()
		while guess in self.guesses:
			guess = self.getRandomRowCol()
		self.guesses.add(guess)
		print("Guessing where you placed a ship...")
		print(Board.convertRowColTupleToSTR(guess))
		sleep(.5)
		return guess

	def getRandomRowCol(self):
		return randrange(self.myBoard.size),randrange(self.myBoard.size)


class Game():

	def __init__(self):
		boardSize, twoPlayer = self.gameSetup()
		self.boardSize = boardSize
		self.player1, self.player2 = self.makePlayers(twoPlayer)
		self.winner = None

	@staticmethod
	def gameSetup():

		def validatePlayers(num):
			rtn = True
			try:
				num = int(num)
				if not (num == 0 or num == 1 or num == 2):
					print("You must write 0, 1, or 2")
					rtn = False
			except ValueError or SyntaxError or TypeError:
				print("Invalid input")
				rtn = False
			return rtn

		def getAndValidateSize():
			try:
				sze = int(input("Choose n: "))
				if sze < 3 or sze > 100:
					raise ValueError
				_size = sze
			except ValueError or SyntaxError or TypeError:
				print("Not Allowed :/\n")
				print("Defaulting to 6x6 board")
				_size = 6
			return _size

		def decidePlayers():
			print("How many human players?")
			answer = input("Answer 0, 1, or 2:\n")
			while not validatePlayers(answer):
				answer = (input("Answer 0, 1, or 2:\n"))
			return int(answer)

		print("Welcome this simple game of Battleship!")
		print("The board is a nxn square")
		size = getAndValidateSize()
		noPlayers = decidePlayers()

		return size, noPlayers

	def makePlayers(self, noPlayers):

		p1, p2 = None, None

		if noPlayers == 0:
			print("Two (dummy) computers playing against each other")
			p1 = ComputerPlayer(boardSize = self.boardSize)
			p2 = ComputerPlayer(boardSize = self.boardSize)

		else:
			name = input("Give player 1 a name:\n")
			p1 = Player(boardSize = self.boardSize, name=name)

			if noPlayers == 1:
				print("Playing against a (dummy) computer:")
				p2 = ComputerPlayer(boardSize = self.boardSize)

			else:
				name = input("Give player 2 a name:\n")
				p2 = Player(boardSize = self.boardSize, name=name)

		return p1, p2

	def beforePlay(self):

		def validateNoShips(num, _max):
			isValid = True
			try:
				num = int(num)
				if num >= (_max//2):
					print("Choose a smaller number")
					isValid = False
				elif num < 1:
					print("You must pick a number bigger than 0")
					isValid = False

			except ValueError or SyntaxError or TypeError:
				print("Invalid input!")
				isValid = False

			return isValid

		def setNoShips(_max):
			print("\nThe Boards are squares with size " + str(self.boardSize) + "x" + str(self.boardSize))

			noShips = input("How many ships does each player place?\n")
			while not validateNoShips(noShips, _max):
				noShips = input("How many ships does each player place?\n")
			return int(noShips)

		def placeShips(player, num):
			print("It is " + player.name + "'s turn to place ships")
			print(player.myBoard)
			for i in range(num):
				player.place1x1Ship()

		shipsToFind = setNoShips(_max=(self.boardSize)**2)

		placeShips(self.player1, shipsToFind)
		print("\n"*20, "-----"*self.boardSize,"\n"*20, sep = "")

		placeShips(self.player2, shipsToFind)
		print("\n"*20, "-----"*self.boardSize,"\n"*20, sep = "")

		print("READY TO START!!")
				
		return shipsToFind

	def play(self):
		toFind = self.beforePlay()
		win = False;    rnd = 0;    switch = True

		while not win:
                        
			if switch:     rnd += 1

			print("\nRound",rnd)
			print(self.player1.name,"has found", self.player1.numShipsFound, "ship(s)",end = ' ')
			print("while",self.player2.name,"has found", self.player2.numShipsFound, "ship(s)\n")

			currentPlayer = self.player1 if switch else self.player2
			currentOpponent = self.player1 if not switch else self.player2

			print("It is " + currentPlayer.name + "'s turn")
			print(currentOpponent.myBoard)

			guess = currentPlayer.makeGuess()

			while currentOpponent.myBoard.guessShip(guess):
				currentPlayer.numShipsFound += 1
				if (currentPlayer.numShipsFound == toFind):
					sleep(.5);  print("\nYou found all the ships!");    win = True
					break

				print("It is "+ currentPlayer.name + " turn once more!")
				print(currentOpponent.myBoard)

				guess = currentPlayer.makeGuess()

			print("At the end of your turn, the board you're playing at lookes like this")
			print(currentOpponent.myBoard)

			sleep(1)

			print("\n\n\n" + "======"*self.boardSize + "\n" + "======"*self.boardSize + "\n\n")
			switch = not switch

		self.winner = self.player1 if self.player1.numShipsFound == toFind else self.player2
		self.endGame(rnd)

	def endGame(self, rounds):
		print("\nThe winner is", self.winner.name, "after", rounds, "rounds!!")
		answer = input("Do you wish to view the coordinates of the winner's ships? (y/n)\n").lower()
		if answer == 'y' or answer == 'yes':
			print(self.winner.name + " had their ships at:")
			for coord in self.winner.myBoard.ships:
				print(Board.convertRowColTupleToSTR(coord), end = "  ")

		print("\nThanks for playing, have a nice day!")
		sleep(2)


def main():
	game = Game()
	game.play()

if __name__ == '__main__':
	main()
