import pygame, sys
import gameSetting
from pyfiles.Button import Button

class MainMenu:
    IMAGE_PATH = "images/"
    # no args needed
    def __init__(self, window, args):
        self.window = window
        self.loadImage()


    def mainloop(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # draw on screen
            self.window.blit(self.bg_img, (0, 0))
            self.start_button.displayUpdate()
            if (self.start_button.OnMouseUp()):
                return "choose level", None # page name to be opened next and args to be passed to

            pygame.display.update()
            clock.tick(gameSetting.FPS)


    def loadImage(self):
        self.bg_img = pygame.image.load(self.IMAGE_PATH + "mainpage_bg.png")
        button_img = self.IMAGE_PATH + "start_button.png"
        button_hover_img = self.IMAGE_PATH + "start_button_hover.png"
        button_pos = (350, 320)
        self.start_button = Button(self.window, button_img, button_pos, onHover=button_hover_img, onClick="smaller")