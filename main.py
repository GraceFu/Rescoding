import pygame

class WindowPage:
    def __init__(self):
        pygame.init()
        pygame.font.get_fonts()
        self.PINK = (254, 223, 225, 127)
        self.MINT = (186, 216, 185, 127)
        self.BLUE = (119, 150, 154)
        self.PURPLE = (143, 119, 181)
        self.BLACK = (0, 0, 0)

        self.font = pygame.font.SysFont("monospace", 20)
        self.text_forward = None
        self.text_left = None
        self.text_right = None
        self.text_if = None

        self.SCREEN = pygame.display.set_mode((1000, 600))
        self.SCREEN.fill(pygame.Color('white'))
        pygame.display.set_caption("game")


class GamePage(WindowPage):
    def functionBlock(self):
        pygame.draw.rect(self.SCREEN, self.PINK, (600, 0, 395, 200))
        pygame.draw.rect(self.SCREEN, self.MINT, (600, 205, 395, 390))
        pygame.draw.rect(self.SCREEN, self.BLUE, (620, 20, 150, 40))
        pygame.draw.rect(self.SCREEN, self.BLUE, (620, 80, 150, 40))
        pygame.draw.rect(self.SCREEN, self.BLUE, (620, 140, 150, 40))
        pygame.draw.rect(self.SCREEN, self.PURPLE, (800, 20, 150, 40))

        self.text_forward = self.font.render("forward", False, self.BLACK)
        self.text_left = self.font.render("left", False, self.BLACK)
        self.text_right = self.font.render("right", False, self.BLACK)
        self.text_if = self.font.render("if", False, self.BLACK)
        self.SCREEN.blit(self.text_left, (620+150//4, 20+40//4))
        self.SCREEN.blit(self.text_left, (620+150//4, 80+40//4))
        self.SCREEN.blit(self.text_right, (620+150//4, 140+40//4))
        self.SCREEN.blit(self.text_if, (800+150//4, 20+40//4))
        pygame.display.update()


if __name__ == '__main__':
    GP = GamePage()
    GP.functionBlock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()
