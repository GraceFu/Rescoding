import pygame, sys, gameSetting

class PageTemp:

    """
    @ param window: (pygame.Surface) main window
    @ param args: (list) all arguments needed (should be specified here)
    """
    def __init__(self, window, args):
        self.window = window
        pass
    

    def mainloop(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if (True): # some condition
                return "page name", [] # page name to be opened next and args to be passed to

            pygame.display.update()
            clock.tick(gameSetting.FPS)
