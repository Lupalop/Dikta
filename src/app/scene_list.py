from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.scene import Scene
    from app.mission import Mission

all: dict[str, "Scene"] = {}

def add_mission(mission: "Mission") -> None:
    all[mission.mission_key] = mission
