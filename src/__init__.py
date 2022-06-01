# MaquinaPy Game Runner

# The following suppresses the PyGame message emitted in the console
# on startup.
from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

# Initialize engine and app packages.
import engine
import app
