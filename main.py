import pygame


class WindowPage:
    def __init__(self):
        self.SAKURA_PINK = (254, 223, 225)
        self.MINT = (186, 216, 185)
        self.BLUE = (119, 150, 154)
        self.PURPLE = (143, 119, 181)
        self.SCREEN = pygame.display.set_mode((1000, 600))
        self.SCREEN.fill(pygame.Color('white'))
        pygame.display.set_caption("game")

class GamePage(WindowPage):
    def functionBlock(self):
        self.FORWARD = pygame.Surface((150, 40))
        pygame.draw.rect(self.FORWARD, self.BLUE, (620, 20, 150, 40))
        self.LEFT = pygame.Surface((150, 40))
        pygame.draw.rect(self.LEFT, self.BLUE, (620, 80, 150, 40))
        self.RIGHT = pygame.Surface((150, 40))
        pygame.draw.rect(self.RIGHT, self.BLUE, (620, 140, 150, 40))
        self.IF = pygame.Surface((150, 40))
        pygame.draw.rect(self.IF, self.PURPLE, (800, 20, 150, 40))
        pygame.draw.rect(self.SCREEN, self.SAKURA_PINK, (600, 0, 395, 200))
        pygame.draw.rect(self.SCREEN, self.MINT, (600, 205, 395, 390))


        pygame.display.update()


if __name__ == '__main__':
    GamePage().functionBlock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()
