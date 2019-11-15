import pygame, sys, gameSetting
from pyfiles.Button import Button

class ChooseLevel:

    IMAGE_PATH = "images/"
    # no args needed
    def __init__(self, window, args):
        self.window = window
        self.number_of_levels = 6
        self.loadImage()
        

    def mainloop(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # draw on screen
            self.window.blit(self.bg_img, (0,0))
            for i in range(self.number_of_levels):
                button = self.buttonList[i]
                button.displayUpdate()
                if (button.OnMouseUp()):
                    return "stage", (i+1)  # page name to be opened next and args to be passed to
            self.back_button.displayUpdate()
            if (self.back_button.OnMouseUp()):
                return "main menu", None

            pygame.display.update()
            clock.tick(gameSetting.FPS)

    
    def loadImage(self):
        bg_img_path = self.IMAGE_PATH + "chooseLevel_bg.png"
        self.bg_img = pygame.image.load(bg_img_path)

        self.buttonList = []
        size = (75, 75)
        buttonPositions = [(60, 75), (90, 300), (250, 510), (380, 320), (635,350), (780,490)]
        for i in range(self.number_of_levels):
            img_path = self.IMAGE_PATH + "stageButtons/stage_button%d.png"%(i+1)
            button = Button(self.window, img_path, buttonPositions[i], scale=size, onClick="smaller")
            self.buttonList.append(button)

        back_button_imgPath = self.IMAGE_PATH + "back_button.png"
        self.back_button = Button(self.window, back_button_imgPath, (930,30), scale=(50, 50), onClick="smaller")
