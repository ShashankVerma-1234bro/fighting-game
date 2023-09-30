import pygame, sys, threading, time, sqlite3
from others import *
from fighter import *
from pygame import mixer
pygame.init()
mixer.init()

icon = pygame.image.load('assets/images/icon.jpg')
pygame.display.set_icon(icon)
pygame.display.set_caption('Infernal Vendetta')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
fps = 100
running = True

#sqlite3
game_data = sqlite3.connect("game_data.db")
curse = game_data.cursor()

listOfTables = curse.execute(cmd_to_check_table).fetchall()
if listOfTables == []:
    curse.execute(cmd_to_make_table)
    curse.execute(cmd_to_insert_values)
    game_data.commit()
else:
    pass

#load music and sounds
pygame.mixer.music.load("assets/audio/The-Key-to-the-Kingdom.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1,5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

starting = pygame.image.load('assets/images/starting photo.png').convert_alpha()
starting = pygame.transform.scale(starting,(SCREEN_WIDTH,SCREEN_HEIGHT))
starting_rect = starting.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

main_menu_bg = pygame.image.load('assets/images/background/main_menu_bg.jpg').convert_alpha()
main_menu_bg = pygame.transform.scale(main_menu_bg,(SCREEN_WIDTH,SCREEN_HEIGHT))
main_menu_bg_rect = main_menu_bg.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

back_button = pygame.image.load('assets/images/back_button.png').convert_alpha()
back_button_rect = back_button.get_rect(center = (SCREEN_WIDTH/2,40))

def display_msg(message,color,pos):
    input = message
    text = font_style.render(input, True, color)
    text_rect = text.get_rect(center = pos)
    screen.blit(text,text_rect)
        
def fight_word_display():
    screen.blit(fight_word,fight_word_rect)
    pygame.draw.rect(screen,'black',fight_word_rect,1)
    
def music_system():
    while True:
        screen.blit(main_menu_bg,main_menu_bg_rect)
        pygame.draw.rect(screen,'black',main_menu_bg_rect,1)

        mouse_pos = pygame.mouse.get_pos()

        font_style = pygame.font.Font("turok.ttf", 55)
        back_button_input = 'BACK'
        back_button = font_style.render(back_button_input, True, fg_color)
        back_button_rect = back_button.get_rect()
        back_button_rect.center = (70, 60)

        sound_text = font_style.render('SOUND : ', True, fg_color)
        sound_text_rect = sound_text.get_rect(center = (SCREEN_WIDTH/2, 200))

        on_text = font_style.render('ON', True, fg_color)
        on_text_rect = on_text.get_rect(center = (300, 350))

        off_text = font_style.render('OFF', True, fg_color)
        off_text_rect = off_text.get_rect(center = (700, 350))

        if mouse_pos[0] in range(on_text_rect.left,on_text_rect.right) and mouse_pos[1] in range(on_text_rect.top,on_text_rect.bottom):
            on_text = font_style.render('ON', True, fg_color_alt)
        else:
            on_text = font_style.render('ON', True, fg_color)

        if mouse_pos[0] in range(off_text_rect.left,off_text_rect.right) and mouse_pos[1] in range(off_text_rect.top,off_text_rect.bottom):
            off_text = font_style.render('OFF', True, fg_color_alt)
        else:
            off_text = font_style.render('OFF', True, fg_color)

        if mouse_pos[0] in range(back_button_rect.left,back_button_rect.right) and mouse_pos[1] in range(back_button_rect.top,back_button_rect.bottom):
            back_button = font_style.render(back_button_input, True, fg_color_alt)
        else:
            back_button = font_style.render(back_button_input, True, fg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_pos[0] in range(back_button_rect.left,back_button_rect.right) and mouse_pos[1] in range(back_button_rect.top,back_button_rect.bottom):
                    options_button_function()
                if mouse_pos[0] in range(on_text_rect.left,on_text_rect.right) and mouse_pos[1] in range(on_text_rect.top,on_text_rect.bottom):
                    pygame.mixer.music.unpause()
                if mouse_pos[0] in range(off_text_rect.left,off_text_rect.right) and mouse_pos[1] in range(off_text_rect.top,off_text_rect.bottom):
                    pygame.mixer.music.pause()

        screen.blit(sound_text,sound_text_rect)
        screen.blit(on_text,on_text_rect)
        screen.blit(off_text,off_text_rect)
        screen.blit(back_button,back_button_rect)
        pygame.display.update()

def quitting_screen():
    while True:
        screen.blit(main_menu_bg,main_menu_bg_rect)
        pygame.draw.rect(screen,'black',main_menu_bg_rect,1)

        mouse_pos = pygame.mouse.get_pos()

        font_style = pygame.font.Font("turok.ttf", 55)
        quitting_input = quitting
        quitting_text = font_style.render(quitting_input, True, fg_color)
        quitting_text_rect = quitting_text.get_rect(center = (SCREEN_WIDTH/2, 200))

        yes_text = font_style.render('YES', True, fg_color)
        yes_text_rect = yes_text.get_rect(center = (300, 350))

        no_text = font_style.render('NO', True, fg_color)
        no_text_rect = no_text.get_rect(center = (700, 350))

        if mouse_pos[0] in range(yes_text_rect.left,yes_text_rect.right) and mouse_pos[1] in range(yes_text_rect.top,yes_text_rect.bottom):
            yes_text = font_style.render('YES', True, fg_color_alt)
        else:
            yes_text = font_style.render('YES', True, fg_color)

        if mouse_pos[0] in range(no_text_rect.left,no_text_rect.right) and mouse_pos[1] in range(no_text_rect.top,no_text_rect.bottom):
            no_text = font_style.render('NO', True, fg_color_alt)
        else:
            no_text = font_style.render('NO', True, fg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_pos[0] in range(yes_text_rect.left,yes_text_rect.right) and mouse_pos[1] in range(yes_text_rect.top,yes_text_rect.bottom):
                    pygame.quit()
                    sys.exit()
                else:
                    main_menu()

        screen.blit(quitting_text,quitting_text_rect)
        screen.blit(yes_text,yes_text_rect)
        screen.blit(no_text,no_text_rect)
        pygame.display.update()

def score_screen_function():
    while True:
        screen.blit(main_menu_bg,main_menu_bg_rect)
        pygame.draw.rect(screen,'black',main_menu_bg_rect,1)

        scores_mouse_pos = pygame.mouse.get_pos()

        font_style = pygame.font.Font("turok.ttf", 55)
        scores_back_button_input = 'BACK'
        scores_back_button = font_style.render(scores_back_button_input, True, fg_color)
        scores_back_button_rect = scores_back_button.get_rect()
        scores_back_button_rect.center = (70, 60)

        y = 150
        curse.execute(cmd_to_select)
        rec = curse.fetchall()[0]
        for i in score_screen:
            if i == "Total Games Played - {}":
                input = i.format(sum(rec))
                display_msg(input,fg_color,(SCREEN_WIDTH/2,y))
                y+=80
            elif i == "Games won by the Warrior - {}":
                input = i.format(rec[0])
                display_msg(input,fg_color,(SCREEN_WIDTH/2,y))
                y+=80
            elif i == "Games won by the Wizard - {}":
                input = i.format(rec[1])
                display_msg(input,fg_color,(SCREEN_WIDTH/2,y))
                y+=80
            elif i == "Win %age of Warrior - {}":
                if rec[0] == 0:
                    per = 0
                else:
                    per = "{:.2f}".format(rec[0]*100/sum(rec))
                input = i.format(per)
                display_msg(input,fg_color,(SCREEN_WIDTH/2,y))
                y+=80
            elif i == "Win %age of Wizard - {}":
                if rec[1] == 0:
                    per = 0
                else:
                    per = "{:.2f}".format(rec[1]*100/sum(rec))
                input = i.format(per)
                display_msg(input,fg_color,(SCREEN_WIDTH/2,y))
                y+=80

        if scores_mouse_pos[0] in range(scores_back_button_rect.left,scores_back_button_rect.right) and scores_mouse_pos[1] in range(scores_back_button_rect.top,scores_back_button_rect.bottom):
            scores_back_button = font_style.render(scores_back_button_input, True, fg_color_alt)
        else:
            scores_back_button = font_style.render(scores_back_button_input, True, fg_color)
        screen.blit(scores_back_button,scores_back_button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if scores_mouse_pos[0] in range(scores_back_button_rect.left,scores_back_button_rect.right) and scores_mouse_pos[1] in range(scores_back_button_rect.top,scores_back_button_rect.bottom):
                    options_button_function()
        pygame.display.update()

def loading():
    global loading_finished,loading_progress
    for i in range(work):
        loading_progress=i
    loading_finished=True

threading.Thread(target = loading).start()

def draw_back():
    screen.blit(back_button,back_button_rect)

def find_coordinates(obj_size, y_coordinate):
    obj_width = obj_size[0]
    obj_height = obj_size[1]

    lower_x_limit = int( SCREEN_WIDTH/2 - obj_width/2)
    upper_x_limit = int( SCREEN_WIDTH/2 + obj_width/2)

    lower_y_limit = int(y_coordinate - obj_height/2)
    upper_y_limit = int(y_coordinate + obj_height/2)

    limits = [lower_x_limit,upper_x_limit,lower_y_limit,upper_y_limit]
    return limits

def play_button_function():
    
    #time.sleep(0.015)
    start_time = pygame.time.get_ticks()
    
    #define game variables
    intro_count = 3
    last_count_update = pygame.time.get_ticks()
    score = [0, 0]#player scores. [P1, P2]
    round_over = False
    ROUND_OVER_COOLDOWN = 2000

    #define fighter variables
    WARRIOR_SIZE = 162
    WARRIOR_SCALE = 4
    WARRIOR_OFFSET = [72, 56]
    WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
    WIZARD_SIZE = 250
    WIZARD_SCALE = 3
    WIZARD_OFFSET = [112, 107]
    WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

    #load background image
    bg_image = pygame.image.load("assets/images/background/max.jpg").convert_alpha()

    #load spritesheets
    warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
    wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

    #load vicory image
    victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

    #define number of steps in each animation
    WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
    WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

    #define font
    count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
    score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

    #function for drawing text
    def draw_text(text, font, text_col, x, y):
      img = font.render(text, True, text_col)
      screen.blit(img, (x, y))

    #function for drawing background
    def draw_bg():
      scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
      screen.blit(scaled_bg, (0, 0))

    #function for drawing fighter health bars
    def draw_health_bar(health, x, y):
      ratio = health / 100
      pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
      pygame.draw.rect(screen, RED, (x, y, 400, 30))
      pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

    #create two instances of fighters
    fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
    fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

    while True:
        
        clock.tick(fps)
        play_mouse_pos = pygame.mouse.get_pos()

        draw_bg()
        draw_back()

        #sh SCREEN_WIDTHow player stats
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
        draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)
        
        #update countdown
        if intro_count <= 0:
          if pygame.time.get_ticks() <= start_time+3800:
              display_msg('FIGHT!','red',(SCREEN_WIDTH/2,200))
              
          #move fighters
          fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
          fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
          draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
          #update count timer
          if (pygame.time.get_ticks() - last_count_update) >= 1000:
              intro_count -= 1
              last_count_update = pygame.time.get_ticks()

        #update fighters
        fighter_1.update()
        fighter_2.update()

        #draw fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        #check for player defeat
        if round_over == False:
          curse.execute(cmd_to_select)
          rec = curse.fetchall()[0]
          if fighter_1.alive == False: #if warrior is dead
            score[1] += 1
            curse.execute(cmd_to_change_value.format('wizard',score[1]+rec[1]))
            game_data.commit()
            round_over = True
            round_over_time = pygame.time.get_ticks()
          elif fighter_2.alive == False:
            score[0] += 1
            curse.execute(cmd_to_change_value.format('warrior',score[0]+rec[0]))
            game_data.commit()
            round_over = True
            round_over_time = pygame.time.get_ticks()

        else:
          #display victory image
          start_time = 0
          screen.blit(victory_img, (360, 150))
          if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 4
            fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx) 
            fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_mouse_pos[0] in range(back_button_rect.left,back_button_rect.right) and play_mouse_pos[1] in range(back_button_rect.top,back_button_rect.bottom):
                    main_menu()

        pygame.display.update()

def options_button_function():
    while True:
        option_mouse_pos = pygame.mouse.get_pos()
        screen.blit(main_menu_bg,main_menu_bg_rect)
        pygame.draw.rect(screen,'black',main_menu_bg_rect,1)

        option_back_button_input = 'BACK'
        option_back_button = font_style.render(option_back_button_input, True, fg_color)
        option_back_button_rect = option_back_button.get_rect()
        option_back_button_rect.center = (70, 60)

        scores_input = 'Scores'
        scores_button = font_style.render(scores_input, True, fg_color)
        scores_button_rect = scores_button.get_rect()
        scores_button_rect.center = (SCREEN_WIDTH/2, 150)
        scores_button_coordinates = find_coordinates(option_back_button.get_size(), 150)

        reset_input = 'DELETE THE GAME DATA'
        reset_button = font_style.render(reset_input, True, fg_color)
        reset_button_rect = reset_button.get_rect()
        reset_button_rect.center = (SCREEN_WIDTH/2, 300)
        reset_button_coordinates = find_coordinates(option_back_button.get_size(), 300)

        sound_button = font_style.render('SOUND SETTINGS', True, fg_color)
        sound_button_rect = sound_button.get_rect()
        sound_button_rect.center = (SCREEN_WIDTH/2, 450)
        sound_button_coordinates = find_coordinates(sound_button.get_size(), 450)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if option_mouse_pos[0] in range(reset_button_rect.left,reset_button_rect.right) and option_mouse_pos[1] in range(reset_button_rect.top,reset_button_rect.bottom):
                    curse.execute(cmd_to_select)
                    rec = curse.fetchall()[0]
                    curse.execute(cmd_to_delete.format('warrior',rec[0]))
                    curse.execute(cmd_to_delete.format('wizard',rec[1]))
                    curse.execute(cmd_to_insert_values)
                    game_data.commit()
                                            
                if option_mouse_pos[0] in range(scores_button_rect.left,scores_button_rect.right) and option_mouse_pos[1] in range(scores_button_rect.top,scores_button_rect.bottom):
                    score_screen_function()
                if option_mouse_pos[0] in range(option_back_button_rect.left,option_back_button_rect.right) and option_mouse_pos[1] in range(option_back_button_rect.top,option_back_button_rect.bottom):
                    main_menu()
                if option_mouse_pos[0] in range(sound_button_rect.left,sound_button_rect.right) and option_mouse_pos[1] in range(sound_button_rect.top,sound_button_rect.bottom):
                    music_system()

        if option_mouse_pos[0] in range(option_back_button_rect.left,option_back_button_rect.right) and option_mouse_pos[1] in range(option_back_button_rect.top,option_back_button_rect.bottom):
            option_back_button = font_style.render(option_back_button_input, True, fg_color_alt)
        else:
            option_back_button = font_style.render(option_back_button_input, True, fg_color)

        if option_mouse_pos[0] in range(reset_button_rect.left,reset_button_rect.right) and option_mouse_pos[1] in range(reset_button_rect.top,reset_button_rect.bottom):
            reset_button = font_style.render(reset_input, True, fg_color_alt)
        else:
            reset_button = font_style.render(reset_input, True, fg_color)

        if option_mouse_pos[0] in range(scores_button_rect.left,scores_button_rect.right) and option_mouse_pos[1] in range(scores_button_rect.top,scores_button_rect.bottom):
            scores_button = font_style.render(scores_input, True, fg_color_alt)
        else:
            scores_button = font_style.render(scores_input, True, fg_color)

        if option_mouse_pos[0] in range(sound_button_rect.left,sound_button_rect.right) and option_mouse_pos[1] in range(sound_button_rect.top,sound_button_rect.bottom):
            sound_button = font_style.render('SOUND SETTINGS', True, fg_color_alt)
        else:
            sound_button = font_style.render('SOUND SETTINGS', True, fg_color)

        screen.blit(option_back_button,option_back_button_rect)
        screen.blit(reset_button,reset_button_rect)
        screen.blit(scores_button,scores_button_rect)
        screen.blit(sound_button,sound_button_rect)
        pygame.display.update()

def help_button_function():
    while True:
        screen.blit(main_menu_bg,main_menu_bg_rect)
        pygame.draw.rect(screen,'black',main_menu_bg_rect,1)
        y = 15
        for i in help_screen:
            font_style = pygame.font.Font("turok.ttf", 35)
            control = i
            control_text = font_style.render(control, True, fg_color)
            control_rect = control_text.get_rect()
            control_rect.centerx = SCREEN_WIDTH/2
            control_rect.centery = y
            screen.blit(control_text,control_rect)
            y+= 60

        help_mouse_pos = pygame.mouse.get_pos()

        font_style = pygame.font.Font("turok.ttf", 55)
        help_back_button_input = 'BACK'
        help_back_button = font_style.render(help_back_button_input, True, fg_color)
        help_back_button_rect = help_back_button.get_rect()
        help_back_button_rect.center = (70, 60)

        if help_mouse_pos[0] in range(help_back_button_rect.left,help_back_button_rect.right) and help_mouse_pos[1] in range(help_back_button_rect.top,help_back_button_rect.bottom):
            help_back_button = font_style.render(help_back_button_input, True, fg_color_alt)
        else:
            help_back_button = font_style.render(help_back_button_input, True, fg_color)
        screen.blit(help_back_button,help_back_button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if help_mouse_pos[0] in range(help_back_button_rect.left,help_back_button_rect.right) and help_mouse_pos[1] in range(help_back_button_rect.top,help_back_button_rect.bottom):
                    main_menu()
        pygame.display.update()

def main_game():
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(starting,starting_rect)

        if not loading_finished:

            GAME_input = 'Infernal Vendetta'
            GAME = font_style.render(GAME_input, True, school_bus_yellow)
            GAME_rect = GAME.get_rect()
            GAME_rect.center = ( SCREEN_WIDTH/2, 50)
            pygame.draw.rect(screen,maroon,pygame.Rect((GAME_rect.left-5,GAME_rect.top,GAME_rect.width+5, GAME_rect.height)),border_radius = 15)
            screen.blit(GAME, GAME_rect)

            #loading text
            load = font_style.render('Loading ...', True, fg_color)
            load_rect = load.get_rect()
            load_rect.center = (SCREEN_WIDTH/2, 460)
            screen.blit(load, load_rect)

            #loading frame
            loading_bar_frame = (395,495,210,40)
            pygame.draw.rect(screen,red,pygame.Rect(loading_bar_frame),width = 5,border_radius = 18)
            #loading bar
            loading_bar_width = loading_progress/work*200
            loading_bar_rect = (400, 500,loading_bar_width,30)
            pygame.draw.rect(screen,golden_yellow,pygame.Rect(loading_bar_rect),border_radius = 15)

        else:
            time.sleep(3)
            main_menu()
        pygame.display.update()

def main_menu():
    while running:

        mouse_pos = pygame.mouse.get_pos()
        screen.blit(main_menu_bg,main_menu_bg_rect)
        pygame.draw.rect(screen,'black',main_menu_bg_rect,1)

        clock.tick(120)
        MAIN_MENU_input = 'MAIN MENU'
        MAIN_MENU = font_style.render(MAIN_MENU_input, True, fg_color)
        MAIN_MENU_rect = MAIN_MENU.get_rect()
        MAIN_MENU_rect.center = ( SCREEN_WIDTH/2, 50)

        play_input = 'PLAY'
        play = font_style.render(play_input, True, fg_color)
        play_rect = play.get_rect()
        play_rect.center = ( SCREEN_WIDTH/2, 200)
        play_coordinates = find_coordinates(play.get_size(), 200)

        help_input = 'HELP'
        help = font_style.render(help_input, True, fg_color)
        help_rect = help.get_rect()
        help_rect.center = ( SCREEN_WIDTH/2, 300)
        help_coordinates = find_coordinates(play.get_size(), 300)

        options_input = 'OPTIONS'
        options = font_style.render(options_input, True, fg_color)
        options_rect = options.get_rect()
        options_rect.center = ( SCREEN_WIDTH/2, 400)
        options_coordinates = find_coordinates(play.get_size(), 400)

        quit_input = 'QUIT'
        quit = font_style.render(quit_input, True, fg_color)
        quit_rect = quit.get_rect()
        quit_rect.center = (SCREEN_WIDTH/2, 500)
        quit_coordinates = find_coordinates(quit.get_size(), 500)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_pos[0] in range(play_coordinates[0],play_coordinates[1]) and mouse_pos[1] in range(play_coordinates[2],play_coordinates[3]):
                    play_button_function()
                if mouse_pos[0] in range(help_coordinates[0],help_coordinates[1]) and mouse_pos[1] in range(help_coordinates[2],help_coordinates[3]):
                    help_button_function()
                if mouse_pos[0] in range(options_coordinates[0],options_coordinates[1]) and mouse_pos[1] in range(options_coordinates[2],options_coordinates[3]):
                    options_button_function()
                if mouse_pos[0] in range(quit_coordinates[0],quit_coordinates[1]) and mouse_pos[1] in range(quit_coordinates[2],quit_coordinates[3]):
                    quitting_screen()

        #change colour of the button when the mouse is on it.
        if mouse_pos[0] in range(play_coordinates[0],play_coordinates[1]) and mouse_pos[1] in range(play_coordinates[2],play_coordinates[3]):
            play = font_style.render(play_input, True, fg_color_alt)
        else:
            play = font_style.render(play_input, True, fg_color)

        if mouse_pos[0] in range(help_coordinates[0],help_coordinates[1]) and mouse_pos[1] in range(help_coordinates[2],help_coordinates[3]):
            help = font_style.render(help_input, True, fg_color_alt)
        else:
            help = font_style.render(help_input, True, fg_color)

        if mouse_pos[0] in range(options_coordinates[0],options_coordinates[1]) and mouse_pos[1] in range(options_coordinates[2],options_coordinates[3]):
            options = font_style.render(options_input, True, fg_color_alt)
        else:
            options = font_style.render(options_input, True, fg_color)

        if mouse_pos[0] in range(quit_coordinates[0],quit_coordinates[1]) and mouse_pos[1] in range(quit_coordinates[2],quit_coordinates[3]):
            quit = font_style.render(quit_input, True,fg_color_alt)
        else:
            quit = font_style.render(quit_input, True, fg_color)

        screen.blit(MAIN_MENU, MAIN_MENU_rect)
        screen.blit(play, play_rect)
        screen.blit(help, help_rect)
        screen.blit(options, options_rect)
        screen.blit(quit, quit_rect)
        pygame.display.update()

main_game()

pygame.quit()
