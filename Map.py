import json


"""
@attributes:
    self.size: list of two int, e.g. (5, 5)
    self.ch_position: list of two int, e.g. [3, 2]
    self.ch_direction: string of 1 char, l -> left, r -> right, u -> up, d -> down
    self.env: 2d-list of int, int representation:
        0 -> None
        1 -> animal
        2 -> walls
        3 -> wolves
        4 -> rivers
    self.command_list: list of string, values:
        "forward", "turn left", "turn right"
"""
class Map:
    
    def __init__(self, filename):
        self.env = []
        self.readfile(filename)
        
    
    def readfile(self, filename):
        with open(filename) as file:
            data = json.load(file)
            self.size = tuple(data["size"])
            self.ch_position = data["grace_position"]
            self.ch_direction = data["grace_direction"]
            animal = data["animal"]
            walls = data["walls"]
            rivers = data["rivers"]
            wolves = data["wolves"]
            self.command_list = data["command_list"]
        
        # init all entry in self.env to 0
        for i in range(self.size[0]):
            temp = []
            for j in range(self.size[1]):
                temp.append(0)
            self.env.append(temp)
        
        self.env[animal[0]][animal[1]] = 1
        
        for wall in walls:
            self.env[wall[0]][wall[1]] = 2
        
        for wolf in wolves:
            self.env[wolf[0]][wolf[1]] = 3

        for river in rivers:
            self.env[river[0]][river[1]] = 4
