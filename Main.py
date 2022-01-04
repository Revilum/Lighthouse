import time
from pyghthouse import Pyghthouse
import keyboard
import random

# BEGIN define global parameters
p = Pyghthouse("MrSubidubi", "API-TOK_5lLL-mYtC-Iisr-q76Q-YiH+",
               ignore_ssl_cert=True)  # Hier eigene Werte eintragen!
img = Pyghthouse.empty_image()
currentTick = 0
lastTick = 0
swapEnemyDirection = False
gamefield = [[[]]]
outerBoundary = 1
playerX = (len(img[0]) - 1) / 2
playerY = 10
playerSpeed = 0.25
barrierwidth = 4
barrierSpawnRow = len(img) - 6
firstEnemySpawnRow = 1
EnemySpawnChance = 1
barrierHP = 50
gameEntities = {
    "enemy": [["enemy", 1], [0, 255, 255]],
    "barrier": [["barrier", barrierHP], [255, 0, 0]],
    "bedrock": [["bedrock", -1], [0, 255, 255]],
    "none": [["none", 0], [0, 0, 0]],
    "player": [["player", 3, playerX], [255, 0, 0]],
    "projectile": [["projectile", -1, playerX, True], [255, 255, 255]]  # Fourth parameter indicates upward movement
}


# END define global parameters

def init():
    # initialize lighthouse
    Pyghthouse.start(p)
    # TODO possible pregame menu
    # initialize keybinds upon press
    keyboard.on_press_key("a", lambda _: move("left"))
    keyboard.on_press_key("d", lambda _: move("right"))
    keyboard.on_press_key("space", lambda _: shoot())
    # keyboard.on_press_key("escape", lambda _: pause()) - TODO possible pause function


def resetgamefield():
    global gamefield
    # iniializes a gamefield (here based upon dimensions of the image of the lighthouse) with elemets of type "none"
    gamefield = [[gameEntities["none"][0].copy() for j in range(len(img[0]))] for i in range(len(img))]


def initgamefield(barriers):
    global gamefield
    # create new gamefield
    resetgamefield()
    # create barriers for player
    nextbarrier = 0.0
    spaceinbetween = (len(gamefield[0]) - barriers * barrierwidth) / (barriers + 1)
    for barrier in range(barriers):
        nextbarrier += spaceinbetween
        for x in range(barrierwidth):
            for y in range(2):
                if y == 0 and x != 0 and x != barrierwidth - 1 or y == 1:
                    # somewhat hardcoded to barrierwitdth | 2 and larger than 2
                    gamefield[barrierSpawnRow + y][round(nextbarrier) + x + barrier * barrierwidth] = gameEntities[
                        "barrier"][0].copy()
    # Initialize first player position
    gamefield[playerY][round(playerX)] = gameEntities["player"][0]
    spawnenemies(4, 14)


def spawnenemies(rows, enemiesPerRow):
    global gamefield
    # TODO Add Spawn Apart Function
    # spawns "enemiesPerRow" enemies in "rows" rows
    sidespace = round((len(gamefield[0]) - enemiesPerRow) / 2)
    for y in range(rows):
        for x in range(enemiesPerRow):
            if random.random() <= EnemySpawnChance:
                gamefield[firstEnemySpawnRow + y][sidespace + x] = gameEntities["enemy"][0].copy()


def moveenemies():
    global gamefield
    # moves enemies based upon their current position in a snake-light pattern
    # -> direction can always be swapped by changing global boolean "swapEnemyDirection" !
    for y in range(barrierSpawnRow - 1, firstEnemySpawnRow - 1, -1):
        if (y + int(swapEnemyDirection)) % 2 == 0:
            for x in range(outerBoundary, len(gamefield[y]) - outerBoundary):
                if gamefield[y][x] == gameEntities["enemy"][0]:
                    gamefield[y][x] = gameEntities["none"][0].copy()
                    if (y + int(swapEnemyDirection)) % 2 == 0:
                        if x == outerBoundary:
                            gamefield[y + 1][x] = gameEntities["enemy"][0].copy()
                        else:
                            gamefield[y][x - 1] = gameEntities["enemy"][0].copy()
        else:
            for x in range(len(gamefield[y]) - outerBoundary - 1, outerBoundary - 1, -1):
                if gamefield[y][x] == gameEntities["enemy"][0]:
                    gamefield[y][x] = gameEntities["none"][0]
                    if x == len(gamefield[y]) - outerBoundary - 1:
                        gamefield[y + 1][x] = gameEntities["enemy"][0].copy()
                    else:
                        gamefield[y][x + 1] = gameEntities["enemy"][0].copy()


def move(direction):
    # activates once player inputs movement and waits for key-release unless boundaries reached
    # speed is controlled by global variable "playerSpeed"
    while direction == "right" and keyboard.is_pressed("d"):
        if playerX < len(gamefield[0]) - 1 - outerBoundary:
            playerOnGamefield(playerX + playerSpeed)
            time.sleep(0.005)
    while direction == "left" and keyboard.is_pressed("a"):
        if playerX > 0 + outerBoundary:
            playerOnGamefield(playerX - playerSpeed)
            time.sleep(0.005)


def playerOnGamefield(newplayerx):
    global gamefield, playerX
    # moves the player on the gamefield if neccesary and transfers his current position into the gamefield
    currentPos = [i[0] for i in gamefield[playerY]].index(gameEntities["player"][0][0])
    playerX = newplayerx
    if round(playerX) != currentPos:
        gamefield[playerY][currentPos] = gameEntities["none"][0].copy()
    gamefield[playerY][round(playerX)] = gameEntities["player"][0]


def shoot():
    global gamefield
    shotPlacement = round(playerX)
    if gamefield[playerY - 1][shotPlacement] == gameEntities["none"][0]:
        gamefield[playerY - 1][shotPlacement] = gameEntities["projectile"][0].copy()
    else:
        gamefield[playerY - 1][shotPlacement][1] += gameEntities["projectile"][0][1]
        checkIfDead(playerY - 1, shotPlacement)


def shotmovement():
    for ypos, y in enumerate(gamefield):
        for xpos, x in enumerate(y):
            if x[0] == gameEntities["projectile"][0][0]:
                subtract = 1
                if x[3]:
                    subtract = -1
                if gamefield[ypos + subtract][xpos] == gameEntities["none"][0] and 0 < ypos < len(gamefield) - 1:
                    gamefield[ypos + subtract][xpos] = x
                else:
                    gamefield[ypos + subtract][xpos][1] += x[1]
                    checkIfDead(ypos + subtract, xpos)

                gamefield[ypos][xpos] = gameEntities["none"][0].copy()


# TODO This is the block-remove-function without any animation
def checkIfDead(ypos, xpos):
    global gamefield
    if gamefield[ypos][xpos][1] <= 0:
        if gamefield[ypos][xpos][0] == gameEntities["player"][0][0]:
            gameOver()
        else:
            gamefield[ypos][xpos] = gameEntities["none"][0].copy()


# END block-remove

def gameOver():
    print("Game Over!")
    return False


def executeOnTick(tick, executeFunction):
    if currentTick % tick == 0:
        executeFunction()


def gamefieldrender():
    # renders the gamefield based upon the color parameters in the dictionary "gameEntities"
    colorcode = {i[0][0]: i[1] for i in list(gameEntities.values())}
    for ypos, y in enumerate(gamefield):
        for xpos, x in enumerate(y):
            pixeldata = colorcode[x[0]].copy()
            # TODO Fix healtbar display
            if x[0] not in [gameEntities["projectile"][0][0], gameEntities["none"][0][0], gameEntities["player"][0][0]]:
                for count, color in enumerate(pixeldata):
                    pixeldata[count] = round(color * x[1] / gameEntities[x[0]][0][1])
            img[ypos][xpos] = pixeldata
    # sets the image onto the lighthouse once done
    Pyghthouse.set_image(p, img)


def main():
    global currentTick
    # test calls of the functions to check whether they work
    init()
    initgamefield(4)
    gamefieldrender()
    for i in range(10000):
        executeOnTick(30, moveenemies)
        executeOnTick(3, shotmovement)
        gamefieldrender()
        time.sleep(1 / 30)
        currentTick += 1
    Pyghthouse.close(p)


if __name__ == "__main__":
    main()
