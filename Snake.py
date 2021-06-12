#!/usr/bin/python3

import pygame
from random import randrange


class Circle:
    count = -1

    def __init__(self, radius, color=(0, 255, 0)):
        self.radius = radius
        self.color = color
        self.x = 0
        self.y = 0
        self.count = Circle.count + 1

    def display(self, screen):
        # self.x = self.x + x
        # self.y = self.y + y
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def collided(self, obj):
        return ((obj.x - self.x)**2 + (obj.y - self.y)**2)**(0.5) <= obj.radius + self.radius


class Foods:
    count = -1

    def __init__(self, radius, color=(0, 255, 0), x=0, y=0):
        self.radius = radius
        self.color = color
        self.x = x
        self.y = y
        Foods.count = Foods.count + 1
        self.count = Foods.count

    def display(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


def game_continue():
    #WHITE = (255, 255, 255)
    #font = pygame.font.SysFont('calibri', 32)
    #text = font.render('Game Over', True, WHITE)
    #textRect = text.get_rect()
    #textRect.center = (width // 2, height // 2)
    #screen.blit(text, textRect)
    return False


def main():
    width = 1200
    height = 1200
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    middle_x = width // 2
    middle_y = height // 2
    y = 0
    x = 0

    # Game Over text
    font = pygame.font.SysFont('calibri', 32)
    gameOverText = font.render('Game Over', True, WHITE)
    gameOverRect = gameOverText.get_rect()
    gameOverRect.center = (middle_x, middle_y)

    # Continue text
    continueText = font.render('Continue: [Yes] [No]', True, WHITE)
    continueTextRect = continueText.get_rect()
    continueTextRect.center = (middle_x, middle_y + 50)

    circle = Circle(20)
    circle.x = middle_x
    circle.y = middle_y
    food = Foods(5, WHITE, randrange(0, width), randrange(0, height))

    clock = pygame.time.Clock()

    snake = []
    snake.append(circle)

    foodsAr = []
    foodsAr.append(food)

    running = True
    old_x = 0
    old_y = 0
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        # arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            x = 1
            y = 0
        if keys[pygame.K_LEFT]:
            x = -1
            y = 0
        if keys[pygame.K_UP]:
            x = 0
            y = -1
        if keys[pygame.K_DOWN]:
            x = 0
            y = 1

        screen.fill(BLACK)

        # rng = randrange(0, 61)
        # if rng == 60:
        # newFood = Foods(5, WHITE, randrange(0, width), randrange(0, height))
        # foodsAr.append(newFood)

        # if list is not empty display
        if foodsAr:
            for index, f in enumerate(foodsAr):
                f.count = index
                f.display(screen)

        # display the circles
        old_x = snake[0].x
        old_y = snake[0].y

        # TODO fix this shit
        for index, s in enumerate(snake):
            # bound check for now
            # if s.y + y < height and s.y + y >= 0:
            #s.y = s.y + y
            # if s.x + x < width and s.x + x >= 0:
            #s.x = s.x + x
            temp_x = s.x
            temp_y = s.y

            s.x = old_x + x
            s.y = old_y + y

            old_x = temp_x
            old_y = temp_y

            if index > 0:
                if x > 0:
                    s.x = s.x + (-1)
                if x < 0:
                    s.x = s.x + (1)
                if y > 0:
                    s.y = s.y + (-1)
                if y < 0:
                    s.y = s.y + (1)

            # adjust location of snake
            s.display(screen)
        # circle.display(middle_x, middle_y)
        pygame.display.update()

        # if head of snake eats tail
        for index, s in enumerate(snake):
            if index > 60:
                if (snake[0].collided(s)):
                    screen.blit(gameOverText, gameOverRect)
                    pygame.display.update()
                    running = False

        # Check if snake is within bounds
        if snake[0].x in (0, width, height) or snake[0].y in (0, width, height):
            screen.blit(gameOverText, gameOverRect)
            pygame.display.update()
            running = False

        # clear the that specific food form list then create extend snake
        if foodsAr:
            for f in foodsAr:
                if (snake[0].collided(f)):
                    foodsAr.pop(f.count)
                    # new part of snake
                    # depending head
                    for _ in range(60):
                        newCircle = Circle(20)
                        newCircle.x = snake[-1].x
                        newCircle.y = snake[-1].y
                        if x > 0:
                            newCircle.x = newCircle.x + (-1)
                        if x < 0:
                            newCircle.x = newCircle.x + (1)
                        if y > 0:
                            newCircle.y = newCircle.y + (-1)
                        if y < 0:
                            newCircle.y = newCircle.y + (1)
                        newCircle.display(screen)
                        pygame.display.update()
                        snake.append(newCircle)
                    # create new food
                    food = Foods(5, WHITE, randrange(0, width), randrange(0, height))
                    foodsAr.append(food)

        clock.tick(150)

    # To continue game
    screen.blit(continueText, continueTextRect)
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                # Yes
                if mouse[0] in range(middle_x + 5, middle_x + 72) and mouse[1] in range(middle_y + 38, middle_y + 66):
                    running = False
                    main()
                # No
                elif mouse[0] in range(middle_x + 85, middle_x + 138) and mouse[1] in range(middle_y + 38, middle_y + 66):
                    running = False
                # if continueTextRect.collidepoint(pygame.mouse.get_pos()):
                    # print('Pressed')
                    # print(pygame.mouse.get_pos())

    pygame.quit()


if __name__ == "__main__":
    main()
