import pygame
import os

def load_asset(aAssetName):
    asset_path = os.path.join("assets", aAssetName);
    return pygame.image.load(asset_path)

def load_scene_asset(aSceneId, aAssetName):
    scene_dir = "scene" + str(aSceneId) + "/"
    asset_path = os.path.join("assets", scene_dir, aAssetName);
    return pygame.image.load(asset_path)    

pygame.font.init()
pygame.display.set_caption("DIKTA")
# MAIN_LOGO = load_asset('mainBG.png')
# pygame.display.set_icon(MAIN_LOGO)


class Game:
    def __init__(self):
        self.state = 'main_menu'
        self.width = 800
        self.height = 600
        self.win = pygame.display.set_mode((self.width, self.height))

    def menuOption(self):

        menu = Menu()

        menu.picked_option()

    def main_game(self):
        level = Level()

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.state == 'main_menu':
                    self.menuOption()
                if self.state == 'main_game':
                    self.main_game()

        pygame.quit()


class TaskPanel(Game):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont('bodoniblack', 13)

    def addPanel(self):
        self.rect = pygame.draw.rect(
            self.win, (255, 255, 255), (40, 135, 180, 150))
        pygame.display.update()


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


class Level(Game):
    def __init__(self):

        self.buttons = []
        self.life = 10
        self.level = 1
        self.inited_main_game = False

    def findLevel(self):
        if self.level == 1:
            self.levelOne()

    def levelOne(self, bg):
        self.win.blit(self.bg, (0, 0))

        FIND_ITEMS = []
        TASK_FONT = pygame.font.SysFont('bodoniblack', 13)

        PERSON_SAYING = pygame.transform.scale(
            load_scene_asset(1, 'saying.png'), (461, 93))
        ZOOM = pygame.transform.scale(
            load_scene_asset(1, 'search.png'), (66, 66))
        HAND = pygame.transform.scale(
            load_scene_asset(1, 'hand.png'), (66, 66))
        TASK = pygame.transform.scale(
            load_scene_asset(1, 'task.png'), (106, 113))
        MENU = pygame.transform.scale(
            load_scene_asset(1, 'menu.png'), (107, 35))
        PAPER = pygame.transform.scale(
            load_scene_asset(1, 'paper.png'), (306, 306))
        JOURNAL = pygame.transform.scale(
            load_scene_asset(1, 'journal.png'), (203, 144))
        EYEGLASS = pygame.transform.scale(
            load_scene_asset(1, 'eyeglasses.png'), (140, 140))
        LONG_PAPER = pygame.transform.scale(
            load_scene_asset(1, 'longPaper.png'), (118, 117))

        if not self.inited_main_game:
            PERSON_SAYING_BUTTON = Button(
                PERSON_SAYING, 480, 65, 'personSaying')
            ZOOM_BUTTON = Button(ZOOM, 160, 70, 'Zoom')
            HAND_BUTTON = Button(HAND, 85, 70, 'Hand')
            TASK_BUTTON = Button(TASK, 100, 200, 'Task')
            MENU_BUTTON = Button(MENU, 100, 550, 'Menu')
            PAPER_BUTTON = Button(PAPER, 230, 350, 'Paper')
            JOURNAL_BUTTON = Button(JOURNAL, 630, 220, 'Journal')
            EYEGLASS_BUTTON = Button(EYEGLASS, 700, 120, 'Eye Glass')
            LONG_PAPER_BUTTON = Button(LONG_PAPER, 440, 350, 'Long Paper')
            self.buttons = [PERSON_SAYING_BUTTON, ZOOM_BUTTON,
                            HAND_BUTTON, TASK_BUTTON, MENU_BUTTON,
                            PAPER_BUTTON, JOURNAL_BUTTON, EYEGLASS_BUTTON,
                            LONG_PAPER_BUTTON]
            self.inited_main_game = True

            self.win.blit(SCENE_ONE_BACKGROUND, (0, 0))
            for item in self.buttons:
                self.win.blit(item.image, item.rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btns in self.buttons:
                        btns.checkClick(pos)

            pygame.display.update()


class Menu(Game):
    def __init__(self):
        super().__init__()
        self.options = 'main_menu'

    def picked_option(self):
        if self.options == 'main_menu':
            self.main_menu()

        if self.options == 'help':

            print('Help Here soon')

    def main_menu(self):

        WHITE = (255, 255, 255)
        START_GAME_FONT = pygame.font.SysFont('bodoniblack', 13)
        LANDING_NEW_GAME_TEXT = START_GAME_FONT.render(
            "PRESS X FOR NEW GAME", 1, WHITE)

        MENU_BACKGROUND = load_asset('mainBG.png')
        MAIN_LOGO = pygame.transform.scale(load_asset('logoName.png'), (300, 80))

        self.win.blit(MENU_BACKGROUND, (0, 0))
        self.win.blit(MAIN_LOGO, (70, 80))
        self.win.blit(LANDING_NEW_GAME_TEXT, (500, 110))
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                print('stage 2')
                if event.key == pygame.K_x:
                    self.state = 'main_game'
        pygame.display.update()

    def help(self):
        print('Help Here Soon')


SCENE_ONE_BACKGROUND = load_scene_asset(1, 'bg.png')


def lvlOne():
    level_one = Level(SCENE_ONE_BACKGROUND)


game = Game()
game.run()
