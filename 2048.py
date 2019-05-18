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

    def __init__(self, size=4, MSet="wasd", cont=True, win=False, points=0):
        self.size = size
        self.field = np.zeros((self.size, self.size), dtype=int)
        self.mset = MSet
        self.cont = cont
        self.win = win
        self.points = points

        self.moveDict = Game.makeMoveDict(self.mset)
        self.currentMove = None

        # self.formatter = {
        #     int:
        # }

    @staticmethod
    def makeMoveDict(mset, rotations=((1,-1), (0,0), (-1, 1), (2, 2))):
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
        ind = ra.randrange(tempX.shape[0])
        self.field[tempX[ind]][tempY[ind]] = int(np.random.choice((2, 4), 1, p=(.8,.2)))
        return self


    def CheckWinAndContinue(self):
        if 2048 in self.field.flatten():
            self.win = True
            print("You have won!")
            c = input("Type 'yes' if you wish to continue playing\t").lower()
            self.cont = True if c == 'yes' else False
        # return not self.win or self.cont
        return self

    def getMove(self):
        move = input(self.mset + "?\t")
        if len(move) != 1 or move not in self.mset:
             move = self.getMove()
        self.currentMove = move
        return self


    def executeMove(self):
        # todo: calc points

        #self.moveDict = {
        #    "a": (0,0),
        #    "w": (1,-1),
        #    "s": (-1,1),
        #    "d": (2,2)
        #    }

        rotKey = self.moveDict[self.currentMove]

        # todo: add rotation to eval a swipe and rot back


        for i in range(self.size):
            self.field[i] = Game.mergeLine(self.field[i], self.size)


        self.currentMove = None
        return self

    @staticmethod #maybe not static
    def mergeLine(line, n):
        # todo: calc points
        # todo: remove zeros not at the end too
        temp = np.trim_zeros(line)
        # todo: add funtunality to merge tiles

        return np.append(temp, [0 for i in range((n-len(temp)))])


def run(n=3):
    # todo: add  while (not game.win or game.cont): continue playing

    game = Game(MSet='1235')
    game.add2or4()
    for i in range(n):
        print("i",i)
        game.add2or4().printField()\
            .getMove().executeMove()
    game.printField()
    print(f"You got {game.points} points!")

run(5)


