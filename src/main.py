import pygame
import os
pygame.font.init()

def load_asset(aAssetName):
    asset_path = os.path.join("assets", aAssetName);
    return pygame.image.load(asset_path)

def load_scene_asset(aSceneId, aAssetName):
    scene_dir = "scene" + str(aSceneId) + "/"
    asset_path = os.path.join("assets", scene_dir, aAssetName);
    return pygame.image.load(asset_path)    

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

MAIN_LOGO = load_asset('mainBG.png')

WIN_MAIN_BACKGROUND = load_asset('mainBG.png')

MAIN_LOGO_NAME = pygame.transform.scale(load_asset('logoName.png'), (300, 80))

WHITE = (255, 255, 255)

MAIN_DIKTA_FONT = pygame.font.SysFont('garamond', 100)
START_GAME_FONT = pygame.font.SysFont('bodoniblack', 13)

LANDING_MAIN_TEXT = MAIN_DIKTA_FONT.render("DIKTA", 1, WHITE)
LANDING_NEW_GAME_TEXT = START_GAME_FONT.render(
    "PRESS X FOR NEW GAME", 1, WHITE)


pygame.display.set_caption("Dikta")
pygame.display.set_icon(MAIN_LOGO)


def make_window():

    WIN.blit(WIN_MAIN_BACKGROUND, (0, 0))
    WIN.blit(MAIN_LOGO_NAME, (70, 80))
    WIN.blit(LANDING_NEW_GAME_TEXT, (500, 110))
    pygame.display.update()


class Button():
    def __init__(self, image, pos_x, pos_y):
        self.image = image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    def update(self):
        WIN.blit(self.image, self.rect)

    def checkPosition(self, position):
        print(position)

    def removeImg(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            print('Will Remove this item')


def start_game():
    btn_try = load_scene_asset(1, 'hand.png')
    btn_try2 = pygame.transform.scale(btn_try, (66, 66))

    hand_button = Button(btn_try2, 160, 75)

    # HAND_BTN = Button(HAND_INIT, 120, 40)

    SCENE_ONE_BG = pygame.transform.scale(
        load_scene_asset(1, 'bg.png'), (800, 600))

    PERSON_SAYING = pygame.transform.scale(
        load_scene_asset(1, 'saying.png'), (461, 93))
    # HAND = pygame.transform.scale(pygame.image.load(
    #     os.path.join('ASSETS', 'hand.png'), (66, 66))
    ZOOM = pygame.transform.scale(
        load_scene_asset(1, 'search.png'), (66, 66))
    TASK = pygame.transform.scale(
        load_scene_asset(1, 'task.png'), (106, 113))
    MENU = pygame.transform.scale(
        load_scene_asset(1, 'menu.png'), (107, 35))
    BOOK = pygame.transform.scale(
        load_scene_asset(1, 'paper.png'), (306, 306))
    JOURNAL = pygame.transform.scale(
        load_scene_asset(1, 'journal.png'), (203, 144))
    EYEGLASS = pygame.transform.scale(
        load_scene_asset(1, 'eyeglasses.png'), (140, 140))
    LONG_PAPER = pygame.transform.scale(
        load_scene_asset(1, 'longPaper.png'), (118, 117))

    WIN.blit(SCENE_ONE_BG, (0, 0))
    WIN.blit(PERSON_SAYING, (250, 20))
    WIN.blit(ZOOM, (40, 40))
    # WIN.blit(HAND_BTN, (HAND_BTN.pos_x, HAND_BTN.pos_y))
    WIN.blit(TASK, (40, 135))
    WIN.blit(MENU, (40, 550))
    WIN.blit(BOOK, (70, 220))
    WIN.blit(JOURNAL, (570, 140))
    WIN.blit(EYEGLASS, (660, 50))
    WIN.blit(LONG_PAPER, (370, 300))
    hand_button.update()

    hand_button.checkPosition(pygame.mouse.get_pos())
    pygame.display.update()


def main():
    running = True
    make_window()
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    start_game()

    pygame.quit()


if __name__ == '__main__':
    main()
