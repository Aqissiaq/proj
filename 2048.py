import random as ra
import numpy as np

# (lambda np,rand:(lambda d,ml,r,ff: (lambda l:lambda k:l(l,k))(lambda p,f:"YOU WON!" if len(list(filter(lambda x:x[1]==2048,np.ndenumerate(f))))>0 else "YOU LOSE!" if all([np.array_equal(f,n) for n in [np.rot90(list(map(ml,np.rot90(f,x[0]))), x[1]) for x in d.values()]]) else (lambda x:p(p,r(np.rot90(list(map(ml,np.rot90(f,x[0]))),x[1]))))(d[input("\033[2J"+str(f)+"\nwasd? ")]))(r(ff)))({"a":(0,0),"w":(1,-1),"s":(-1,1),"d":(2,2)},(lambda l:(lambda x: x+[0]*(4-len(x)))((lambda a:lambda v:a(a,v))(lambda rec,n:(n if len(n)<2 else [n[0]+n[1]]+rec(rec,n[2:]) if n[0]==n[1] else [n[0]]+rec(rec,n[1:])))(list(filter(lambda a:a!=0,l))))),(lambda f: ((lambda a,i,v: a.itemset(i, v) or a)(f,rand.choice(list(map(lambda x:x[0],filter(lambda x:x[1]==0,np.ndenumerate(f))))),2**rand.randint(1,2))) if len(list(filter(lambda x:x[1]==0,np.ndenumerate(f))))>0 else f),np.zeros((4,4),dtype=np.int)))(__import__("numpy"),__import__("random"))

"""
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
I only wanted to try to write a version of the game myself, using the above text as a guide
    found on reddit, but i dont plan on using any of the lambdas
    
# # # # # # 
Also, very much not done at all :)
"""
SIZE = 4
######

def init(s = SIZE):
    return np.zeros((s,s),dtype=int)

def printField(field):
    for line in field:
        print(line)
    return field

def add2or4(field):
    tempX, tempY = np.where(field == 0)
    ind = ra.randrange(tempX.shape[0])
    field[tempX[ind]][tempY[ind]] = int(np.random.choice((2, 4), 1, p=(.8,.2)))
    return field

def test():
    printField(add2or4(init()))

test()


