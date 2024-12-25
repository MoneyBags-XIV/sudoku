class Puzzle:
    def __init__(self, grid):
        self.grid = grid
        self.candidates = [[[x+1 for x in range(9) if self.could_be(j, k, x+1)] for k in range(9)] for j in range(9)]

    
    def solve_puzzle(self):
        while True:
            ans = self.grid
            adsf = self.candidates

            self.solve_by_elimination()
            self.solve_by_box()
            self.solve_by_row()
            self.solve_by_column()
            self.update_candidates()

            print("\n")

            if self.grid == ans and self.candidates == adsf:
                return
    
    def update_candidates(self):
        for i, row in enumerate(self.grid):
            for j, num in enumerate(row):
                for k in self.candidates[i][j]:
                    if not self.could_be(i, j, k):
                        self.candidates[i][j].remove(k)

    
    def solve_by_box(self):
        iterations = 0
        nums_found = 0
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
                        nums_found += 1
                    
                    elif len(possible_indexes) > 1:
                        asdf = [x[0] for x in possible_indexes]
                        jkl = [x[1] for x in possible_indexes]

                        if len(set(asdf)) <= 1:
                            for i in range(9):
                                if i in jkl:
                                    continue
                                try:
                                    self.candidates[asdf[0]][i].remove(num+1)
                                except:
                                    pass
                        
                        elif len(set(jkl)) <= 1:
                            for i in range(9):
                                if i in asdf:
                                    continue
                                try:
                                    self.candidates[i][jkl[0]].remove(num+1)
                                except:
                                    pass

            
            iterations += 1
            
            if ans == self.grid:
                print("Iterating by box found " + str(nums_found) + " numbers over " + str(iterations) + " iterations.")

                return
            
            self.grid = ans

    def solve_by_row(self, column=False):
        iterations = 0
        nums_found = 0
        while True:
            ans = self.grid

            # print(self.grid)

            for i, row in enumerate(self.grid):
                # print(row)
                for k in range(9):
                    # print(str(k))
                    # print(row)
                    if k+1 in row:
                        continue
                    possible_indexes = []
                    for j, num in enumerate(row):
                        if self.could_be(i, j, k+1):
                            possible_indexes.append(j)
                    
                    if len(possible_indexes) == 1:
                        ans[i][possible_indexes[0]] = k+1
                        nums_found += 1

                    elif len(possible_indexes) > 1:
                        adsf = [get_box(i, x) for x in possible_indexes]
                        possible_indexes = [[i, x] for x in possible_indexes]

                        if len(set(adsf)) <= 1:
                            box_num = adsf[0]

                            for i in range(3):
                                for j in range(3):
                                    rowjkl = 3*(box_num//3) + i
                                    col = 3*(box_num%3) + j
                                    if [rowjkl, col] in possible_indexes:
                                        continue
                                    try:
                                        self.candidates[rowjkl, col].remove(k+1)
                                    except:
                                        pass

            
            iterations += 1
                
            if ans == self.grid:
                if column:
                    print("Iterating by column found " + str(nums_found) + " numbers over " + str(iterations) + " iterations.")
                else:
                    print("Iterating by row found " + str(nums_found) + " numbers over " + str(iterations) + " iterations.")

                return
            
            self.grid = ans
    
    def solve_by_column(self):
        self.flip()
        self.solve_by_row(column=True)
        self.flip()

    def solve_by_elimination(self):
        iterations = 0
        nums_found = 0
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
                        nums_found += 1
            
            iterations += 1

            if ans == self.grid:
                print("Iterating by elimination found " + str(nums_found) + " numbers over " + str(iterations) + " iterations.")
                return
            
            self.grid = ans

    def flip(self):
        ans = [[] for x in range(9)]
        for i, row in enumerate(self.grid):
            for j, num in enumerate(row):
                ans[j].append(num)
        self.grid = ans

        ans = [[] for x in range(9)]
        for i, row in enumerate(self.candidates):
            for j, num in enumerate(row):
                ans[j].append(num)
        self.candidates = ans

    def could_be(self, row_number, column_number, number):
        print(row_number)
        print(column_number)
        print(number)
        if self.number_in_column(number, column_number):
            return
        
        if number in self.grid[row_number]:
            return
        
        box_num = get_box(row_number, column_number)
        if self.number_in_box(number, box_num):
            return
        
        if self.grid[row_number][column_number] != 0:
            return
        
        try:
            if not number in self.candidates[row_number][column_number]:
                return
        except:
            pass
        
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
                if num != 0:
                    ans += "| " + str(num) + " "
                else:
                    ans += "|   "
            ans += "|\n"
            if not (i+1)%3:
                ans += ("+ - - - - - " * 3) + "+\n"
            else:
                ans += ("- " * 19) + "\n"
        
        return ans

def get_box(row_number, column_number):
    ans = (column_number//3) + 3*(row_number//3)
    return ans