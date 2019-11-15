import pygame, sys

from pyfiles.Stage import Stage as TestPage

def main():
    # setup args here:
    args = 1

    window = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Rescoding Page Tester")

    page = TestPage(window, args)
    pygame.init()
    nextPage, nextArgs = page.mainloop()

    print("\nValues returned:")
    print("nextPage =", nextPage)
    print("nextArgs =", nextArgs)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()