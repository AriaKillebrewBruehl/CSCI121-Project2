# File: DrawHexagon.py

"""
This program draws a hexagon at the center of the window.
"""

from pgl import GWindow, GPolygon

# Constants 

GWINDOW_WIDTH = 500
GWINDOW_HEIGHT = 200
HEXAGON_SIDE = 50

def DrawHexagon():
    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    hexagon = createHexagon(HEXAGON_SIDE)
    gw.add(hexagon, gw.getWidth() / 2, gw.getHeight() / 2)

def createHexagon(side):
    """
    Creates a GCompound representing a regular hexagon with the specified
    side length.  The reference point is the center.
    """
    hex = GPolygon()
    hex.addVertex(-side, 0)
    angle = 60
    for i in range(6):
        hex.addPolarEdge(side, angle)
        angle -= 60
    return hex

# Startup code

if __name__ == "__main__":
    DrawHexagon()
