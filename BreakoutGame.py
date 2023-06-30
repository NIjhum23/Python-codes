import pygame
from pygame.locals import *
import time

pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')

# Define font
font = pygame.font.SysFont('Constantia', 30)

# Define colors
bg = (234, 218, 184)

# Block colors
red_block = (242, 85, 96)
green_block = (86, 174, 87)
blue_block = (69, 177, 233)

# Paddle color
paddle_color = (142, 135, 123)
paddle_outline = (100, 100, 100)

# Text colors
text_color = (78, 81, 139)




# Define game variables
cols = 6
rows = 6
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = 0


# Function for outputting text onto the screen
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

# Brick wall class

class wall():
    def __init__(self):
        self.width = screen_width // cols
        self.height = 50

    def create_wall(self):
        self.blocks = []
        # Define an empty list for a individual block
        individual_block = []
        for row in range(rows):
            #reset the block row list
            row_block = []
            # Iterate through each column throgh that row
            for col in range(cols):
                # Generate x and y positions for each block and create a rectangle from that
                x_block = col  * self.width
                y_block = row * self.height
                rect = pygame.Rect(x_block, y_block, self.width, self.height)
                # Assign block strength
                if row<2:
                    strength = 3
                elif row<4:
                    strength = 2
                elif row<6:
                    strength = 1
                # Create a list to store the rect and color data
                individual_block = [rect, strength]
                # Append that individual block to row block
                row_block.append(individual_block)
            # Append the row to the whole list
            self.blocks.append(row_block)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                # Assign a color based on block strength
                if block[1] == 3:
                    col_block = blue_block
                elif block[1] == 2:
                    col_block = green_block
                elif block[1] == 1:
                    col_block = red_block
                pygame.draw.rect(screen, col_block, block[0])
                pygame.draw.rect(screen, bg, (block[0]), 2)
                
# Paddle class
class paddle():
    def __init__(self):
        self.reset()


    def move(self):
        # Reset movement direction
        self.directon = 0
        key = pygame.key.get_pressed()
        if (key[pygame.K_LEFT] and self.rect.left >0) :
            self.rect.x -= self.speed
            self.directon = -1

        elif (key[pygame.K_RIGHT] and self.rect.right < screen_width) :
            self.rect.x += self.speed
            self.directon = 1
    
    def draw(self):
        pygame.draw.rect(screen, paddle_color, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)
    
    def reset(self):
        # Define paddle variables
        self.height = 20
        self.width = int(screen_width / cols)
        self.x = int((screen_width / 2) - (self.width / 2))
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.directon = 0


# Create ball class
class game_ball():
    def __init__(self, x, y):
        self.reset(x,y)



    def move(self):

        # Collision threshold
        collision_thresh = 5

        # Start off with the assumption that the wall has been destroyed completely
        wall_destroyed = 1
        row_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                # Check collision
                if self.rect.colliderect(item[0]):
                    # Check if collision is from above
                    if abs(self.rect.bottom - item[0].top) < collision_thresh  and self.speed_y > 0 :
                        self.speed_y *= -1
                    # Check if collision is from below
                    if abs(self.rect.top - item[0].bottom) < collision_thresh  and self.speed_y < 0 :
                        self.speed_y *= -1
                    # Check if collision is from left
                    if abs(self.rect.right - item[0].left) < collision_thresh  and self.speed_x > 0 :
                        self.speed_x *= -1
                    # Check if collision is from left
                    if abs(self.rect.left - item[0].right) < collision_thresh  and self.speed_x < 0 :
                        self.speed_x *= -1
                    # Reduce the block strength by doing damage to it
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] = (0,0,0,0,)
                # Check if block still exists, in which case the wall is not destroyed
                if wall.blocks[row_count][item_count][0] != (0,0,0,0) :
                    wall_destroyed = 0
                # Increase item counter
                item_count += 1
            # Increase row counter
            row_count += 1
        # After iterating through all the blocks, check if the wall is destroyed
        if wall_destroyed == 1:
            self.game_over = 1
                        

        # Check for collisios with paddle
        if self.rect.colliderect(player_paddle):
            # Check if colliding from top
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.directon
                if self.speed_x > self.speed_max :
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max :
                    self.speed_x = -self.speed_max
            else:
                self.speed_x *= -1        



        # Check for collisions with the wall
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1

        # Check for collisions with top and bottom of the screen
        if self.rect.top < 0:
            self.speed_y *= -1
        
        elif self.rect.bottom > screen_height:
            self.game_over = -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over
    

        
    def draw(self):
        pygame.draw.circle(screen, paddle_color, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad, 3)
        


    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0



# Create wall                
wall = wall()
wall.create_wall()       

# Create paddle
player_paddle = paddle()

# Create ball
ball = game_ball(player_paddle.x + (player_paddle.width // 2), (player_paddle.y - player_paddle.height))



run = True
while run:
    
    clock.tick(fps)
    screen.fill(bg)


    # Draw all objects
    wall.draw_wall()  
    player_paddle.draw()  
    ball.draw()


    if live_ball:        
        # Draw paddle
        player_paddle.move()
        # Draw ball
        game_over = ball.move()
        if game_over != 0 :
            live_ball = False
    

    if not live_ball:
        if game_over == 0:
            draw_text('CLICK ANYWHERE TO START', font, text_color, 100, screen_height // 2 + 100)
        elif game_over == 1:
            draw_text('YOU WON!', font, text_color, 240, screen_height // 2 + 50)
            draw_text('CLICK ANYWHERE TO START', font, text_color, 100, screen_height // 2 + 100)
        elif game_over == -1:
            draw_text('YOU LOST!', font, text_color, 240, screen_height // 2 + 50)
            draw_text('CLICK ANYWHERE TO START', font, text_color, 100, screen_height // 2 + 100)

    



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            ball.reset(player_paddle.x +(player_paddle.width // 2), player_paddle.y - player_paddle.height)
            player_paddle.reset()
            wall.create_wall
    
    pygame.display.update()

pygame.quit()


