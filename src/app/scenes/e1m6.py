from engine import *
from app import defaults, scene_list, utils
from app.entities import *
from app.mission import Mission
from app.dialog import DialogSide, DialogFlags

import pygame

light = utils.load_ui_image("spotlight")

class E1M6Scene(Mission):
    def __init__(self):
        super().__init__(1, 6, "", "Police Brutality", DialogSide.TOP)

    def update(self, game, events):
        super().update(game, events)

    def draw(self, layer):
        if self.exists_clue("flashlight"):
            if self.background:
                self.background.draw(layer)

            for entityName in self.entities:
                entity = self.entities[entityName]
                if entity.hidden:
                    continue
                entity.draw(layer)

            filter = pygame.surface.Surface((1360, 765))
            filter.fill(pygame.color.Color("white"))
            pos = game.get_mouse_pos()
            filter.blit(light, (pos[0] - (light.get_rect().width / 2), pos[1] - (light.get_rect().height / 2)))
            layer.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

            self.emitter.draw(layer)
        else:
            self.emitter.draw(layer)

    def load_content(self):
        super().load_content()
        self.background.set_surface(self.get_image("main-bg"))
        self.emitter.add("joe", "intro", "joe-faceright")

        def _cop2_talk(sender):
            self.emitter.add("cop2", "end", "cop2-talk1")
            self.emitter.add("joe", "end", "joe-faceright", callback = lambda:game.scenes.set_scene("e1m7joe"))

        if not self.exists_clue("flashlight"):
            _cop2_talk(None)

        target_jeep = TargetItem(
            self,
            self.get_image("prop-jeep"),
            (70, 145),
            removable = False,
            grabbable = False
        )
        target_jeep.leftclick += lambda sender: \
            self.emitter.add("joe", "target_jeep", "joe-faceright")

        target_cop1 = TargetItem(
            self,
            self.get_image("prop-mac"),
            (1062, 171),
            removable = False,
            grabbable = False
        )
        def _cop1_talk(sender):
            self.emitter.add("joe", "target_riot_talk1", "joe-faceright")
            self.emitter.add("joe", "target_riot_talk2", "joe-faceright")

        target_cop1.leftclick += _cop1_talk

        target_cop2 = TargetItem(
            self,
            self.get_image("prop-cop2"),
            (185, 230),
            removable = False,
            grabbable = False
        )
        target_cop2.leftclick += _cop2_talk

        target_demonstrator = TargetItem(
            self,
            self.get_image("prop-berto"),
            (532, 545),
            removable = False,
            grabbable = False
        )
        def _demonstrator_talk(sender):
            self.emitter.add("joe", "target_demonstrator_talk1", "joe-faceright")
            self.emitter.add("joe", "target_demonstrator_talk2", "joe-faceright")
        target_demonstrator.leftclick += _demonstrator_talk

        self.entities = {
            "target_jeep": target_jeep,
            "target_cop1": target_cop1,
            "target_cop2": target_cop2,
            "target_demonstrator": target_demonstrator
        }

scene_list.add_mission(E1M6Scene())
