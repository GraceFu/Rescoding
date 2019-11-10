import pygame

class Stagebutton:
    
    def __init__(self, window, num, pos):
        
        self.num = num
        self.size = (75,75)
        self.pos = pos
        self.button_img = pygame.image.load('image/stages/stage' + str(num) +'.png')
        window.screen.blit(pygame.transform.scale(self.button_img, self.size), self.pos)
        self.button_hb = pygame.Rect(self.pos[0]+5, self.pos[1]+5, 65, 65)
        
        # mouse initialization
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_hb = pygame.Rect(self.mouse_pos[0], self.mouse_pos[1], 15, 15)        
        
    def click(self):
        return (pygame.mouse.get_pressed()[0] == 1 and self.mouse_hb.colliderect(self.button_hb))
        