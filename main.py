# Assets.
from colorama import Fore, Back, Style

from keyboard import is_pressed
from playsound import playsound

from os import system
from time import sleep


# Objects settings.
ground_sym = ' ' # Also can be point ("."), but needed a bit more code to make it more comfortable for eyes.
ground_color = Back.GREEN
ground_size = [80, 20]

player_sym = '@'
player_color = Fore.RED
player_spawn_pos = [ground_size[0] // 2, ground_size[1] // 2]
player_moving_speed = 1

human_sym = '#'
human_color = Fore.BLUE
human_spawn_pos = [15, 5]

# Game settings.
game_update_time = 0.25

# Ground source view.
ground_src_view = f'{ground_color}{ground_sym}{Back.BLACK}'

# Player source view.
player_src_view = f'{player_color}{ground_color}{player_sym}{Fore.WHITE}{Back.BLACK}'

# Human source view.
human_source_view = f'{human_color}{ground_color}{human_sym}{Fore.WHITE}{Back.BLACK}'

# Clear console screen.
def clear_screen():
    system('cls')

# Fill one console column with ground.
def fill_with_ground():
    print(ground_src_view, end='')

# Print the player.
def print_the_player():
    print(player_src_view, end='')

# Print the human.
def print_the_human():
    print(human_source_view, end='')

# Print message.
def message(text):
    print(f'{Style.BRIGHT}\x1b[1m{text}\x1b[0m{Style.NORMAL}')

# Play sound.
def play_sound(sound):
    playsound(sound, False)

# Game polygon.
game_polygon = [] # BUG : Player position doesn't updates on game polygon.

# Player functions.
get_player_pos_on_polygon = lambda: game_polygon.index(player_src_view)
play_player_moving_sound = lambda: play_sound('sounds\\move_sound.wav')
play_player_interaction_with_human_sound = lambda: play_sound('sounds\\human_interaction.wav')

is_player_touches_the_human = lambda: \
    (player_spawn_pos[0] + 1 == human_spawn_pos[0] or player_spawn_pos[0] == human_spawn_pos[0]) and (player_spawn_pos[1] + 1 == human_spawn_pos[1] or player_spawn_pos[1] == human_spawn_pos[1]) \
        or (player_spawn_pos[0] - 1 == human_spawn_pos[0] or player_spawn_pos[0] == human_spawn_pos[0]) and (player_spawn_pos[1] - 1 == human_spawn_pos[1] or player_spawn_pos[1] == human_spawn_pos[1])

# Human functions.
get_human_pos_on_polygon = lambda: game_polygon.index(human_source_view)

# Keyboarad functions.
pressed = lambda key: is_pressed(key)

# Temporary game loop variables.
_talking_with_human = False
_played_interaction_sound = False
_finished_choice_cutscene = False
_current_choice = 2

# Clear the screen.
clear_screen()

# Game loop.
while True:
    # Print some text :)
    message(f'{" " * ((ground_size[0] // 2) - (ground_size[1] // 2) + 3)} ASCII Game!')

    # Generate terrain + player spawning.
    for y in range(ground_size[1]):
        for x in range(ground_size[0]):
            if x == player_spawn_pos[0] and y == player_spawn_pos[1]:
                print_the_player()

                game_polygon.append(player_src_view)

            elif x == human_spawn_pos[0] and y == human_spawn_pos[1]:
                print_the_human()

                game_polygon.append(human_source_view)

            else:
                fill_with_ground()

                game_polygon.append(ground_src_view)

        print()

        game_polygon.append('\n')

    # If player touches the human then maybe he's want to talk with him?
    if is_player_touches_the_human() and not _talking_with_human:
        message('Press \'E\' to talk with human!')

    # Talk cut-scene.
    if pressed('e') or _talking_with_human:
        _talking_with_human = True

        if is_player_touches_the_human():
            if not _finished_choice_cutscene:
                if not _played_interaction_sound:
                    play_player_interaction_with_human_sound()

                    _played_interaction_sound = True

                message('Hi! You want something?')

                choices = 2

                message(f'{Fore.RED if _current_choice == 2 else ""}> Nah!')
                message(f'{Fore.RED if _current_choice == 1 else ""}> Yes, i wanted to say hi!')

                if pressed('up'):
                    _current_choice = 2

                elif pressed('down'):
                    _current_choice = 1

                if pressed('enter'):
                    if _current_choice == 1:
                        message('Oh, then hi too!')

                        sleep(1)

                    else:
                        message('Okay, bye then!')

                        sleep(1)

                    _finished_choice_cutscene = True

        else:
            _talking_with_human = False

            _played_interaction_sound = False

            _finished_choice_cutscene = False

            _current_choice = 2

    # Dynamic player info.
    current_player_pos = get_player_pos_on_polygon()

    # Player controls.
    if pressed('w'):
        if not (player_spawn_pos[1] <= 0):
            play_player_moving_sound()

            player_spawn_pos[1] -= player_moving_speed

    elif pressed('a'):
        if not (player_spawn_pos[0] <= 0):
            play_player_moving_sound()

            player_spawn_pos[0] -= player_moving_speed

    elif pressed('s'):
        if not (player_spawn_pos[1] >= ground_size[1] - player_moving_speed):
            play_player_moving_sound()

            player_spawn_pos[1] += player_moving_speed

    elif pressed('d'):
        if not (player_spawn_pos[0] >= ground_size[0] - player_moving_speed):
            play_player_moving_sound()

            player_spawn_pos[0] += player_moving_speed

    # Exit ('escape') key handling.
    if pressed('esc'):
        clear_screen()

        break

    # If CTRL + C pressed.
    try:
        # Update time!
        sleep(game_update_time)

        # Clear the screen.
        clear_screen()
    except KeyboardInterrupt:
        clear_screen()

        break
