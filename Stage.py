import pygame


class WindowPage:
    def __init__(self,color=None):
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("game")
        self.screen.fill(pygame.Color('white'))



if __name__ == '__main__':
    WindowPage()
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False




class Stage:

    def __init__(filename):

        self.file = filename
        self.gameMap = Map(self.file)
        self.map_size = self.gameMap.size
        self.env = self.gameMap.env
        self.ch_pos = self.gameMap.ch_position
        self.ch_direction = self.gameMap.ch_direction
        self.hit = False
        self.win = False

    
    def move(movement):
        if movement[0] == "f":
            step_num = int(movement[1:])
            while self.hit == False and step_num > 0:
                next_pos = self.ch_pos
                if self.ch_direction == 'l':
                    next_pos[0] -= 1
                elif self.ch_direction == 'r':
                    next_pos[0] += 1
                elif self.ch_direction == 'u':
                    next_pos[1] -= 1
                else:
                    next_pos[1] += 1
                    
                if not validMove(next_pos):
                    self.hit = True
                else:
                    self.ch_pos = next_pos
                    
                
                
    def validMove(pos):
        if pos[0] < 0 or pos[0] >= self.map_size[0] or pos[1] < 0 or pos[1] >= self.map_size[1]:
            return False
        elif self.env[pos[0]][pos[1]] == 2 or self.env[pos[0]][pos[1]] == 3 or self.env[pos[0]][pos[1]] == 4:
            return False
        else:
            return True

