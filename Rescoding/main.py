"""
Last updated
on Nov.14.2019
by Dulong Sang
version: 0.1.1
"""

import pygame, sys
import gameSetting

# import module here:
from pyfiles.MainMenu import MainMenu
from pyfiles.ChooseLevel import ChooseLevel


def main():

    # setting up pygame window
    window = pygame.display.set_mode(gameSetting.WINDOW_SIZE)
    pygame.display.set_caption("Rescoding")
    
    nextPage = "main menu"  # first page
    args = None
    
    pageClass = {"main menu": MainMenu, "choose level": ChooseLevel}

    pygame.init()
    while True:
        currentPage = pageClass[nextPage](window, args)
        nextPage, args = currentPage.mainloop()

        if nextPage not in pageClass:
            print("\nInvalid page name:", nextPage)
            print("Program shutdown.")
            pygame.quit()
            sys.exit()
    


if __name__ == "__main__":
    main()