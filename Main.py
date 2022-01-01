import time
from pyghthouse import Pyghthouse
import keyboard
import random

# BEGIN define global parameters
p = Pyghthouse("MrSubidubi", "API-TOK_pZhT-JIeS-OPhx-hYIk-lnPe",
               ignore_ssl_cert=True)  # Hier eigene Werte eintragen!
img = Pyghthouse.empty_image()
gamefield = [[[]]]
playerX = (len(img[0]) - 1) / 2
barrierwidth = 4
barrierplacement = len(img) - 6
firstEnemySpawnRow = 1
maxEnemiesPerRow = 12  # less than 14
EnemySpawnChance = 0.95
barrierHP = 50


# END define global parameters

def init():
    Pyghthouse.start(p)
    # TODO possible pregame menu
    # keyboard.on_press_key("a", lambda _: move(keyoptions("left")))
    # keyboard.on_press_key("d", lambda _: move("right"))
    # keyboard.on_press_key("space", lambda _: shoot())
    # keyboard.on_press_key("escape", lambda _: pause()) - TODO possible pause function


def gamefielddata(input, *barriernumber):
    handednumber = 0
    if len(barriernumber) != 0:
        handednumber = barriernumber[0]
    possibilities = {
        "enemy": [1, 1],
        "barrier": [10 + handednumber, barrierHP]
    }
    return possibilities.get(input, [0, 0])


def resetgamefield():
    global gamefield
    gamefield = [[gamefielddata("none") for j in range(len(img[0]))] for i in range(len(img))]


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
                    gamefield[barrierplacement + y][round(nextbarrier) + x + barrier * barrierwidth] = gamefielddata(
                        "barrier", barrier)
    placeenemies(4)


def placeenemies(rows):
    global gamefield
    sidespace = len(gamefield[0]) - maxEnemiesPerRow * 2
    for y in range(rows):
        for x in range(maxEnemiesPerRow):
            if random.random() < EnemySpawnChance:
                gamefield[firstEnemySpawnRow + y][sidespace + x * 2] = gamefielddata("enemy")


def keyoptions(option):
    definedInputs = {"left": 1, "right": 2}
    return definedInputs.get(option, "Undefined!")


def move(direction):
    print(direction)
    return


def shoot():
    return


def main():
    init()
    initgamefield(4)
    for i in gamefield:
        print(i)
    Pyghthouse.close(p)


if __name__ == "__main__":
    main()
