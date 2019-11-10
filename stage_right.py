import pygame

# Define colors
PINK = (254, 223, 225)
MINT = (186, 216, 185)


class stageRight:
    SCREEN = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Rescoding")
    SCREEN.fill(pygame.Color('white'))

    def __init__(self):
        pygame.init()
        self.close_clicked = False
        self.continue_game = True
        self.f = pygame.image.load('forward.png')
        self.l = pygame.image.load('left.png')
        self.r = pygame.image.load('right.png')
        self.i = pygame.image.load('if.png')
        self.runbutton = pygame.image.load('run.png')
        self.obj = []

    def motion(self):
        while not self.close_clicked:  # until player clicks close box play frame
            self.draw()
            self.handle_event()
            if self.continue_game:
                #self.draw()
                if self.run.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and pygame.mouse.get_pressed()[0] == 1:
                    self.run_test()
                    self.continue_game = False
                self.handle_event()
            pygame.display.update()
        pygame.quit()

    def draw(self):
        pygame.draw.rect(self.SCREEN, PINK, (600, 0, 395, 200))
        pygame.draw.rect(self.SCREEN, MINT, (600, 205, 395, 390))
        self.forward = pygame.Rect(620, 20, 150, 50)
        self.SCREEN.blit(self.f, (620, 20))
        self.left = pygame.Rect(620, 80, 150, 50)
        self.SCREEN.blit(self.l, (620, 80))
        self.right = pygame.Rect(620, 140, 150, 50)
        self.SCREEN.blit(self.r, (620, 140))
        self.iff = pygame.Rect(800, 20, 150, 50)
        self.SCREEN.blit(self.i, (800, 20))
        self.run = pygame.Rect(830, 530, 150, 50)
        self.SCREEN.blit(self.runbutton, (830, 530))

        self.obj.sort(key=self.sorted_by_y_axis)
        for item in self.obj:
            self.SCREEN.blit(item[0], (item[1], item[2]))
        pygame.display.update()

    def sorted_by_y_axis(self, obj):
        return obj[2]

    def handle_event(self):
        event = pygame.event.poll()
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            self.close_clicked = True
            self.continue_game = False
        elif event.type == pygame.MOUSEBUTTONDOWN and self.continue_game:
            self.current = None
            if self.forward.collidepoint(pos[0], pos[1]) and pygame.mouse.get_pressed()[0] == 1:
               self.current = self.forward
            elif self.left.collidepoint(pos[0], pos[1]) and pygame.mouse.get_pressed()[0] == 1:
                self.current = self.left
            elif self.right.collidepoint(pos[0], pos[1]) and pygame.mouse.get_pressed()[0] == 1:
                self.current = self.right
            elif self.iff.collidepoint(pos[0], pos[1]) and pygame.mouse.get_pressed()[0] == 1:
                self.current = self.iff
        elif event.type == pygame.MOUSEBUTTONUP and self.continue_game:
            if self.current == self.forward:
                self.obj.append((self.f, pos[0], pos[1]))
            elif self.current == self.left:
                self.obj.append((self.l, pos[0], pos[1]))
            elif self.current == self.right:
                self.obj.append((self.r, pos[0], pos[1]))
            elif self.current == self.iff:
                self.obj.append((self.i, pos[0], pos[1]))
        pygame.display.update()


if __name__ == '__main__':
    sr = stageRight()
    sr.motion()
    clock = pygame.time.Clock()
    cont = True
    run = True
    click_time = 0
