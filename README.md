# solve_sudoku
This project solves a sodoku board.  
To run, simply input a board as a single string read from left-
to-right, then top-to-bottom.  

For example, if we have the board:  
![board](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Sudoku_Puzzle_by_L2G-20050714_standardized_layout.svg/250px-Sudoku_Puzzle_by_L2G-20050714_standardized_layout.svg.png)  
Then we would have:  
`input_str = "530 070 000 600 195 000 098 000 060 800 060 003 400 803 001 700 020 006 060 000 280 000 419 005 000 080 079"`  
Then to run the program, we would run on the command line:  
`python solve.py [input_str]`  
For example, if we run this using the input string above, we get the following output:  
```
1 solutions found


Solution #1

534678912
672195348
198342567
859761423
426853791
713924856
961537284
287419635
345286179
```
