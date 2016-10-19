'''
Created on Sep 6, 2016

@author: Jacob Brunsting
'''

import crossword_tools
import constants
import crossword_gui
import clue_scraper
import solver
import time

puzzle = crossword_tools.Puzzle()

def main():
    def on_puzzle_retrieval(puzzle):
        """
        Gets a word bank from the user, uses it to solve the provided puzzle,
        and displays the results to the user. Should be called once the user
        has finished generating the puzzle using the puzzle creation window
        
        args:
            puzzle: A crossword_tools.Puzzle object representing the puzzle the
                    user created
        """
        
        if not puzzle:
            user_input = input(constants.NO_SOLUTIONS_STR)
            if user_input == 'y':
                main()
        
        puzzle_line_ids = puzzle.get_line_ids()
        clues_by_line = get_clues_from_user(puzzle, puzzle_line_ids)
        
        possible_words_by_line = {}
        for line_id in puzzle_line_ids:
            possible_words_by_line[line_id] = clue_scraper.get_clue_possible_answers(clues_by_line[line_id], puzzle.lines[line_id].length)
            
        
        print(constants.SOLVING_STR)
        start_time = time.clock()
        solutions = solver.find_solutions(puzzle, possible_words_by_line)
        end_time = time.clock()
        diff = end_time - start_time
        seconds = round(diff)
        mills = round((diff - seconds) * 1000)
        
        if seconds == 1:
            seconds_ending = ''
        else:
            seconds_ending = 's'
            
        if mills == 1:
            mills_ending = ''
        else:
            mills_ending = 's'
            
        print(constants.SOLVE_TIME_STR.format(seconds, seconds_ending, mills, 
                                              mills_ending))
        
        if solutions:
            print(constants.DISPLAYING_SOLUTIONS_STR)
            crossword_gui.display_puzzle_solutions(puzzle, solutions, lambda: main())
        else:
            user_input = input(constants.NO_SOLUTIONS_STR)
            if user_input == 'y':
                main()
    
    width = read_int(constants.PUZZLE_WIDTH_STR, 2)
    height = read_int(constants.PUZZLE_HEIGHT_STR, 2)
    print(constants.DRAW_PUZZLE_STR)
    crossword_gui.display_crossword_generation_window(width, height, 
                                                      on_puzzle_retrieval)

def read_int(message, min_val):
    """
    Reads an integer from the user, prompting the user with the provided 
    message. Continually gives an error message and prompts the user with the
    provided message until they provide valid input, if they do not provide an 
    integer input initially.
    
    args:
        message: The message shown to the user to prompt them to input an
                 integer.
    """
    
    while True:
        try:
            int_input = int(input(message))
            
            if int_input >= min_val:
                return int_input
            else:
                print(constants.TOO_LOW_INPUT_STR.format(min_val))
        except ValueError:
            print(constants.IMPROPER_INPUT_STR)
            
def get_clues_from_user(puzzle, line_ids):
    clues = {}
    for i in line_ids:
        crossword_tools.print_puzzle(puzzle, i)
        clues[i] = input(constants.CLUE_ENTRY_STR)
    return clues

main();