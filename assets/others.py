import pygame
pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

#color codes
red = (255,0,0)
maroon = (128,0,0)
baby_blue = (137, 207, 240)
midnight_blue = (0,51,102)
golden_yellow = (255,223,0)
school_bus_yellow = (255,216,0)
dark_purple = (85,26,139)
true_blue = (0,115,207)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#font and color and style
font_style = pygame.font.Font("turok.ttf", 55)
fg_color = midnight_blue
fg_color_alt = true_blue
bg_color = 'white'

#for loading bar
loading_finished = False
loading_progress = 0
work = 44988999

help_screen = ['For the Warrior :',
               'key w for jumping',
               'key a for moving left',
                'key d for moving right',
                'key r, t for attacking',
                'For the Wizard :',
                'up key for jumping',
                'right key for moving right',
                'left key for moving left',
                'key n, m for attacking']

cmd_to_make_table = """CREATE TABLE Scores (
     warrior INTEGER,
     wizard INTEGER)"""

cmd_to_insert_values = """INSERT INTO Scores Values (0,0)"""

cmd_to_select = """SELECT * FROM Scores"""

cmd_to_change_value = """UPDATE Scores SET {} = {}"""

cmd_to_delete = """DELETE FROM Scores WHERE {} = {};"""

score_screen = ["Total Games Played - {}",
"Games won by the Warrior - {}",
"Games won by the Wizard - {}",
"Win %age of Warrior - {}",
"Win %age of Wizard - {}"]

cmd_to_check_table = '''SELECT name FROM sqlite_master WHERE type='table' AND name ='Scores';'''

quitting = 'ARE YOU SURE YOU WANT TO QUIT?'

tick = '✓'
