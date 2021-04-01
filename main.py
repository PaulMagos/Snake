import random
import pygame
import time


class square(object):
    rows = 20
    dim = 700

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 255, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False, circle=False):
        distance = self.dim // self.rows
        i = self.pos[0]
        j = self.pos[1]

        if not circle:
            pygame.draw.rect(surface, self.color, (i * distance + 1, j * distance + 1, distance - 2, (distance - 1)))
        else:
            pygame.draw.circle(surface, self.color,
                               (i * distance + distance // 2 + 1, j * distance + distance // 2 + 1), distance // 2)
        if eyes:
            centre = distance // 2
            radius = 3.5
            circleMiddle = (i * distance + centre - radius * 2, j * distance + 8)
            circleMiddle2 = (i * distance + distance - radius * 2, j * distance + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = square(pos)
        self.body.append(self.head)
        self.xAxis = 0
        self.yAxis = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    if not len(self.body) == 1:
                        if (self.body[0].pos[0] - 1, self.body[0].pos[1]) == self.body[1].pos:
                            continue
                    self.xAxis = -1
                    self.yAxis = 0
                    self.turns[self.head.pos[:]] = [self.xAxis, self.yAxis]
                if keys[pygame.K_RIGHT]:
                    if not len(self.body) == 1:
                        if (self.body[0].pos[0] + 1, self.body[0].pos[1]) == self.body[1].pos:
                            continue
                    self.xAxis = 1
                    self.yAxis = 0
                    self.turns[self.head.pos[:]] = [self.xAxis, self.yAxis]
                if keys[pygame.K_UP]:
                    if not len(self.body) == 1:
                        if (self.body[0].pos[0], self.body[0].pos[1] - 1) == self.body[1].pos:
                            continue
                    self.xAxis = 0
                    self.yAxis = -1
                    self.turns[self.head.pos[:]] = [self.xAxis, self.yAxis]
                if keys[pygame.K_DOWN]:
                    if not len(self.body) == 1:
                        if (self.body[0].pos[0], self.body[0].pos[1] + 1) == self.body[1].pos:
                            continue
                    self.xAxis = 0
                    self.yAxis = 1
                    self.turns[self.head.pos[:]] = [self.xAxis, self.yAxis]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                if c == self.body[0]:
                    if not len(self.body) == 1:
                       if (c.pos[0] + turn[0], c.pos[1] + turn[1]) == self.body[1].pos:
                            continue
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)

            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = square(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def increaseDim(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        self.body.append(square((tail.pos[0] - dx, tail.pos[1] - dy)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(dim, rows, surface):
    blockSize = dim // rows

    for l in range(1, rows):
        pygame.draw.line(surface, (100, 100, 100), (l * blockSize, 0), (l * blockSize, dim))
        pygame.draw.line(surface, (100, 100, 100), (0, l * blockSize), (dim, l * blockSize))


def refreshWIN(surface):
    global dim, rows, snak, snack
    surface.fill((0, 0, 0))
    snak.draw(surface)
    snack.draw(surface, circle=True)
    drawGrid(dim, rows, surface)
    pygame.display.update()


def spawnSnack(rows, item):
    positions = item.body

    while True:
        y = random.randrange(rows)
        x = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return x, y


def main():
    global dim, rows, snak, snack
    dim = 700
    rows = 20
    win = pygame.display.set_mode((dim, dim))

    snak = snake((255, 0, 0), (10, 10))
    snack = square(spawnSnack(rows, snak), color=(0, 0, 255))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(40)
        clock.tick(10)
        snak.move()
        if snak.body[0].pos == snack.pos:
            snak.increaseDim()
            snack = square(spawnSnack(rows, snak), color=(0, 0, 255))

        for x in range(len(snak.body)):
            if snak.body[x].pos in list(map(lambda z: z.pos, snak.body[x + 1:])):
                print("Score: ", len(snak.body))
                print("You lose")
                snak.reset((10, 10))
                time.sleep(3)
                break

        refreshWIN(win)

    pass

main()
