class Puzzle:
    def __init__(self, grid):
        self.grid = grid
    
    def solve_puzzle(self):
        while True:
            ans = self.grid
            self.solve_by_elimination()
            self.solve_by_box()
            self.solve_by_row()
            self.solve_by_column()

            if self.grid == ans:
                return
    
    def solve_by_box(self):
        while True:
            ans = self.grid

            for box_num in range(9):
                for num in range(9):
                    if self.number_in_box(num+1, box_num):
                        continue

                    possible_indexes = []

                    for i in range(3):
                        for j in range(3):
                            row = 3*(box_num//3) + i
                            col = 3*(box_num%3) + j
                            if self.could_be(row, col, num+1):
                                possible_indexes.append([row, col])
                            
                    if len(possible_indexes) == 1:
                        ans[possible_indexes[0][0]][possible_indexes[0][1]] = num + 1
            
            if ans == self.grid:
                return
            
            self.grid = ans

    def solve_by_row(self):
        while True:
            ans = self.grid

            for i, row in enumerate(self.grid):
                for k in range(9):
                    if k+1 in row:
                        continue
                    possible_indexes = []
                    for j, num in enumerate(row):
                        if self.could_be(i, j, k+1):
                            possible_indexes.append(j)
                    
                    if len(possible_indexes) == 1:
                        ans[i][possible_indexes[0]] = k+1
                
            if ans == self.grid:
                return
            
            self.grid = ans
    
    def solve_by_column(self):
        self.flip()
        self.solve_by_row()
        self.flip()

    def solve_by_elimination(self):
        while True:
            ans = self.grid

            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    could_be = []
                    for k in range(9):
                        if self.could_be(i, j, k+1):
                            could_be.append(k+1)
                    
                    if len(could_be) == 1:
                        ans[i][j] = could_be[0]

            if ans == self.grid:
                return
            
            self.grid = ans

    def flip(self):
        ans = [[] for x in range(9)]
        for i, row in enumerate(self.grid):
            for j, num in enumerate(row):
                ans[j].append(num)
        self.grid = ans

    def could_be(self, row_number, column_number, number):
        if self.number_in_column(number, column_number):
            return
        
        if number in self.grid[row_number]:
            return
        
        box_num = get_box(row_number, column_number)
        if self.number_in_box(number, box_num):
            return
        
        if self.grid[row_number][column_number] != 0:
            return
        
        return True

    def number_in_column(self, number, column_number):
        for row in self.grid:
            if number == row[column_number]:
                return True
        return
    
    def number_in_box(self, number, box_number):
        for i in range(3):
            for j in range(3):
                if self.grid[i + 3*(box_number//3)][j + 3*(box_number%3)] == number:
                    return True
        return
    
    def __str__(self):
        ans = ("+ - - - - - " * 3) + "+\n"

        for i, row in enumerate(self.grid):
            for num in row:
                ans += "| " + str(num) + " "
            ans += "|\n"
            if not (i+1)%3:
                ans += ("+ - - - - - " * 3) + "+\n"
            else:
                ans += ("- " * 18) + "\n"
        
        return ans

def get_box(row_number, column_number):
    ans = (column_number//3) + 3*(row_number//3)
    return ans