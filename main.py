# Note: press F3 For debugger output.

import builtins
import json
import os
import random
import sys
import textwrap

import pygame

from timer import timer
from typedef import Coordinate

pygame.font.init()


toggleDebug = False
mode = "intro"
introTicks = 120
args = sys.argv
ignoreNext = False
for iarg in range(len(args)):
    if not ignoreNext:
        if args[iarg] in ("-d","--debug"):
            toggleDebug = True                 # Open the debugger on launch.
        elif args[iarg] in ("-m", "--mode"):
            try:
                mode = args[iarg+1]            # Overwrite the mode on launch.
                ignoreNext = True
            except:
                print("Missing parameter for '--mode'/'-m'")
        elif args[iarg] in ("-t", "--introTicks"):
            introTicks = args[iarg+1] | 120
            ignoreNext = True
        else:
            print(f"Unknown Argument: {args[iarg]}")



class TextLogger:
    def __init__(self, limit: int = 65535):
        """Creates a new textLogger Object with a limit of `limit` lines.
        limit: int = 65535
            How many lines should be added before the oldest lines are cleared. Default is 65535 lines.
        """
        self.limit = 65535
        self.text = []
    def add(self, *args: list[str]):
        argsFormatted = []
        for i in args:
            for j in i.split("&n"):
                argsFormatted.append(j)
        for i in argsFormatted:
            wrapped = textwrap.wrap(i, 60)  # Wrap after 62 chars
            for j in range(len(wrapped)):
                if j != 0:
                    self.text.append("└>"+wrapped[j])
                elif j == 0 and len(wrapped) > 1:
                    self.text.append(wrapped[j])
                else:
                    self.text.append(wrapped[j])

debugLogger = TextLogger()
def _print(*args, **kwargs):
    builtins.print(*args, **kwargs)
def print(*args: list[str]):
    for arg in args:
        debugLogger.add(arg)
def error(error: Exception | str):
    if isinstance(error, Exception):
        debugLogger.add(f"Exception: {error.__class__.__name__}.{error.__traceback__.tb_lineno}: {error}")
    else:
        debugLogger.add(f"Exception: {error}")
    

print("Start Of Debugger")


try:
    with open("settings.json", "r") as f:
        settings = json.load(f)
        print("Loaded settings.")
except Exception as e:
    error(e)
    print(f"Using default settings...")
    settings = {
        "resolution":[0,0],
        "framerate":60
    }

try:
    FRAMERATE = settings["framerate"]
except Exception as e:
    error(e)
    print(f" ^^^^ Will use default framerate.")
    FRAMERATE = 60

try:
    RESOLUTION = (settings["resolution"][0],settings["resolution"][1])
except Exception as e:
    error(e)
    print(f" ^^^^ Will use default resolution.")
    RESOLUTION = (0, 0)

display = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Game")
clock = pygame.time.Clock()



debugPanel = pygame.Surface((500,400))
debugPanel.set_alpha(175)
debugPanelScroll = len(debugLogger.text)
debugFont = pygame.font.SysFont("Courier", 14)
# toggleDebug = False  # Referenced in the "argv" statement at the top.
toggleDebugKeyCooldown = False
prevDebugMax = len(debugLogger.text)


# mode = "intro"  # Referenced in the "argv" statement at the top.
introTimer = None
while 1:
    DELTATIME = clock.tick(FRAMERATE)

    display.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEWHEEL:
            _mousepos = pygame.mouse.get_pos()
            if debugPanel.get_rect().collidepoint(_mousepos):
                _npos = debugPanelScroll + event.y
                if _npos >= 0 and _npos <= len(debugLogger.text):
                    debugPanelScroll += event.y



    if mode == "intro":    
        if introTimer is None:
            introTimer = timer(introTicks)
        elif isinstance(introTimer, timer):
            if introTimer.check():
                mode = "menu"
            else:
                display.blit(debugFont.render(f"Sample Intro Screen. Frame {introTimer.thisFrame}/{introTicks})", 1, (0,0,0)), (20,20))
                introTimer.tick()
        else:
            error(f"introTimer type not recognized: {introTimer}")
            mode = "menu"
    elif mode == "menu":
        display.blit(debugFont.render("Main Menu Screen", 1, (0,0,0)), (100,100))
    else:
        error(f"Unknown Game Mode: {mode}. Defaulting to 'intro'")
        mode = "intro"



    if pygame.key.get_pressed()[pygame.K_F3]:
        if not toggleDebugKeyCooldown:
            toggleDebugKeyCooldown = True
            toggleDebug = not toggleDebug
            if toggleDebug:
                print("Opened Debug Panel")
            else:
                print("Closed Debug Panel")
    else:
        toggleDebugKeyCooldown = False
    if debugPanelScroll == prevDebugMax:
        debugPanelScroll = len(debugLogger.text)
    if toggleDebug == True:
        debugPanel.fill((100,100,100))

        try:
            indxmin = (debugPanelScroll-25 if debugPanelScroll-25 > 0 else 0)
            indxmax = debugPanelScroll+1
            textToRender = debugLogger.text[indxmin:indxmax]
        except IndexError:
            _print("Failed to load debugger output.")
            textToRender = ["Failed to load Debugger Output."]
        textToRender.reverse()
        for i in range(len(textToRender)):
            rendered = debugFont.render(str(textToRender[i]),1,(0,0,0))
            debugPanel.blit(
                rendered,
                (
                    2,
                    (400-i*16-16)
                )
            )
        display.blit(debugPanel, (0,0))
    

    prevDebugMax = len(debugLogger.text)
    pygame.display.flip()
    