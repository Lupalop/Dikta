import pygame


class Button(Game):
    def __init__(self, image, pos_x, pos_y, name):
        self.image = image
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.updateRect()

    def updateRect(self):
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    def checkClick(self, pos):
        self.pos = pos

        if self.rect.collidepoint(self.pos):

            self.pos_x = -500
            self.pos_y = -500
            self.updateRect()
            pygame.display.update()
