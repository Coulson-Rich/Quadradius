import pygame
from ex_server_client.network import Network

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0

class Player():
    def __init__(self, x, y, width, height, color):
        self.y = y
        self.x = x
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.val = 3
        
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
    
    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.x -= self.val
        if keys[pygame.K_RIGHT]:
            self.x += self.val
        if keys[pygame.K_UP]:
            self.y -= self.val
        if keys[pygame.K_DOWN]:
            self.y += self.val
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])



def redrawWindow(win, player, p2):
    win.fill((255,255,255))
    player.draw(win)
    p2.draw(win)
    pygame.display.update()

def main():
    run = True
    n = Network()
    startpos = read_pos(n.getPos())
    p = Player(startpos[0],startpos[1],100,100,(0,255,0))
    p2 = Player(0,0,100,100,(0,255,0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        p.move()
        n.send(make_pos((p.x,p.y)))

        p2pos = read_pos(n.send(make_pos((p.x,p.y))))
        p2.x = p2pos[0]
        p2.y = p2pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        redrawWindow(win, p, p2)
main()

