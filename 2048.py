import random as ra
import numpy as np

# found on /r/ programminghorror
# (lambda np,rand:(lambda d,ml,r,ff: (lambda l:lambda k:l(l,k))(lambda p,f:"YOU WON!" if len(list(filter(lambda x:x[1]==2048,np.ndenumerate(f))))>0 else "YOU LOSE!" if all([np.array_equal(f,n) for n in [np.rot90(list(map(ml,np.rot90(f,x[0]))), x[1]) for x in d.values()]]) else (lambda x:p(p,r(np.rot90(list(map(ml,np.rot90(f,x[0]))),x[1]))))(d[input("\033[2J"+str(f)+"\nwasd? ")]))(r(ff)))({"a":(0,0),"w":(1,-1),"s":(-1,1),"d":(2,2)},(lambda l:(lambda x: x+[0]*(4-len(x)))((lambda a:lambda v:a(a,v))(lambda rec,n:(n if len(n)<2 else [n[0]+n[1]]+rec(rec,n[2:]) if n[0]==n[1] else [n[0]]+rec(rec,n[1:])))(list(filter(lambda a:a!=0,l))))),(lambda f: ((lambda a,i,v: a.itemset(i, v) or a)(f,rand.choice(list(map(lambda x:x[0],filter(lambda x:x[1]==0,np.ndenumerate(f))))),2**rand.randint(1,2))) if len(list(filter(lambda x:x[1]==0,np.ndenumerate(f))))>0 else f),np.zeros((4,4),dtype=np.int)))(__import__("numpy"),__import__("random"))

"""

# # # #
First we create a two-dimensional 4x4 array as the field.
Then we try to find all indices with zeros and replace one random one of them with a 2 or 4.
Then starts the main game logic.

Moves are always evaluated as a "swipe" to the left so
before each move evaluation we rotate the array accordingly and afterwards we rotate it back.

To evaluate a move first all zeros in the array are removed.
Then we recursively (yay recursive lambdas! ) merge each lines values from left to right.
Afterwards we append zeros to each line until the 4x4 structure is restored.
Then the whole procedure is recursively called again.
Replace random zero, get input, rotate, merge, rotate back and repeat.

EDIT: I forgot. Before the rotate step.
We try to find a 2048 as win condition.
Or we check for each possible step if the result is equal to the current field.
If all four move options result in the same field as the current one.
The player has lost because there is nothing else to do.	


# # # # # # # # # # 
I wanted to try to write a version of the game myself, that code 
    (tho mostly the desciption) the above text as a guide
    minimal lambda :)

"""


class Game():

    def __init__(self, size=4, MSet="wasd", cont=True, points=0, winNumb=2048):
        self.size = size
        self.field = np.zeros((self.size, self.size), dtype=int)
        self.mset = MSet
        self.cont = cont
        self.points = points

        self.currentMove = None

        self.winNumb = Game.validateWinNumb(winNumb)
        self.moveDict = Game.makeMoveDict(self.mset)

        # self.formatter = {
        #     int:
        # }

    @staticmethod
    def validateWinNumb(n):
        if bool(n and not (n & (n - 1))):
            return n
        print("Your target number cannot be reached in this game")
        exit(0)

    @staticmethod
    def makeMoveDict(mset, rotations=((1, -1), (0, 0), (-1, 1), (2, 2))):
        """
        :param mset: which keys to press
        :param rotations: can change the rotation of the matrix, default (UP, LEFT, DOWN, RIGHT)
        :return: moveDict
        """
        if len(set(mset)) != 4:
            print('Invalid move set, has to be four unique chars')
            exit(1)

        tempDict = {}
        for i in range(4):
            tempDict[mset[i]] = rotations[i]
        return tempDict


    def printField(self):
        print('\nPoints: ', self.points)
        print(self.field)
        return self


    def add2or4(self):
        tempX, tempY = np.where(self.field == 0)
        if len(tempY) == 0:
            self.cont = False
            return self
        ind = ra.randrange(tempX.shape[0])
        newVal = int(np.random.choice((2, 4), 1, p=(.8, .2)))
        self.field[tempX[ind]][tempY[ind]] = newVal
        self.points += newVal
        return self


    def executeMove(self):

        def getMove():
            move = input('\n' + self.mset + "?\n>>> ")
            if move == 'esc':    exit(0)

            if len(move) != 1 or move not in self.mset:
                move = getMove()
            return move

        self.currentMove = getMove()

        rotKey = self.moveDict[self.currentMove]
        temp_field = np.rot90(self.field, rotKey[0])

        for i in range(self.size):
            # print(f"row{i}", temp_field[i])
            temp_field[i] = self.handleRow(temp_field[i], self.size)

        self.field = np.rot90(temp_field, rotKey[1])
        self.currentMove = None
        return self


    def handleRow(self, row, n):
        temp_row = np.delete(row, np.where(row == 0))
        newRow = self.mergeLine(temp_row) if len(temp_row) > 1 else temp_row
        return np.append(newRow, [0 for k in range((n - len(newRow)))])


    def mergeLine(self, line):
        temp = line.tolist()  # for changing values inline
        rtn = []  # Gather the values to be returned

        for j in range(len(temp) - 1):
            if (temp[j] == temp[j + 1]):
                sc = line[j] + line[j + 1]
                self.points += (sc)
                temp[j] = sc;
                temp[j + 1] = 0

            if temp[j] != 0:    rtn.append(temp[j])
        # Try to add the last elemet in the list
        if temp[-1] != 0:   rtn.append(temp[-1])

        return np.asarray(rtn, dtype=int)


    def movePossible(self):
        #TODO: make this methos a part of the game
        # game does not end when there are no possible moves left
        a = '''

        def handleRow(row, n):
            temp_row = np.delete(row, np.where(row == 0))
            newRow = handelMerge(temp_row) if len(temp_row) > 1 else temp_row
            return np.append(newRow, [0 for k in range((n - len(newRow)))])

        def handelMerge(line):
            temp = line.tolist();
            rtn = []

            for j in range(len(temp) - 1):
                if (temp[j] == temp[j + 1]):
                    temp[j] = line[j] + line[j + 1]
                    temp[j + 1] = 0
                if temp[j] != 0:    rtn.append(temp[j])

            if temp[-1] != 0:   rtn.append(temp[-1])
            return np.asarray(rtn, dtype=int)

        nowField = self.field.copy()
        print("NOW\n", nowField)

        for rotKey in self.moveDict.values():
            print(rotKey)
            temp_field = np.rot90(nowField, rotKey[0])

            for i in range(self.size):
                # print(f"row{i}", temp_field[i])
                temp_field[i] = handleRow(temp_field[i], self.size)

            testField = np.rot90(temp_field, rotKey[1])
            print("TEST\n", testField)

            if np.equal(nowField.all(), testField.all()):
                return False
        return True
        '''
        return self

    def play(self, n=20):
        print("Welcome to this game of 2048\n"
              f"Move the tiles till you reach {self.winNumb}!")

        self.add2or4()
        while (self.cont):

            if self.winNumb in self.field.flatten():
                self.printField()
                print("Congratulations!")
                c = input("Type 'yes' if you wish to continue playing\n>>> ").lower()
                if 'yes' in c:
                    self.winNumb *= 2
                    print(f'Your new target is {self.winNumb}!\n')
                else:
                    break

            self.add2or4().printField().executeMove()
        self.printField()


def run():
    game = Game(size=3, MSet='wasd', winNumb=16)
    game.play()
    # Game().play()
    print("\nGame is over, thank you for playing")


run()
