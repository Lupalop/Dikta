# pygbag: name=dikta, width=1360, height=765
import asyncio
import pygame
import pygame.freetype
import engine
import app

async def main():
    await engine.game.run()

if __name__ == "__main__":
    asyncio.run(main())
