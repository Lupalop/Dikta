from .mouse import MouseOverlay
from .debug import DebugOverlay
from .main_menu import MainMenuScene

from .e0mtest import E0MTestScene
from .e1m0 import E1M0Scene
from .e1m1 import E1M1Scene
from .e1m2 import E1M2Scene
from .e1m3 import E1M3Scene
from .e1m4 import E1M4Scene
from .e1m5 import E1M5Scene
from .e1m6 import E1M6Scene
from .e1m7 import E1M7Scene
from .e1m8 import E1M8Scene
from .e1m9 import E1M9Scene

scene_list = {
    "mouse": MouseOverlay(),
    "debug": DebugOverlay(),
    "main_menu": MainMenuScene(),
    "test": E0MTestScene(),
    "e1m0": E1M0Scene(),
    "e1m1": E1M1Scene(),
    "e1m2": E1M2Scene(),
    "e1m3": E1M3Scene(),
    "e1m4": E1M4Scene(),
    "e1m5": E1M5Scene(),
    "e1m6": E1M6Scene(),
    "e1m7": E1M7Scene(),
    "e1m8": E1M8Scene(),
    "e1m9": E1M9Scene(),
}
