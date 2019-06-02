import random as ra
import numpy as np


class Game():

    def __init__(self, size=4, MSet="wasd", winNumb=2048, esc='exit'):

        self.size = size
        self.field = np.zeros((self.size, self.size), dtype=int)
        self.mset = MSet  # ORDER: UP, LFFT, DOWN, RIGHT

        self.goodToGo = True
        self.currentMove = None
        self.points = 0

        # make sure end-command cannot be a move input
        self.esc = esc.lower() if (len(esc) > 1 and type(esc) == str) else 'exit'

        # Make sure the target number cann be reached
        self.winNumb = winNumb if (not (winNumb & (winNumb - 1)) and winNumb != 0) else 2048

        self.moveDict = Game.makeMoveDict(self.mset)


    @staticmethod
    def makeMoveDict(mset):
        if len(set(mset)) != 4:
            print('Invalid move set, has to be four unique chars')
            exit(1)

        tempDict = {}
        rotations = ((1, -1), (0, 0), (-1, 1), (2, 2))
        
        for i in range(4):
            tempDict[mset[i]] = rotations[i]
        return tempDict

    def printField(self):

        print('\nPoints: ', self.points)
        print(self.field)
        return self

    def add2or4(self):
        tempX, tempY = np.where(self.field == 0)
        if len(tempY) != 0:
            ind = ra.randrange(tempX.shape[0])
            self.field[tempX[ind]][tempY[ind]] = int(np.random.choice((2, 4), 1, p=(.8, .2)))
            del (tempX, tempY, ind)
        else:
            self.goodToGo = self.movePossible(self.field.copy())
        return self

    def executeMove(self):
        def getMove():
            move = input('\n' + self.mset + "?\n>>> ").lower()
            if move == self.esc:
                exit(0)

            if len(move) != 1 or move not in self.mset:
                print('Invalid move')
                move = getMove()
            return move

        self.currentMove = getMove()

        rotKey = self.moveDict[self.currentMove]
        temp_field = np.rot90(self.field, rotKey[0])
        
        for i in range(self.size):
            temp_field[i] = self.handleRow(temp_field[i], self.size)

        self.field = np.rot90(temp_field, rotKey[1])
        self.currentMove = None

        del (temp_field, rotKey)
        return self

    def handleRow(self, row, n):
        
        def mergeLine(line):
            temp = line.tolist()  # for changing values inline
            for j in range(len(temp) - 1):
                if (temp[j] == temp[j + 1]):
                    self.points += temp[j]*2
                    temp[j] *= 2
                    temp[j + 1] = 0
            return np.asarray([x for x in temp if x != 0], dtype=int)

        temp_row = np.delete(row, np.where(row == 0))
        newRow = mergeLine(temp_row) if len(temp_row) > 1 else temp_row
        return np.append(newRow, [0 for k in range((n - len(newRow)))])

    def movePossible(self, field):

        def handleRow(row, n):
            def handelMerge(line):
                temp = line.tolist()  # for changing values inline
                for j in range(len(temp) - 1):
                    if (temp[j] == temp[j + 1]):
                        temp[j] = line[j] + line[j + 1]
                        temp[j + 1] = 0
                return np.asarray([x for x in temp if x != 0], dtype=int)
            
            temp_row = np.delete(row, np.where(row == 0))
            newRow = handelMerge(temp_row) if len(temp_row) > 1 else temp_row
            return np.append(newRow, [0 for k in range((n - len(newRow)))])

        notPossibleMoves = 0

        # try every move possible
        for rotKey in self.moveDict.values():
            nowField = field.copy()
            tempField = np.rot90(nowField, rotKey[0])

            for i in range(self.size):
                tempField[i] = handleRow(tempField[i], self.size)

            testField = np.rot90(tempField, rotKey[1])

            if np.equal(field.all(), testField.all()):
                notPossibleMoves += 1

            del (testField, tempField, nowField)
        return notPossibleMoves != len(self.moveDict)

    def play(self):
        print("Welcome to this game of 2048\n"
              f"Move the tiles till you reach {self.winNumb}!\n"
              f"Type '{self.esc}' to stop the game")
        self.add2or4()
        while True:
            if self.winNumb in self.field.flatten():
                self.printField()
                print("Congratulations!")
                c = input("Type 'yes' if you wish to continue playing\n>>> ").lower()
                if 'yes' in c:
                    self.winNumb *= 2
                    print(f'Your new target is {self.winNumb}!\n')
                else:
                    break

            self.add2or4()
            if not self.goodToGo:
                break
            self.printField().executeMove()
        self.printField


def run():
    Game(size=4, MSet="wasd", winNumb=2048, esc='exit').play()
    print("\nGame is over, thank you for playing")

run()
