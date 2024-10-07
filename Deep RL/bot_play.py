import pygame
import random
from environments import TicTacToe

# Initialize pygame
pygame.init()
size = 500  # Taille de la fenêtre
screen = pygame.display.set_mode((size, size))
pygame.display.set_caption("TicTacToe")

# Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (23, 145, 135)
X_COLOR = (84, 84, 84)
O_COLOR = (28, 170, 156)
BUTTON_COLOR = (100, 200, 100)
BUTTON_HOVER_COLOR = (170, 255, 170)
TEXT_COLOR = (255, 255, 255)

# Game Variables
board_size = 3
cell_size = size // board_size  # Ajuste la taille des cellules en fonction de la taille de la fenêtre
line_width = 15  # Épaisseur des lignes

# Initialize font
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)  # Augmenter la taille de la police
button_font = pygame.font.SysFont('Arial', 20)  # Augmenter la taille de la police pour les boutons

# Variable to track the current player (1 = X, -1 = O)
current_player = 1

def draw_board():
    screen.fill(WHITE)
    for i in range(1, board_size):
        pygame.draw.line(screen, LINE_COLOR,
                         (0, i * cell_size),
                         (size, i * cell_size),
                         line_width)
        pygame.draw.line(screen, LINE_COLOR,
                         (i * cell_size, 0),
                         (i * cell_size, size),
                         line_width)


def draw_move(row, col, player):
    center = (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2)
    if player == 1:
        pygame.draw.line(screen, X_COLOR,
                         (center[0] - 70, center[1] - 70),
                         (center[0] + 70, center[1] + 70),
                         line_width)
        pygame.draw.line(screen, X_COLOR,
                         (center[0] + 70, center[1] - 70),
                         (center[0] - 70, center[1] + 70),
                         line_width)
    else:
        pygame.draw.circle(screen, O_COLOR, center, 70, line_width)


def get_click_position():
    x, y = pygame.mouse.get_pos()
    row = y // cell_size
    col = x // cell_size
    return row, col


def display_winner(winner):
    """ Afficher le message du gagnant. """
    if winner == 1:
        text = font.render('Player 1 (X) wins!', True, BLACK)
    elif winner == -1:
        text = font.render('Player 2 (O) wins!', True, BLACK)
    else:
        text = font.render('It\'s a draw!', True, BLACK)

    screen.fill(WHITE)
    screen.blit(text, (size // 6, size // 3))
    pygame.display.update()


def draw_button(text, rect, active):
    """ Afficher un bouton avec effet de survol """
    color = BUTTON_HOVER_COLOR if active else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect)
    text_surf = button_font.render(text, True, TEXT_COLOR)
    screen.blit(text_surf, (rect.x + 10, rect.y + 10))


def end_screen(winner):
    """ Afficher l'écran de fin avec les options pour rejouer ou quitter """
    display_winner(winner)
    pygame.time.wait(1000)

    # Définir les boutons
    replay_button = pygame.Rect(100, 350, 300, 60)  # Ajuster la taille et la position des boutons
    quit_button = pygame.Rect(100, 420, 300, 60)

    redraw = True  # Indicateur pour redessiner l'écran seulement si nécessaire

    while True:
        if redraw:
            screen.fill(WHITE)
            display_winner(winner)

            # Afficher les boutons une seule fois ou lorsque l'état de survol change
            mouse_pos = pygame.mouse.get_pos()

            replay_hovered = replay_button.collidepoint(mouse_pos)
            quit_hovered = quit_button.collidepoint(mouse_pos)

            draw_button("Restart", replay_button, replay_hovered)
            draw_button("Quit", quit_button, quit_hovered)

            pygame.display.update()
            redraw = False  # Ne redessine plus tant qu'il n'y a pas de changement

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Quit the game

            if event.type == pygame.MOUSEMOTION:
                # Redessiner uniquement si l'état de survol change
                mouse_pos = pygame.mouse.get_pos()
                if replay_button.collidepoint(mouse_pos) or quit_button.collidepoint(mouse_pos):
                    redraw = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.collidepoint(mouse_pos):
                    return True  # Return to menu instead of restarting the game
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    return False  # Quit the game


def bot_play(env):
    """ Bot aléatoire pour jouer un coup """
    available_actions = env.available_actions()
    action = random.choice(available_actions)
    return action


def game_mode_selection():
    """ Menu pour sélectionner le mode de jeu """
    screen.fill(WHITE)
    title_font = pygame.font.SysFont('Arial', 40)
    title_text = title_font.render('Select Game Mode', True, BLACK)
    screen.blit(title_text, (size // 6, size // 4))

    # Define buttons
    bot_button = pygame.Rect(100, 250, 300, 60)
    multiplayer_button = pygame.Rect(100, 350, 300, 60)

    running = True
    while running:
        screen.fill(WHITE)
        screen.blit(title_text, (size // 6, size // 4))

        mouse_pos = pygame.mouse.get_pos()

        bot_hovered = bot_button.collidepoint(mouse_pos)
        multiplayer_hovered = multiplayer_button.collidepoint(mouse_pos)

        draw_button("Play vs Bot", bot_button, bot_hovered)
        draw_button("Multiplayer", multiplayer_button, multiplayer_hovered)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None  # Quit the game

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bot_button.collidepoint(mouse_pos):
                    return 'bot'  # Jouer contre le bot
                if multiplayer_button.collidepoint(mouse_pos):
                    return 'multiplayer'  # Mode multijoueur


# Main loop
def play_game():
    global current_player  # Use global to track the current player across moves
    running = True

    while running:
        # Sélectionner le mode de jeu à chaque "Restart"
        game_mode = game_mode_selection()
        if game_mode is None:
            return  # Si l'utilisateur quitte

        env = TicTacToe()
        state = env.reset()
        draw_board()
        game_over = False
        winner = None

        while not game_over:
            if game_mode == 'bot' and current_player == -1:
                # Bot joue quand c'est au tour du joueur O (bot)
                action = bot_play(env)
                row, col = action
                state, reward, game_over = env.step(action)
                draw_move(row, col, current_player)
                pygame.display.update()

                current_player *= -1  # Changer de joueur après le coup du bot

                if game_over:
                    pygame.time.wait(500)
                    winner = current_player * -1 if reward == 1 else 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                    game_over = True

                elif event.type == pygame.MOUSEBUTTONDOWN and current_player == 1:
                    row, col = get_click_position()
                    action = (row, col)
                    try:
                        # Vérifier que la cellule est vide avant de jouer le coup
                        if (row, col) in env.available_actions():
                            draw_move(row, col, current_player)
                            pygame.display.update()

                            # Appliquer l'action du joueur courant
                            state, reward, game_over = env.step(action)
                            current_player *= -1  # Changer de joueur après le coup

                            if game_over:
                                pygame.time.wait(500)
                                winner = current_player * -1 if reward == 1 else 0

                    except ValueError:
                        pass  # Coup invalide

            pygame.display.update()

        # Écran de fin avec options pour rejouer ou quitter
        running = end_screen(winner)


# Run the game
if __name__ == "__main__":
    play_game()
