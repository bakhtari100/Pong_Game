# Import necessary libraries
import pygame
import random
import math





# Constants for the windows width and height values
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

# Assign HP colors to variables
WING_COLOR = (220, 220, 220)
GREY = (128, 128, 128)  
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLOR_SNITCH = (212, 175, 55)
COLOR_WAND = (101, 67, 33)
HOUSE_COLORS = {
    "Gryffindor": (124, 0, 0),
    "Slytherin": (0, 70, 0),
    "Hufflepuff": (200, 170, 0),
    "Ravenclaw": (0, 0, 100)

}


def main():
    # GAME SETUP

    pygame.init()

    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Harry Potter Pong")

    # Create the clock object to keep track of the time
    clock = pygame.time.Clock()


    
    paddle_1_rect = pygame.Rect(30, 0, 10, 100)  
    paddle_2_rect = pygame.Rect(SCREEN_WIDTH - 50, 0, 10, 100)   
    
    
    paddle_1_move = 0   
    paddle_2_move = 0   
    
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
    def get_input(prompt):
        name = ""
        entering = True
        while entering:
            screen.fill(GREY)
            text_surface = font.render(f"{prompt}: {name}", True, WHITE)
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
    player1_name = get_input("Enter Player 1 Name")
    player1_house = get_input(f"Enter {player1_name}'s Hogwarts House").capitalize()
    if player1_house not in HOUSE_COLORS:
        player1_house = "Gryffindor"

    # Get the players' names and houses
    player2_name = get_input("Enter Player 2 Name")
    player2_house = get_input(f"Enter {player2_name}'s Hogwarts House").capitalize()
    if player2_house not in HOUSE_COLORS:
        player2_house = "Slytherin"
    pygame.event.clear() 
    started = False



    # Reset the ball to the center of the screen and randomize its direction
    def reset_ball():
        nonlocal ball_rect, ball_accel_x, ball_accel_y
        ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        ball_accel_x = random.choice([-1, 1]) * random.randint(2, 4) * 0.09
        ball_accel_y = random.choice([-1, 1]) * random.randint(2, 4) * 0.09
    
    # Display the winner and pause before quitting
    def show_winner(winner_name, winner_house):
        text = font.render(f"{winner_name} wins the House Cup for {winner_house}!", True, WHITE)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.fill(HOUSE_COLORS[winner_house])
        screen.blit(text, rect)
        pygame.display.flip()
        pygame.time.delay(5000)
        pygame.quit()
        exit()

    frame_count = 0
        
    def draw_snitch(ball_rect, frame_count):
        pygame.draw.circle(screen, COLOR_SNITCH, ball_rect.center, ball_rect.width // 2) 

        
        
        x, y = ball_rect.center
        r = ball_rect.width // 2


        # Animate wings flapping
        flap = int(5 * math.sin(frame_count * 0.3)) 

        # Draw wings using polygons
        pygame.draw.polygon(screen, WING_COLOR, [
            (x - r - 8, y), 
            (x - r - 2, y - 8), 
            (x - r - 2, y + 8)
            ])
        pygame.draw.polygon(screen, WING_COLOR, [
            (x + r + 8, y), 
            (x + r + 2, y - 8), 
            (x + r + 2, y + 8)
            ])


  
    while True:


        screen.fill(BLACK)

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
                    if event.key == pygame.K_w:
                        paddle_1_move = -0.5
                    if event.key == pygame.K_s:
                        paddle_1_move = 0.5

                    # PLAYER 2
                    if event.key == pygame.K_UP:
                        paddle_2_move = -0.5
                    if event.key == pygame.K_DOWN:
                        paddle_2_move = 0.5
                
                # if player released a key
                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_w, pygame.K_s):
                        paddle_1_move = 0.0
                    if event.key in (pygame.K_UP, pygame.K_DOWN):
                        paddle_2_move = 0.0


    
        if not started:
            #font = pygame.font.SysFont('Consolas', 30)
            text = font.render('Press Space to Start', True, WHITE)
            text_rect = text.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
        else:
            
            delta_time = clock.tick(60)

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
                show_winner(player1_name, player1_house)
            if score_2 >= 5:
                show_winner(player2_name, player2_house)


            if paddle_1_rect.colliderect(ball_rect) and ball_accel_x < 0:
                ball_accel_x *= -1
                ball_rect.left = paddle_1_rect.right

            # Repeat with paddle_2_rect
            if paddle_2_rect.colliderect(ball_rect) and ball_accel_x > 0:
                ball_accel_x *= -1
                ball_rect.right = paddle_2_rect.left
        
        pygame.draw.rect(screen, COLOR_WAND, paddle_1_rect)
        pygame.draw.rect(screen, COLOR_WAND, paddle_2_rect)
        
        draw_snitch(ball_rect, frame_count)
        frame_count += 1

        # Display scores
        score_text =  font.render(f"{player1_name}: {score_1} - {player2_name}: {score_2}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(score_text, score_rect)
        # Update the display
        pygame.display.flip()
        clock.tick(60)



# Run the game
if __name__ == '__main__':
    main()

