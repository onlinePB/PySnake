import pygame
import sys
import random
import tkinter as tk
from tkinter import ttk

FPS_LIMIT = 11

WIN_WIDTH = 800
WIN_HEIGHT = 800
PIXEL_SIZE = 40

BG_COLOUR = (186, 222, 252)
BG_COLOUR_ALT = (98, 181, 248)
SNAKE_COLOUR = (50, 168, 82)
GOAL_COLOUR = (240, 97, 36)

APP_INFO = """
Made by Ryan W.

View the source code here:
https://github.com/onlinePB/PySnake

Controls:
Use the arrow keys to move
Use the space bar to pause the game

To begin, press 'Start' below.
"""


def get_random_location():
    x = random.randint(0, ((WIN_WIDTH - PIXEL_SIZE) / PIXEL_SIZE)) * PIXEL_SIZE
    y = random.randint(0, ((WIN_HEIGHT - PIXEL_SIZE) / PIXEL_SIZE)) * PIXEL_SIZE
    return [x, y]


class Snake():
    def __init__(self):
        self.length = 1
        self.body = [get_random_location()]
        self.direction = {"x": -1, "y": 0}
        self.paused = False
        self.grow = False

    def get_head(self):
        return self.body[0]

    def get_next_position(self, travel_direction = None):
        if travel_direction is None:
            travel_direction = self.direction

        head = self.get_head()
        return [ (head[0] + (travel_direction["x"] * PIXEL_SIZE)), (head[1] + (travel_direction["y"] * PIXEL_SIZE)) ]

    def move(self):
        if not self.paused:
            next_pos = self.get_next_position()
            
            # Check if next position is out of bounds, and go to opposite side if it is
            for i in range(2):
                max_value = WIN_WIDTH if i == 0 else WIN_HEIGHT

                if next_pos[i] < 0:
                    next_pos[i] = max_value - PIXEL_SIZE
                elif next_pos[i] > max_value - PIXEL_SIZE:
                    next_pos[i] = 0


            if len(self.body) > 1 and next_pos in self.body:
                self.reset()

            else:
                self.body.insert(0, next_pos)

                if self.grow:
                    self.grow = False
                else:
                    self.body.pop()
                    
    
    def toggle_grow(self):
        if not self.grow:
            self.grow = True

    def set_direction(self, new_direction):
        if not self.paused:
            if len(self.body) > 1 and self.get_next_position(new_direction) == self.body[1]:
                pass
            else:
                self.direction = new_direction

    def reset(self):
        head = self.get_head()
        self.body.clear()
        self.body.insert(0, head)

    def draw(self, window):
        for body_part in self.body:
            snake_pixel = pygame.Rect(body_part[0], body_part[1], PIXEL_SIZE, PIXEL_SIZE)
            pygame.draw.rect(window, SNAKE_COLOUR, snake_pixel)

    def toggle_paused(self):
        if self.paused:
            self.paused = False
        else:
            self.paused = True

class Goal():
    def __init__(self):
        self.location = get_random_location()

    def get_location(self):
        return self.location

    def set_location(self, new_pos):
        self.location = new_pos

    def draw(self, window):
        goal_pixel = pygame.Rect(self.location[0], self.location[1], PIXEL_SIZE, PIXEL_SIZE)
        pygame.draw.rect(window, GOAL_COLOUR, goal_pixel)



def draw_background(window):
    for x in range(0, WIN_WIDTH, PIXEL_SIZE):
        for y in range(0, WIN_HEIGHT, PIXEL_SIZE):
            tile = pygame.Rect(x, y, PIXEL_SIZE, PIXEL_SIZE)

            # Alternate the colour of the background tiles
            if ((x + y) / PIXEL_SIZE) % 2 == 0:
                colour = BG_COLOUR
            else:
                colour = BG_COLOUR_ALT

            pygame.draw.rect(window, colour, tile)

def input_listener(player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.set_direction({"x": 0, "y": -1})

            elif event.key == pygame.K_RIGHT:
                player.set_direction({"x": 1, "y": 0})

            elif event.key == pygame.K_DOWN:
                player.set_direction({"x": 0, "y": 1})

            elif event.key == pygame.K_LEFT:
                player.set_direction({"x": -1, "y": 0})

            elif event.key == pygame.K_SPACE:
                player.toggle_paused()
            
def show_app_info():
    info_window = tk.Tk()
    info_window.title("About")
    info_window.configure(bg="white")

    description = tk.Label(info_window, text=APP_INFO)
    description.pack(side="top", fill="x", pady=5, padx=10)
    description.configure(bg="white")
    
    button = ttk.Button(info_window, text="Start", command=info_window.destroy)
    button.pack()

    info_window.mainloop()

def main():

    show_app_info()

    pygame.init()

    clock = pygame.time.Clock()
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Snake")

    draw_background(window)
    snake = Snake()
    goal = Goal()

    # Game loop
    running = True
    while running:
        clock.tick(FPS_LIMIT)
        
        input_listener(snake)
        snake.move()
        
        if snake.get_head() == goal.get_location():
            snake.toggle_grow()
            
            while True:
                new_goal_loc = get_random_location()

                if new_goal_loc is not goal.get_location():
                    break

            goal.set_location(new_goal_loc)

        # Draw elements
        draw_background(window)
        snake.draw(window)
        goal.draw(window)

        pygame.display.update()
        

if __name__ == "__main__":
    main()
    