import pygame, time

class Button:
    """
    constructor parameters: 
        window: (pygame.Surface)
        imgPath: (str) image file path, e.g. "images/start_button.png"
        position: (tuple), two int, the top-left corner
        [opt] scale: (tuple of two int or float) default value = None (keeps the original scale)
        [opt] onHover: (str) image file path when button is on hover
        [opt] onClick: (str) image file path when button is on click, specific value: "smaller"

    methods:
        self.isClicked()     -> return True if user is clicking on this button, False otherwise
        self.OnMouseUp()     -> return True if user has released the mouse button, False otherwise
        self.displayUpdate() -> call it every frame

    NOTE: self.OnMouseUp() is disabled if onClick==None
    """

    POP_UP_DELAY = 0.1 # sec

    def __init__(self, window, imgPath, position, scale=None, onHover=None, onClick=None):
        self.window = window
        self.img = pygame.image.load(imgPath)
        self.position = position
        self.size = self.img.get_size()
        if (scale != None):
            if (type(scale) == float):
                self.size = ((int)(self.size[0]*scale), (int)(self.size[1]*scale))
                self.img = pygame.transform.scale(self.img, self.size)
            elif (type(scale) == tuple):
                self.img = pygame.transform.scale(self.img, scale)
                self.size = self.img.get_size()

        if (onHover != None):
            self.onHover_img = pygame.image.load(onHover)
        else:
            self.onHover_img = None

        if (onClick != None):
            if (onClick == "smaller"):
                self.onClick_img = "smaller"
            else:
                self.onClick_img = pygame.image.load(onClick)
        else:
            self.onClick_img = None

        # (x_min, x_max, y_min, y_max)
        self.region = ( position[0], position[0] + self.size[0], position[1], position[1] + self.size[1])
        self.click = False
        self.popUpTimer = None
        self.isMouseUp = False
        
    
    def isClicked(self):
        if not pygame.mouse.get_pressed()[0]: # if left key is not pressed
            return False
        return self.isOnHover()


    def OnMouseUp(self):
        if not self.isMouseUp:
            return False
        self.isMouseUp = False
        return True
        

    def isOnHover(self):
        mouse_pos = pygame.mouse.get_pos()
        # if mouse position is inside the button
        if (mouse_pos[0] >= self.region[0] and mouse_pos[0] <= self.region[1] and 
            mouse_pos[1] >= self.region[2] and mouse_pos[1] <= self.region[3]):
            return True
        return False

    
    def displayUpdate(self):
        if (self.onClick_img != None):
            if not self.click:
                self.click = self.isClicked()
            else:
                if (not pygame.mouse.get_pressed()[0]):
                    if (self.popUpTimer == None):
                        self.popUpTimer = time.time()
                    else:
                        if (time.time() - self.popUpTimer) > 0.15:
                            self.click = False
                            self.popUpTimer = None
                            self.isMouseUp = True

        displayImg = self.img
        position = self.position
        if (self.isOnHover()):
            if (pygame.mouse.get_pressed()[0]): # user clicked the button
                if (self.onClick_img != None):
                    if (self.onClick_img == "smaller"):
                        scale = ((int)(self.size[0]*0.9), (int)(self.size[1]*0.9))
                        position = ((int)(self.position[0] + self.size[0] * 0.05), 
                                    (int)(self.position[1] + self.size[1] * 0.05))
                        if (self.onHover_img != None):
                            displayImg = pygame.transform.scale(self.onHover_img, scale)
                        else:
                            displayImg = pygame.transform.scale(self.img, scale)
                    else:
                        displayImg = self.onClick_img
            else: # user's mouse is hovering on the button
                if (self.onHover_img != None):
                    displayImg = self.onHover_img
        self.window.blit(displayImg, position)
