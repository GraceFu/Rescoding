import pygame

class CommandBox:

    def __init__(self, imagePath, command, scale=None):
        self.img = pygame.image.load(imagePath)
        if (scale != None):
            self.img = pygame.transform.scale(self.img, scale)
        self.size = self.img.get_size()
        self.pos = None
        self.region = None
        self.command = command


    def displayUpdate(self, window, dragging=False):
        if (dragging):
            mouse_pos = pygame.mouse.get_pos()
            self.pos = (mouse_pos[0] - (self.size[0] // 2), mouse_pos[1] - (self.size[1] // 2))
            self.region = (self.pos[0], self.pos[0] + self.size[0], self.pos[1], self.pos[1] + self.size[1])
        window.blit(self.img, self.pos)
        

    def setPosition(self, position):
        self.pos = position


    # return: tuple of two int, [0] for left key, [1] for right key
    def isClicked(self):
        ret = [False, False]
        mouse_pos = pygame.mouse.get_pos()
        if (mouse_pos[0] < self.region[0] or mouse_pos[0] > self.region[1] or
            mouse_pos[1] < self.region[2] or mouse_pos[1] > self.region[3]):
            return (tuple)(ret)
        
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]: # if left key is pressed
            ret[0] = True
        if mouse_pressed[2]:
            ret[1] = True
        return (tuple)(ret)

    
    def getCommand(self):
        return self.command