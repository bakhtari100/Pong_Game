import pygame
import random



# Constants for the windows width and height values
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

# Assign the colors used in the game

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 128, 0)
COLOR_PINK = (255, 105, 180)


def main():
    # GAME SETUP
    # Initialize the PYgame library 
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong")

    # Create the clock object to keep track of the time
    clock = pygame.time.Clock()

    
    """ 
    these are the players' game paddles 
    the pygame.Rect function need x, y, width and height    
    of the rectangle we will be drawing 
    """ 
    
    paddle_1_rect = pygame.Rect(30, 0, 7, 100)  
    paddle_2_rect = pygame.Rect(SCREEN_WIDTH - 50, 0, 7, 100)   
    
    # This is to track by how much the player's paddles wil move per frame 
    paddle_1_move = 0   
    paddle_2_move = 0   
    
    # This is the rectangle that represents the ball    
    ball_rect = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 25, 25)    
    ball_accel_x = random.randint(2, 4) * 0.09   
    ball_accel_y = random.randint(2, 4) * 0.09   
    
    # Randomize the direction of the ball   
    if random.randint(1, 2) == 1:   
        ball_accel_x *= -1  
    if random.randint(1, 2) == 1:   
        ball_accel_y *= -1

    score_1 = 0
    score_2 = 0
    font = pygame.font.SysFont('Consolas', 30)

    # Get the players' names
    def get_players_names(prompt):
        name = ""
        entering = True
        while entering:
            screen.fill(COLOR_PINK)
            text_surface = font.render(f"{prompt}: {name}", True, COLOR_WHITE)
            rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text_surface, rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        entering = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
        return name if name != "" else "Player"
    
    # Get the players' names
    player1_name = get_players_names("Enter Player 1 Name")
    player2_name = get_players_names("Enter Player 2 Name")

    started = False



    # Reset the ball to the center of the screen and randomize its direction
    def reset_ball():
        nonlocal ball_rect, ball_accel_x, ball_accel_y
        ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        ball_accel_x = random.choice([-1, 1]) * random.randint(2, 4) * 0.07
        ball_accel_y = random.choice([-1, 1]) * random.randint(2, 4) * 0.07
    
    # Display the winner and pause before quitting
    def show_winner():
        text = font.render(winner_text, True, COLOR_WHITE)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.fill(COLOR_PINK)
        screen.blit(text, rect)
        pygame.display.flip()
        pygame.time.delay(5000)
        pygame.quit()
        exit()
        


  
    while True:

        """
        set the back ground to color to black 
        needs to be called everytime the games updates
        """
        screen.fill(COLOR_PINK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if not started:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        started = True
            else:
                # make the ball move after 3 seconds
                if event.type == pygame.KEYDOWN:
                    # PLAYER 1
                    # if key is W, set the movement of paddle_1 to go up
                    if event.key == pygame.K_w:
                        paddle_1_move = -0.5
                    # if the key is S, set the movement of paddle_1 to go down
                    if event.key == pygame.K_s:
                        paddle_1_move = 0.5
                    # PLAYER 2
                    # if the key is the up arrow, set the movement of paddle_2 to go up
                    if event.key == pygame.K_UP:
                        paddle_2_move = -0.5
                    # if the key is the down arrow, set the movement of paddle_2 to go down
                    if event.key == pygame.K_DOWN:
                        paddle_2_move = 0.5
                
                # if player released a key
                if event.type == pygame.KEYUP:
                    # if the key is released is w or s, stop movement of paddle_1
                    if event.key in (pygame.K_w, pygame.K_s):
                        paddle_1_move = 0.0
                    # if key released is the up or down arrow, stop movement of paddle_2
                    if event.key in (pygame.K_UP, pygame.K_DOWN):
                        paddle_2_move = 0.0


    
        if not started:
            # Load the Consolas font
            font = pygame.font.SysFont('Consolas', 30)
            # Draw some text to the center of the screen 
            text = font.render('Press Space to Start', True, COLOR_WHITE)
            text_rect = text.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
        else:
            """
            get the time elapse between now and the last frame
            60 is an arbitray number but the game runs smooth at 60 FPS
            """
            
            delta_time = clock.tick(60)

            """
            move paddle_1 and paddle_2 according to their move variables
            we also multiply the move variable by the delta time to keep the movement consistent through frames
            """
            paddle_1_rect.top += paddle_1_move * delta_time
            paddle_2_rect.top += paddle_2_move * delta_time

            # Clamp the paddles to the screen height
            paddle_1_rect.top = max(0, min(SCREEN_HEIGHT - paddle_1_rect.height, paddle_1_rect.top))
            paddle_2_rect.top = max(0, min(SCREEN_HEIGHT - paddle_2_rect.height, paddle_2_rect.top))
            
            # Move the ball according to its acceleration
            ball_rect.left += ball_accel_x * delta_time
            ball_rect.top += ball_accel_y * delta_time

            if ball_rect.top <= 0:
                # Invert its vertical veolcity
                ball_accel_y *= -1
                ball_rect.top = 0
            # Repeat with bottom
            if ball_rect.bottom >= SCREEN_HEIGHT:
                ball_accel_y *= -1
                ball_rect.bottom = SCREEN_HEIGHT 
            
            
            # Scoring system
            if ball_rect.left <= 0:
                score_2 += 1
                reset_ball()
            if ball_rect.right >= SCREEN_WIDTH:
                score_1 += 1
                reset_ball()
            
            # Check win condition
            if score_1 >= 5:
                winner_text = f"{player1_name} Wins!"
                show_winner()
            if score_2 >= 5:
                winner_text = f"{player2_name} Wins!"
                show_winner()
            """
            if paddle_1_rect collides with the ball and the ball is in front of it,
            change the speed of the ball and make it move a little in the opposite direction
            """

            if paddle_1_rect.colliderect(ball_rect) and ball_accel_x < 0:
                ball_accel_x *= -1
                ball_rect.left = paddle_1_rect.right

            # Repeat with paddle_2_rect
            if paddle_2_rect.colliderect(ball_rect) and ball_accel_x > 0:
                ball_accel_x *= -1
                ball_rect.right = paddle_2_rect.left
        
        pygame.draw.rect(screen, COLOR_WHITE, paddle_1_rect)
        pygame.draw.rect(screen, COLOR_WHITE, paddle_2_rect)
        pygame.draw.rect(screen, COLOR_WHITE, ball_rect)
        #pygame.display.update()

        # Display scores
        score_text =  font.render(f"{player1_name}: {score_1} - {player2_name}: {score_2}", True, COLOR_WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(score_text, score_rect)
        # Update the display
        pygame.display.flip()
        clock.tick(60)



# Run the game
if __name__ == '__main__':
    main()

