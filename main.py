import pygame


class WindowPage:
    def __init__(self):
        pygame.init()
        self.SAKURA_PINK = (254, 223, 225)
        self.SCREEN = pygame.display.set_mode((1000, 600))
        GamePage().functionBlock()

class GamePage(WindowPage):
    def functionBlock(self):
        self.SCREEN.fill(pygame.Color('white'))
        pygame.display.set_caption("game")
        pygame.draw.rect(self.SCREEN, self.SAKURA_PINK, (600, 0, 400, 600))
        pygame.display.update()


if __name__ == '__main__':
    WindowPage()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()
