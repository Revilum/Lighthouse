import time
from pyghthouse import Pyghthouse
import keyboard
import random

# BEGIN define global parameters
p = Pyghthouse("MrSubidubi", "API-TOK_pZhT-JIeS-OPhx-hYIk-lnPe",
               ignore_ssl_cert=True)  # Hier eigene Werte eintragen!
img = Pyghthouse.empty_image()
currentTick = 0
swapEnemyDirection = False
gamefield = [[[]]]
outerBoundary = 1
playerX = (len(img[0]) - 1) / 2
barrierwidth = 4
barrierSpawnRow = len(img) - 6
firstEnemySpawnRow = 1
maxEnemiesPerRow = 12  # less than 14
EnemySpawnChance = 1
barrierHP = 50
gameEntities = {
    "enemy": [(1, 1), [0, 255, 255]],
    "barrier": [(10, barrierHP), [255, 0, 0]],
    "bedrock": [(99, -1), [0, 255, 255]],
    "none": [(0, 0), [0, 0, 0]]
}


# END define global parameters

def init():
    Pyghthouse.start(p)
    # TODO possible pregame menu
    # keyboard.on_press_key("a", lambda _: move(keyoptions("left")))
    # keyboard.on_press_key("d", lambda _: move("right"))
    # keyboard.on_press_key("space", lambda _: shoot())
    # keyboard.on_press_key("escape", lambda _: pause()) - TODO possible pause function


def resetgamefield():
    global gamefield
    gamefield = [[gameEntities["none"][0] for j in range(len(img[0]))] for i in range(len(img))]


def initgamefield(barriers):
    global gamefield
    resetgamefield()
    nextbarrier = 0.0
    spaceinbetween = (len(gamefield[0]) - barriers * barrierwidth) / (barriers + 1)
    for barrier in range(barriers):
        nextbarrier += spaceinbetween
        for x in range(barrierwidth):
            for y in range(2):
                if y == 0 and x != 0 and x != barrierwidth - 1 or y == 1:
                    # somewhat hardcoded to barrierwitdth | 2 and larger than 2
                    gamefield[barrierSpawnRow + y][round(nextbarrier) + x + barrier * barrierwidth] = gameEntities[
                        "barrier"][0]
    spawnenemies(4)


def spawnenemies(rows):
    global gamefield
    sidespace = round(len(gamefield[0]) / 2 - maxEnemiesPerRow)
    for y in range(rows):
        for x in range(maxEnemiesPerRow):
            if random.random() <= EnemySpawnChance:
                gamefield[firstEnemySpawnRow + y][sidespace + x * 2] = gameEntities["enemy"][0]


def moveenemies():
    global gamefield
    for y in range(barrierSpawnRow - 1, firstEnemySpawnRow - 1, -1):
        if (y + int(swapEnemyDirection)) % 2 == 0:
            for x in range(outerBoundary, len(gamefield[y]) - outerBoundary):
                if gamefield[y][x] == gameEntities["enemy"][0]:
                    gamefield[y][x] = gameEntities["none"][0]
                    if (y + int(swapEnemyDirection)) % 2 == 0:
                        if x == outerBoundary:
                            gamefield[y + 1][x] = gameEntities["enemy"][0]
                        else:
                            gamefield[y][x - 1] = gameEntities["enemy"][0]
        else:
            for x in range(len(gamefield[y]) - outerBoundary - 1, outerBoundary - 1, -1):
                if gamefield[y][x] == gameEntities["enemy"][0]:
                    gamefield[y][x] = gameEntities["none"][0]
                    if x == len(gamefield[y]) - outerBoundary - 1:
                        gamefield[y + 1][x] = gameEntities["enemy"][0]
                    else:
                        gamefield[y][x + 1] = gameEntities["enemy"][0]


def keyoptions(option):
    definedInputs = {"left": 1, "right": 2}
    return definedInputs.get(option, "Undefined!")


def move(direction):
    print(direction)
    return


def shoot():
    return


def gamefieldrender():
    colorcode = {i[0]: i[1] for i in list(gameEntities.values())}
    for ypos, y in enumerate(gamefield):
        for xpos, x in enumerate(y):
            img[ypos][xpos] = colorcode[tuple(x)]
    Pyghthouse.set_image(p, img)


def main():
    init()
    initgamefield(4)
    gamefieldrender()
    time.sleep(5)
    for i in range(10):
        moveenemies()
        gamefieldrender()
        time.sleep(1)
    Pyghthouse.close(p)


if __name__ == "__main__":
    main()
