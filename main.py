from puzzle import Puzzle
from time import time

puz = Puzzle([
    [0,0,0,2,7,3,9,0,5],
    [5,0,0,0,0,9,0,3,7],
    [7,9,0,4,0,0,0,0,2],
    [0,8,0,5,2,6,4,0,0],
    [1,6,5,8,0,0,0,0,0],
    [0,0,2,0,9,0,5,0,6],
    [0,0,1,0,0,5,3,6,0],
    [9,3,8,0,6,2,0,0,0],
    [0,0,0,9,3,0,0,2,0]
])

if __name__ == "__main__":
    start = time()
    print(puz)
    puz.solve_puzzle()
    print(puz)
    end = time()
    print("Puzzle solved in " + str(end-start) + " seconds.")