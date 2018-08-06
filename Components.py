from pygame import draw

class Ball:
    def __init__(self, spawnCoordinates, screen, speed):
        self.xPos = spawnCoordinates[0]
        self.yPos = spawnCoordinates[1]
        self.dX = -speed
        self.dY = -speed
        self.rad = 6
        self.screen = screen

    def spreadExposure(self, wall, row, col):
        if(not(col-1 < 0)):
            if(wall.brickArr[row][col-1].alive):
                wall.brickArr[row][col-1].exposed = True
        if(not(col+1 > len(wall.brickArr[0])-1)):
            if(wall.brickArr[row][col+1].alive):
                wall.brickArr[row][col+1].exposed = True
        if(not(row-1 < 0)):
            if(wall.brickArr[row-1][col].alive):
                wall.brickArr[row-1][col].exposed = True
        if(not(row+1 > len(wall.brickArr)-1)):
            if(wall.brickArr[row+1][col].alive):
                wall.brickArr[row+1][col].exposed = True

    def detectCollision(self, brick):
        if(self.dX < 0):
            if(self.dY < 0):
                truth1 = False
                truth2 = False
                if(self.xPos - self.rad < brick.xPos + brick.width):
                    if(self.xPos > brick.xPos + brick.width):
                        truth1 = True
                        if(self.yPos < brick.yPos + brick.height and self.yPos > brick.yPos):
                            self.dX *= -1
                            return True
                if(self.yPos - self.rad < brick.yPos + brick.height):
                    if(self.yPos > brick.yPos + brick.height):
                        truth2 = True
                        if(self.xPos < brick.xPos + brick.width and self.xPos > brick.xPos):
                            self.dY *= -1
                            return True
                if(truth1 and truth2):
                    self.dX *= -1
                    self.dY *= -1
                    return True

            else:
                truth1 = False
                truth2 = False
                if(self.xPos - self.rad < brick.xPos + brick.width):
                    if(self.xPos > brick.xPos + brick.width):
                        truth1 = True
                        if(self.yPos < brick.yPos + brick.height and self.yPos > brick.yPos):
                            self.dX *= -1
                            return True
                if(self.yPos + self.rad > brick.yPos and self.yPos < brick.yPos):
                    truth2 = True
                    if(self.xPos < brick.xPos + brick.width and self.xPos > brick.xPos):
                        self.dY *= -1
                        return True
                if(truth1 and truth2):
                    self.dX *= -1
                    self.dY *= -1
                    return True

        else:
            if(self.dY < 0):
                truth1 = False
                truth2 = False
                if(self.xPos < brick.xPos and self.xPos + self.rad > brick.xPos):
                    truth1 = True
                    if(self.yPos < brick.yPos + brick.height and self.yPos > brick.yPos):
                        self.dX *= -1
                        return True
                if(self.yPos - self.rad < brick.yPos + brick.height):
                    if(self.yPos > brick.yPos + brick.height):
                        truth2 = True
                        if(self.xPos < brick.xPos + brick.width and self.xPos > brick.xPos):
                            self.dY *= -1
                            return True
                if(truth1 and truth2):
                    self.dX *= -1
                    self.dY *= -1
                    return True

            else:
                truth1 = False
                truth2 = False
                if(self.xPos < brick.xPos and self.xPos + self.rad > brick.xPos):
                    truth1 = True
                    if(self.yPos < brick.yPos + brick.height and self.yPos > brick.yPos):
                        self.dX *= -1
                        return True
                if(self.yPos + self.rad > brick.yPos and self.yPos < brick.yPos):
                    truth2 = True
                    if(self.xPos < brick.xPos + brick.width and self.xPos > brick.xPos):
                        self.dY *= -1
                        return True
                if(truth1 and truth2):
                    self.dX *= -1
                    self.dY *= -1
                    return True

        return False


    def checkHit(self, wall):
        for i in range(len(wall.brickArr)):
            for j in range(len(wall.brickArr[0])):
                if(wall.brickArr[i][j].alive and wall.brickArr[i][j].exposed):
                    collision = self.detectCollision(wall.brickArr[i][j])
                    if(collision):
                        wall.brickArr[i][j].alive = False
                        wall.bricksLeft -= 1
                        self.spreadExposure(wall, i, j)
                        return True

    def checkStatus(self, paddle, wall):
        hit = self.checkHit(wall)
        if(not hit):
            if((self.xPos - self.rad) <= 0):
                self.dX *= -1
            if((self.yPos - self.rad) <= 0):
                self.dY *= -1
            if((self.xPos + self.rad) >= self.screen.get_size()[0]):
                self.dX *= -1
            if((self.yPos + self.rad) >= self.screen.get_size()[1]):
                if(not(self.xPos > paddle.xPos and self.xPos < paddle.xPos + paddle.width)):
                    self.dY *= -1
                    return False
                else:
                    self.dY *= -1
        else:
            return 10

    def move(self, paddle, wall):
        status = self.checkStatus(paddle, wall)
        if(status == True):
            return True
        elif(status == 10):
            return 10
        self.xPos += self.dX
        self.yPos += self.dY

    def render(self):
        draw.circle(self.screen, (0, 0, 0), (int(self.xPos), int(self.yPos)), self.rad, 0)

class Paddle():
    def __init__(self, screen, paddleWidth, paddleSpeed):
        self.dX = paddleSpeed
        self.height = 9
        self.width = paddleWidth
        self.screen = screen
        self.xPos = int(screen.get_size()[0]/2) - self.width/2
        self.yPos = screen.get_size()[1]-10

    def moveLeft(self):
        if(not self.xPos <= 0):
            self.xPos -= self.dX

    def moveRight(self):
        if(not (self.xPos + self.width) >= self.screen.get_size()[0]):
            self.xPos += self.dX

    def render(self):
        draw.rect(self.screen, (0, 0, 0), (int(self.xPos), int(self.yPos), self.width, self.height), 0)

class Brick():
    def __init__(self, screen, spawnCoordinates, width, height, isExposed):
        self.screen = screen
        self.alive = True
        self.exposed = isExposed
        self.width = width
        self.height = height
        self.xPos = spawnCoordinates[0]
        self.yPos = spawnCoordinates[1]

    def render(self):
        if(self.alive):
            draw.rect(self.screen, (255, 0, 0), (self.xPos, self.yPos, self.width, self.height), 0)

class Wall():
    def __init__(self, screen, dimensions, xPadding, yPadding):
        self.screen = screen
        self.dimensions = dimensions
        self.brickHeight = ((screen.get_size()[1]/2)-yPadding*(dimensions[0]+1))/dimensions[0]
        self.brickWidth = (screen.get_size()[0]-xPadding*(dimensions[1]+1))/dimensions[1]
        self.xPadding = xPadding
        self.yPadding = yPadding
        self.brickArr = self.genBrickArr()
        self.bricksLeft = len(self.brickArr)*len(self.brickArr[0])


    def genBrickArr(self):
        returnArr = []

        i = 0
        xPadCount = 1
        j = 0
        yPadCount = 1

        isExposed = False

        while(i < self.dimensions[0]):
            row = []
            if(i+1 == self.dimensions[0]):
                isExposed = True
            j = 0
            xPadCount = 1
            while(j < self.dimensions[1]):
                row.append(Brick(self.screen, (self.xPadding*xPadCount + j*self.brickWidth, self.yPadding*yPadCount + i*self.brickHeight), self.brickWidth, self.brickHeight, isExposed))
                xPadCount += 1
                j += 1
            returnArr.append(row)
            yPadCount += 1
            i += 1

        return returnArr

    def render(self):
        for i in range(len(self.brickArr)):
            for j in range(len(self.brickArr[0])):
                if(self.brickArr[i][j].alive):
                    self.brickArr[i][j].render()
