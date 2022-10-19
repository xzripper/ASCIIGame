# Assets.
from colorama import Fore, Back

from os import system

from keyboard import is_pressed

from time import sleep


# Game settings.
ground_sym = ' ' # Also can be point (".").
ground_color = Back.GREEN

player_sym = '@'
player_color = Fore.RED

ground_size = [80, 20]

player_spawn_pos = [ground_size[0] // 2, ground_size[1] // 2]

player_moving_speed = 1

game_update_time = 0.25

# Ground source view.
ground_src_view = f'{ground_color}{ground_sym}{Back.BLACK}'

# Player source view.
player_src_view = f'{player_color}{ground_color}{player_sym}{Fore.WHITE}{Back.BLACK}'

# Clear console screen.
def clear_screen():
    system('cls')

# Fill one console column with ground.
def fill_with_ground():
    print(ground_src_view, end='')

# Print the player.
def print_the_player():
    print(player_src_view, end='')

# Game polygon.
game_polygon = []

# Player functions.
get_player_pos_on_polygon = lambda: game_polygon.index(player_src_view)

# Keyboarad functions.
pressed = lambda key: is_pressed(key)

# Clear the screen.
clear_screen()

# Game loop.
while True:
    # Print some text :)
    print(f'{" " * ((ground_size[0] // 2) - (ground_size[1] // 2) + 3)} ASCII Game!')

    # Generate terrain + player spawning.
    for y in range(ground_size[1]):
        for x in range(ground_size[0]):
            if x == player_spawn_pos[0] and y == player_spawn_pos[1]:
                print_the_player()

                game_polygon.append(player_src_view)

            else:
                fill_with_ground()

                game_polygon.append(ground_src_view)

        print()

        game_polygon.append('\n')

    # Dynamic player info.
    current_player_pos = get_player_pos_on_polygon()

    # Player controls.
    if pressed('w'):
        if not (player_spawn_pos[1] <= 0):
            player_spawn_pos[1] -= player_moving_speed

    elif pressed('a'):
        if not (player_spawn_pos[0] <= 0):
            player_spawn_pos[0] -= player_moving_speed

    elif pressed('s'):
        if not (player_spawn_pos[1] >= ground_size[1] - player_moving_speed):
            player_spawn_pos[1] += player_moving_speed

    elif pressed('d'):
        if not (player_spawn_pos[0] >= ground_size[0] - player_moving_speed):
            player_spawn_pos[0] += player_moving_speed

    # If CTRL + C pressed.
    try:
        # Update time!
        sleep(game_update_time)

        # Clear the screen.
        clear_screen()
    except KeyboardInterrupt:
        clear_screen()

        break
