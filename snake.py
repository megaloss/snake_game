import pygame
import random
pygame.init()
WIDTH = 600
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("comicsans", 30, True)
font_end = pygame.font.SysFont("comicsans", 50, True)
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
# size of a block in snake's body
width = 19
height = 19


def move(body, direction, apple, score):
    res = ''
    # dictionary to translate direction into vector
    moves = {'L': [-1, 0],
             'R': [1, 0],
             'U': [0, -1],
             'D': [0, 1],
             }
    # find a place to put a new block if the snake extends
    end_x, end_y = body[-1]

    # move - every block follows the previous one
    if len(body) > 1:
        for i in range(len(body)-1, 0, -1):
            body[i] = body[i-1].copy()
    # head moves depending on direction
    body[0][0] = body[0][0] + moves[direction][0]
    body[0][1] = body[0][1] + moves[direction][1]
    # check on collision with itself
    if body[0] in body[1:]:
        res = 'You hit yourself and died !'
    # check if we hit the wall
    if body[0][0] < 1 or body[0][0] > 27 or body[0][1] < 1 or body[0][1] > 27:
        res = 'You hit the wall and died !'
    # check on collision with an apple
    if list(apple) in body:
        body.append([end_x, end_y])
        score += 1
        apple = set_apple(body)

    return body, apple, score, res


def end_of_game(text):
    # print text and wait 3 sec
    text = font_end.render(str(text), 1, (200, 100, 100))
    win.blit(text, (30, 300))
    pygame.display.update()
    pygame.time.delay(3000)


def redraw(body, apple, score, direction):
    # clear screen
    win.fill((0, 0, 0))
    # dictionary for eye positions
    eyes = {'L': ((5, 5), (5, 15)),
            'R': ((15, 5), (15, 15)),
            'U': ((15, 5), (5, 5)),
            'D': ((15, 15), (5, 15)),
            }
    # draw the game boarder
    pygame.draw.rect(win, (155, 155, 155), (0, 0, WIDTH-20, HEIGHT-20), 20)
    # draw the snake body block-by-block
    for part in body:
        pygame.draw.rect(win, (55, 255, 55), (part[0]*20, part[1]*20, width, height))

    # define a position for both eye depending on direction
    eye1, eye2 = eyes[direction]
    eye1_x = body[0][0]*20+eye1[0]
    eye1_y = body[0][1]*20+eye1[1]
    eye2_x = body[0][0]*20+eye2[0]
    eye2_y = body[0][1]*20+eye2[1]
    # and draw them
    pygame.draw.circle(win, (200, 200, 200), (eye1_x, eye1_y), 5)
    pygame.draw.circle(win, (200, 200, 200), (eye2_x, eye2_y), 5)
    pygame.draw.circle(win, (0, 0, 20), (eye1_x, eye1_y), 2)
    pygame.draw.circle(win, (0, 0, 20), (eye2_x, eye2_y), 2)
    # draw the apple
    pygame.draw.circle(win, (255, 50, 50), (apple[0]*20+10, apple[1]*20+10), 10)
    # print score
    text = font.render("Score: " + str(score), 1, (100, 100, 200))
    win.blit(text, (390, 10))
    # update screen
    pygame.display.update()


def set_apple(body):
    # placing a new apple outside snake's body
    while True:
        x = random.randint(1, 27)
        y = random.randint(1, 27)
        if [x, y] not in body:
            return x, y


def main():
    run = True
    score = 0
    # starting position and direction
    x, y = 5, 5
    direction = 'R'
    # we start with 3-blocks body
    body = [[x, y], [x - 1, y], [x - 2, y]]
    # place a new apple
    apple = set_apple(body)
    while run:
        clock.tick(8+int(score/10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            direction = 'L'

        if keys[pygame.K_RIGHT]:
            direction = 'R'

        if keys[pygame.K_UP]:
            direction = 'U'

        if keys[pygame.K_DOWN]:
            direction = 'D'

        if keys[pygame.K_q]:
            pygame.quit()
        # move snake
        body, apple, score, res = move(body, direction, apple, score)
        # draw screen
        redraw(body, apple, score, direction)
        # end game if we got a signal
        if res:
            end_of_game(res)
            run = False

    main()


main()
