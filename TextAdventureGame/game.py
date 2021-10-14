import cmd
import textwrap
import sys
import os
import time
import random


screen_width = 100

#### Setting up the player
class player:
    def __init__(self):
        self.name = ''
        self.location = 'room'
        self.won = False
        self.solves = 0

my_player = player()

def title_selection():
    option = input("> ")
    if option.lower() == ("play"):
        start_game()
    elif option.lower() == ("help"):
        game_help()
    elif option.lower() == ('quit'):
        sys.exit()
    while option.lower() not in ['play', 'help', 'quit']:
        print("Please enter a valid command.")
        input("> ")
        option = input("> ")
        if option.lower() == ("play"):
            start_game()
        elif option.lower() == ("help"):
            game_help()
        elif option.lower() == ('quit'):
            sys.exit()


def intro():
    os.system('cls')
    print('------------------------')
    print('          Hole          ')
    print('------------------------')
    print('         -Play-         ')
    print('         -Help-         ')
    print('-        -Quit-         ')
    print('------------------------')
    title_selection()

def game_help():
    os.system('cls')
    print('------------------------')
    print('          Hole          ')
    print('------------------------')
    print('- Enter input to move around! -')
    print('- Type \'move\' and where you want to move to\'')
    print('- To inspect something, type \'examine\'.')
    print('- Have fun! -')
    title_selection()

# GAME
def start_game():
    os.system('cls')
    speech1 ="You wake up in a cold sweat, bathing in the dim light of a flickering light bulb. You feel your head throbbing as you struggle to recall where you are and who you are. \n"
    speech2 = "\'Wha..? ...Where am I?\' \n"
    speech3 = '... \n'
    speech4 = 'I don\'t remember anything... \n'
    for character in speech1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.03)
    for character in speech2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in speech3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.1)
    for character in speech4:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    get_name()
    speech4 = 'You suddenly feel a sharp pain as you recall your name. \n'
    speech5 = my_player.name + " is my name? \n"
    speech6 = "...that doesn't feel right... \n"
    for character in speech4:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in speech5:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.1)
    for character in speech6:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.2)
    time.sleep(1)

    os.system('cls')
    print("'You find yourself in a somewhat damp room, with a small crawlway on all four of your cardinal direction.\nYou reach into your pocket and you notice that you have small map of the area with you.\n")

    ### Starts the game
    main_game_loop()

# MAP
"""
                        WELL
                        |
                        |
                        |
                        |
CATACOMBS ----------- ROOM ------------ RUINS
                        |
                        |
                        |
                        |
                        |
                    STAIRWAY

"""

#### Constant Variables
DESCRIPTION = 'description'
INFO = 'info'
PUZZLE = 'puzzle'
SOLVED = False
ROOM = 'room'
STAIRS = 'stairs'
WELL = 'well'
RUINS = 'ruins'
CATACOMBS = 'catacombs'


solved_places = {
    'well':False, 'catacombs':False, 'stairway':False, 'ruins':False, 'room':False
}

### Different part of the maps that players can travel and interact with
zone_map = {
    'room': {
        DESCRIPTION: 'You find yourself in a somewhat damp room, with a small crawlway on all four of your cardinal direction.\nYou reach into your pocket and you notice that you have small map of the area with you.\n',
        INFO: 'The areas on the map are titled \"Room, Catacombs, Well, Ruins, and Stairway\"',
        PUZZLE: '\nYou notice that right next to the entrance to each room, there are mailboxes, all titled respectively according to the room names. How strange...',
        SOLVED: False, #Finished when every other puzzle is done and you come back to the main room
        ROOM: 'room',
        STAIRS: 'stairway',
        WELL: 'well',
        RUINS: 'ruins',
        CATACOMBS: 'catacombs'
    },

    'catacombs': {
        DESCRIPTION: 'You enter what seems like the catacombs, according to the sign. \nYou notice there are three coffins, but only one is open...\n',
        INFO: 'You go check out one of the open coffin. Inside you see a piece of paper...\n',
        PUZZLE: '\'What has teeth but it cannot bite?\' the second paper says. How odd...',
        SOLVED: 'comb',
        ROOM: 'room',
        STAIRS: 'stairway',
        WELL: 'well',
        RUINS: 'ruins',
        CATACOMBS: 'catacombs'
    },

    'ruins': {
        DESCRIPTION: 'You enter the ruins.\nThe only thing you can make out in this room is that it used to be a gallery here.\nFrame upon frames lie amongst the wall, but no picture inside of them, except for one.\n',
        INFO: 'You go and check out the only painting on the wall. \nYou notice that behind the painting there is a piece of paper, tucked away in the frame of the painting of a well.',
        PUZZLE: 'The piece of paper reads \'The more you take, the more you leave behind. What am I?\'',
        SOLVED: 'footsteps',
        ROOM: 'room',
        STAIRS: 'stairway',
        WELL: 'well',
        RUINS: 'ruins',
        CATACOMBS: 'catacombs'
    },

    'well': {
        DESCRIPTION: 'You walk into the well and notice the bucket in the middle of the room.',
        INFO: '\nThere\'s water up to your knees.\nYou feel heavy as you trod through the water to get to the bucket that\'s in the middle of the room.\n The bucket contains a piece of paper.',
        PUZZLE: 'The piece of paper reads...\"You live in a one story house and it\'s made out of redwood. What color are the stairs?',
        SOLVED: 'none',
        ROOM: 'room',
        STAIRS: 'stairway',
        WELL: 'well',
        RUINS: 'ruins',
        CATACOMBS: 'catacombs'
    },

    'stairway': {
        DESCRIPTION: 'You enter the stairway and theres nothing here but a big metal door, approximately twelve feet tall.',
        INFO: 'The stairway leads up but there\'s clearly a metal door blocking it, and you notice that there are no handles or locks.\n You do however, notice the piece of paper taped to the door.',
        PUZZLE: 'The paper reads, \"What has many keys, but can\'t even open a single door?\"',
        SOLVED: 'piano',
        ROOM: 'room',
        STAIRS: 'stairs',
        WELL: 'well',
        RUINS: 'ruins',
        CATACOMBS: 'catacombs'
    },
}

### Tell current location
def print_location():
	#Makes a pretty picture when printed and prints the cube floor information for the player.
	print('\n' + ('#' * (4 +len(my_player.location))))
	print('# ' + my_player.location.upper() + ' #')
	print('#' * (4 +len(my_player.location)))
	print('\n' + (zone_map[my_player.location][DESCRIPTION]))

### Player entering what they want to do
def prompt():
    if my_player.solves == 4:
        finish = 'You hear something turning...'
        for character in finish:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.1)
    print("\n" + '-------------------------')
    print("What are you going to do?")
    action = input('> ')
    correct_action = ['move', 'go', 'travel', 'walk', 'quit', 'examine', 'inspect', 'interact', 'look']
    while action.lower() not in correct_action:
        print("Invalid command, please try again. \n")
        action = input('> ')
    if action.lower == 'quit':
        sys.exit()
    elif action.lower() in ['move', 'go', 'travel', 'walk']:
        player_move(action.lower())
    elif action.lower() in ['examine', 'inspect', 'interact', 'look']:
        examine(action.lower())
    elif action.lower() == ['map', 'help']:
        print("You refer back to your map..\nThe room names are titled \"Room, Catacombs, Well, Ruins, and Stairway\".")


def player_move(action):
    ask = "Where would you like to go? \n> "
    dest = input(ask)
    if dest == ['room']:
        destination = zone_map[my_player.location][ROOM]
        movement_handler(destination)
    elif dest in ['ruins']:
        destination = zone_map[my_player.location][RUINS]
        movement_handler(destination)
    elif dest in ['well']:
        destination = zone_map[my_player.location][WELL]
        movement_handler(destination)
    elif dest in ['stairs']:
        destination = zone_map[my_player.location][STAIRS]
        movement_handler(destination)
    elif dest in ['catacombs']:
        destination = zone_map[my_player.location][CATACOMBS]
        movement_handler(destination)
    else:
        print("Invalid direction command.\nHint: The room names are titled \"Room, Catacombs, Well, Ruins, and Stairway\".\n")
        player_move(action)

def movement_handler(dest):
    print('\n' + 'You have moved to the ' + dest + '.')
    my_player.location = dest
    print_location()



def get_name():
    question_name = "What is my name? \n"
    for character in question_name:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    player_name = input("> ")
    my_player.name = player_name

def examine(self):
	if solved_places[my_player.location] == False:
		print('\n' + (zone_map[my_player.location][INFO]))
		print((zone_map[my_player.location][PUZZLE]))
		puzzle_answer = input("> ")
		checkpuzzle(puzzle_answer)
	else:
		print("There is nothing new for you to see here.")

def checkpuzzle(puzzle_answer):
	if my_player.location == 'room':
		if my_player.solves >= 4:
			endspeech = ("You proceed to put in a letter in each mailbox so that each mailbox contains one letter.\n You hear a loud clicking noise as you notice the door starts to open.\nYour heart race as you wait for it to open as you are about to leave.\n You open the door as you realize that there is nothing outside.\nThere are no trees.\nThere are no birds.\nThere are no humans.\nExcept for you.")
			for character in endspeech:
				sys.stdout.write(character)
				sys.stdout.flush()
				time.sleep(0.05)
			print("\nHow unfortunate.")
			sys.exit()
		else:
			print("Nothing seems to happen still...")
	else:
		if puzzle_answer == (zone_map[my_player.location][SOLVED]):
			solved_places[my_player.location] = True
			my_player.solves += 1
			print("You have solved the puzzle. Onwards!")
			print("\nPuzzles solved: " + str(my_player.solves))
		else:
			print("Wrong answer! Try again.\n~~~~~~~~~~~~~~~~~~~~~~~~~~")
			examine()
    
    

            

def main_game_loop():
	total_puzzles = 6
	while my_player.won is False:
		prompt()

intro()