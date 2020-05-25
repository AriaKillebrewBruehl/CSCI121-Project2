# File: SpellingBee.py

"""
This program generates the layout of a SpellingBee game based on the users input. 
The possible solutions to this puzzle are displayed in addititon to the number of 
solutions and the total possible points. Pangrams are displayed in blue. 
"""

from english import ENGLISH_WORDS
from pgl import GWindow, GCompound, GLabel
from DrawHexagon import createHexagon 
import random

# Constants used in Milestone #1

GWINDOW_WIDTH = 1000            # These constants specify the width
GWINDOW_HEIGHT = 310            # and height of the graphics window

BEEHIVE_X = 150                 # These constants specify the center
BEEHIVE_Y = 150                 # of the beehive figure

HEX_SIDE = 40                   # The length of a hexagon side
HEX_SEP = 76                    # The distance between hexagon centers
HEX_LABEL_DY = 14               # Offset to the label baseline

LABEL_FONT = "36px bold 'Helvetica Neue','Sans-Serif'"
CENTER_HEX_COLOR = "#FFCC33"
OUTER_HEX_COLOR = "#DDDDDD"

# Constants used in Milestone #3

WORDLIST_X = 300                # Starting x coordinate of the wordlist
WORDLIST_Y = 20                 # Baseline of first word listed
WORDLIST_DX = 100               # Separation between wordlist columns
WORDLIST_DY = 17                # Separation between wordlist rows
SCORE_BASELINE = 10             # Distance from bottom to score baseline
SCORE_WORDLIST_SEP = 20         # Spacing between wordlist and scores

WORDLIST_FONT = "16px 'Helvetica Neue','Sans-Serif'"
PANGRAM_COLOR = "Blue"
gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
beehive = None # Create beehive variable
# Main program

def isLegalPuzzle(puzzle): # Cehck if input is a leagal puzzle 
    global shuffleword
    
    if notRepeating(puzzle) and len(puzzle) == 7: # Characters must not repeate and puzzle must be 7 characters 
        shuffleword = puzzle.upper() # Create variable for shuffle function 
        displayWordsList(puzzle) # If puzzle is legal display words list 
        beehive = createBeehive(puzzle) # If puzzle is legal create beehive 
        gw.add(beehive, BEEHIVE_X, BEEHIVE_Y) # Is puzzle is legal add beehive 
    else: # Ask user to enter new puzzle if puzzle not legal 
        print("This is not a legal puzzle. Please try again.")  
        isLegalPuzzle(input("Enter puzzle letters with center hex first:"))
    
def notRepeating(puzzle):
    for i in range(len(puzzle)):
        if puzzle[i] in puzzle[:i] or puzzle[i] in puzzle[i + 1:]: # Check if a character is present multiple times 
            return False 
        else: 
            return True         
    
def createBeehive(puzzle):
    global beehive
    cell = None
    puzzle = puzzle.upper()
    """
    Creates a GCompound that contains the objects necessary to display
    the beehive structure for the Spelling Bee.  The puzzle parameter
    is a seven-letter string that defines the labels on the hexagons.
    The first letter goes in the center hexagon; each subsequent letter
    goes in a hexagon whose center is HEX_SEP pixels from the center at
    angles of 30, 90, 150, 210, 270, and 330 degrees as the letters
    move counterclockwise around the hexagon.
    """
    beehive = GCompound() # Create GCompund
    cell = createHexagon(HEX_SIDE)
    cell.setFilled(True)
    cell.setColor(CENTER_HEX_COLOR)
    beehive.add(cell) # Add center cell 
    letter = GLabel(puzzle[0])
    letter.setFont(LABEL_FONT)
    beehive.add(letter, cell.getX() - letter.getWidth()/2, cell.getY() + HEX_LABEL_DY) # Add center letter 
    
    for i in range(6): # Add other cells and letters 
         cell = createHexagon(HEX_SIDE)
         cell.setFilled(True)
         cell.setColor(OUTER_HEX_COLOR)
         cell.movePolar(HEX_SEP, 30 + 60*i)
         beehive.add(cell)
         letter = GLabel(puzzle[i + 1])
         letter.setFont(LABEL_FONT)
         beehive.add(letter, cell.getX() - letter.getWidth()/2, cell.getY() + HEX_LABEL_DY)

    shuffle = createHexagon(HEX_SIDE) # Create shuffle button 
    shuffle.setFilled(True)
    shuffle.setColor(CENTER_HEX_COLOR)
    shuffle.movePolar(HEX_SEP * 1.75, -120)
    beehive.add(shuffle)
    letter = GLabel("SHUFFLE")
    letter.setFont("12px bold 'Helvetica Neue','Sans-Serif'")
    beehive.add(letter, shuffle.getX() - letter.getWidth()/2, shuffle.getY() + letter.getAscent()/2)
    
    return beehive # Return completed beehive 

def shuffle(e): # Function to shuffle hexs
    global shuffleword, beehive
    
    obj = gw.getElementAt(e.getX(), e.getY()) # 
    if obj is not None: 
        letters = shuffleword[1:7] # Only shuffle after first letter 
        letters = [char for char in letters] # Break shuffleword into list 
        random.shuffle(letters)
        letters = "".join(letters) # Create new shuffled string 
        for i in range(6): # Add new cells and letters 
         cell = createHexagon(HEX_SIDE)
         cell.setFilled(True)
         cell.setColor(OUTER_HEX_COLOR)
         cell.movePolar(HEX_SEP, 30 + 60*i)
         beehive.add(cell)
         letter = GLabel(letters[i])
         letter.setFont(LABEL_FONT)
         beehive.add(letter, cell.getX() - letter.getWidth()/2, cell.getY() + HEX_LABEL_DY)
        
def isLegalEntry(word, puzzle): # Check to see if words are in puzzle 
    for ch in word:
        if ch not in puzzle:
           return False 
    if len(word) < 4:
        return False
    elif puzzle[0] not in word:
        return False
    else:
        return True 
    
def displayWordsList(puzzle):
    puzzle = puzzle.lower()
    legalWords = [] # Create blank list of words 
    points = 0
    x = WORDLIST_X
    i = 0
    
    for word in ENGLISH_WORDS:
        if isLegalEntry(word, puzzle): 
            legalWords.append(word) # Add leagal words to legalWords 
    
    def isPangram(word): # Check to see if Pangram 
        letters = 0
        for ch in puzzle:
            if ch in word:
                letters += 1
        if letters == len(puzzle):
            return True
        else:
            return False
    
    for word in legalWords:
        points += len(word) - 3 # Number of points per word 
        
        if isPangram(word): # Make changes if pangram
            points += 7
            line = GLabel(word)
            line.setColor(PANGRAM_COLOR)
            line.setFont(WORDLIST_FONT)
        else:
            line = GLabel(word)
            line.setFont(WORDLIST_FONT)
        y = WORDLIST_Y + WORDLIST_DY * i
        gw.add(line, x, y) # Add words to window 
        i += 1
        if y >= GWINDOW_HEIGHT - (SCORE_BASELINE + SCORE_WORDLIST_SEP + line.getAscent()):
            x += WORDLIST_DX
            i = 0 

    score = GLabel(str(len(legalWords)) + " words; "  + str(points) + " points") # Add score to window 
    score.setFont(WORDLIST_FONT)
    gw.add(score, WORDLIST_X, GWINDOW_HEIGHT - SCORE_BASELINE)  
    
def SpellingBee():
    global puzzle     
    isLegalPuzzle(input("Enter puzzle letters with center hex first:")) # Ask user for first puzzle attempt 
    gw.addEventListener("click", shuffle) 
       

# Startup code

if __name__ == "__main__":
    SpellingBee()
