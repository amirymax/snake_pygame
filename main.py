import pygame as p
import random
from snake_snacks.point import Point
from snake_snacks.directions import Direction
from snake_snacks.other_variables_stuff import *

pygame.init()


class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = p.display.set_mode((self.w, self.h))
        p.display.set_caption('Snake')
        self.clock = p.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self.the_apple()

    def move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

    def the_apple(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self.the_apple()

    def collided(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True

        return False

    def go_for_apple(self):
        # 1. collect user input
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                quit()
            if event.type == p.KEYDOWN:
                if event.key == p.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == p.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == p.K_UP:
                    self.direction = Direction.UP
                elif event.key == p.K_DOWN:
                    self.direction = Direction.DOWN

        # 2. move
        self.move(self.direction)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        game_over = False
        if self.collided():
            game_over = True
            return game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self.the_apple()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self.update()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def update(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            p.draw.rect(self.display, GREEN, p.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            p.draw.rect(self.display, GREEN2, p.Rect(pt.x + 4, pt.y + 4, 12, 12))

        p.draw.rect(self.display, RED, p.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        p.display.flip()


if __name__ == '__main__':
    game = SnakeGame()

    # game loop
    while True:
        game_over, score = game.go_for_apple()

        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()
