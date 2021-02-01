import pygame
import random
pygame.init()
WIDTH = 600
HEIGHT = 600
win = pygame.display.set_mode((WIDTH,HEIGHT))
font = pygame.font.SysFont("comicsans", 30, True)
font_end = pygame.font.SysFont("comicsans", 50, True)
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()


width = 20
height = 20
vel = 1




def move(body, direction, apple, score):
    res=''
    moves = {'L': [-1, 0],
             'R': [1, 0],
             'U': [0, -1],
             'D': [0, 1],
             }
    end_x,end_y=body[-1]
    if len(body)>1:
        for i in range (len(body)-1,0,-1):
            body[i]=body[i-1].copy()

    body[0][0]=body[0][0] + moves[direction][0]*vel
    body[0][1] = body[0][1] + moves[direction][1] * vel
    if body[0] in body[1:]:
        res = 'You hit yourself and died !'
    if body[0][0]<1 or body[0][0]>27 or body[0][1]<1 or body[0][1]>27:
        res = 'You hit the wall and died !'
        print (body)

    if list(apple) in body:
        body.append([end_x,end_y])
        score += 1
        apple = set_apple(body)

    return body,apple,score,res

def blit_text(text):
    text = font_end.render(str(text),1, (200, 100, 100))  # Arguments are: text, anti-aliasing, color
    win.blit(text, (30, 300))
    pygame.display.update()
    pygame.time.delay(3000)

def redraw(body,apple,score,direction):
    win.fill((0, 0, 0))
    eyes = { 'L': ((5, 5), (5, 15)),
             'R': ((15, 5), (15, 15)),
             'U': ((15, 5), (5, 5)),
             'D': ((15, 15), (5, 15)),
             }
    pygame.draw.rect(win, (155, 155, 155), (0, 0, WIDTH-20, HEIGHT-20),20)
    for part in body:
        pygame.draw.rect(win, (55, 255, 55), (part[0]*20, part[1]*20, width, height))
    eye1, eye2 = eyes[direction]

    eye1_x = body[0][0]*20+eye1[0]
    eye1_y = body[0][1]*20+eye1[1]
    eye2_x = body[0][0]*20+eye2[0]
    eye2_y = body[0][1]*20+eye2[1]


    pygame.draw.circle(win,(200,200,200),(eye1_x, eye1_y),5)
    pygame.draw.circle(win, (200, 200, 200), (eye2_x, eye2_y), 5)
    pygame.draw.circle(win,(0,0,20),(eye1_x, eye1_y),2)
    pygame.draw.circle(win, (0, 0, 20), (eye2_x, eye2_y), 2)

    pygame.draw.circle(win, (255, 50, 50), (apple[0]*20+10,apple[1]*20+10), 10)
    text = font.render("Score: " + str(score), 1, (100, 100, 200))  # Arguments are: text, anti-aliasing, color
    win.blit(text, (390, 10))
    pygame.display.update()


def set_apple(body):
    while True:
        x = random.randint(1,19)
        y = random.randint(1,19)
        if [x, y] not in body:
            return x, y

def main():
    run = True
    score = 0
    x = 5
    y = 5
    direction = 'R'
    body = [[x, y], [x - 1, y], [x - 2, y]]

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

        body, apple, score, res = move(body, direction, apple, score)
        redraw(body, apple, score, direction)
        if res:
            blit_text(res)
            run = False


    main()

main()
