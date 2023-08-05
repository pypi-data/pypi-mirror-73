import pygame as pg
import math


class Pgp(object):
    def __init__(self, surface, width, height, topleft=None, topright=None,
                 bottomleft=None, bottomright=None, centre=None,
                 labelColour=None):
        self.__screen = surface
        if width > 300:
            self.__width = width
        else:
            self.__width = 300

        if height > 300:
            self.__height = height
        else:
            self.__height = 300

        self.__rect = pg.Rect(0, 0, self.__width, self.__height)

        if topleft is not None:
            self.__rect.topleft = (int(topleft[0]), int(topleft[1]))

        elif topright is not None:
            self.__rect.topright = (int(topright[0]), int(topright[1]))

        elif bottomleft is not None:
            self.__rect.bottomleft = (int(bottomleft[0]), int(bottomleft[1]))

        elif bottomright is not None:
            self.__rect.bottomright = (int(bottomright[0]), int(bottomright[1]))

        elif centre is not None:
            self.__rect.center = (int(centre[0]), int(centre[1]))

        if labelColour is None:
            self.__textColour = (33, 33, 33)
        else:
            self.__textColour = labelColour

        self.__plots1 = []
        self.__plotCoords1 = []
        self.__plots2 = []
        self.__plotCoords2 = []
        self.__xLabels = [0]
        self.__yLabels = [0]
        self.__xInterval = 10
        self.__yInterval = 10
        self.__xSpacing = self.__width
        self.__ySpacing = self.__height
        self.__font = pg.font.SysFont("Helvetica", 18)

    def draw(self):

        pg.draw.rect(self.__screen, (222, 222, 222), self.__rect)

        startPos = self.__rect.bottomleft

        try:
            distance = self.__width / (len(self.__xLabels) - 1)
        except ZeroDivisionError:
            distance = 0

        for i in range(0, len(self.__xLabels)):
            xPos = int(startPos[0] + distance * i)
            pg.draw.line(self.__screen, (170, 170, 170),
                         (xPos, int(startPos[1])),
                         (xPos, int(startPos[1] - self.__height)), 1)
            text = self.__font.render(str(self.__xLabels[i]), True,
                                      self.__textColour)
            textRect = text.get_rect(center=(xPos, int(startPos[1] + 30)))
            self.__screen.blit(text, textRect)

        try:
            distance = self.__height / (len(self.__yLabels) - 1)
        except ZeroDivisionError:
            distance = 0

        for i in range(0, len(self.__yLabels)):
            yPos = int(startPos[1] - distance * i)
            pg.draw.line(self.__screen, (170, 170, 170),
                         (int(startPos[0]), yPos),
                         (int(startPos[0] + self.__width), yPos), 1)
            text = self.__font.render(str(self.__yLabels[i]), True,
                                      self.__textColour)
            textRect = text.get_rect(center=(int(startPos[0] - 30), yPos))
            self.__screen.blit(text, textRect)

        plots = self.__plotCoords1
        for i in range(0, len(self.__plotCoords1) - 1):
            pg.draw.line(self.__screen, (20, 20, 195),
                         (startPos[0] + plots[i][0], startPos[1] - plots[i][1]),
                         (startPos[0] + plots[i + 1][0],
                          startPos[1] - plots[i + 1][1]))

        plots = self.__plotCoords2
        for i in range(0, len(self.__plotCoords2) - 1):
            pg.draw.line(self.__screen, (195, 20, 20),
                         (startPos[0] + plots[i][0], startPos[1] - plots[i][1]),
                         (startPos[0] + plots[i + 1][0],
                          startPos[1] - plots[i + 1][1]))

        for plot in self.__plotCoords1:
            plotRect = pg.Rect(0, 0, 3, 3)
            plotRect.center = (startPos[0] + plot[0], startPos[1] - plot[1])
            pg.draw.rect(self.__screen, (20, 20, 195), plotRect)

        for plot in self.__plotCoords2:
            plotRect = pg.Rect(0, 0, 3, 3)
            plotRect.center = (startPos[0] + plot[0], startPos[1] - plot[1])
            pg.draw.rect(self.__screen, (195, 20, 20), plotRect)

    def addPlot(self, plot, position=None, line=None):
        if not type(plot) is tuple:
            raise ValueError("Plot must be type: tuple (x, y)")

        if line is None:
            line = 1

        if line == 1:
            if position is None:
                self.__plots1.append(plot)
            else:
                self.__plots1.insert(position, plot)
            if len(self.__plots1) > 1:
                self.generateLabels()
            self.convertPlots(1)

        elif line == 2:
            if position is None:
                self.__plots2.append(plot)
            else:
                self.__plots2.insert(position, plot)
            if len(self.__plots1) > 1:
                self.generateLabels()
            self.convertPlots(2)

    def convertPlots(self, line):
        if line == 1:
            self.__plotCoords1 = []
            plotList = self.__plots1
        elif line == 2:
            self.__plotCoords2 = []
            plotList = self.__plots2

        xEnd = self.__xLabels[-1]
        yEnd = self.__yLabels[-1]
        for i in plotList:
            try:
                xCoord = int(i[0] * self.__width / xEnd)
            except ZeroDivisionError:
                xCoord = 0

            try:
                yCoord = int(i[1] * self.__height / yEnd)
            except ZeroDivisionError:
                yCoord = 0

            if line == 1:
                self.__plotCoords1.append((xCoord, yCoord))
            elif line == 2:
                self.__plotCoords2.append((xCoord, yCoord))

    def highest(self, axis, line):
        if line == 1:
            largest = self.__plots1[0][axis]
            plotList = self.__plots1
        elif line == 2:
            largest = self.__plots2[0][axis]
            plotList = self.__plots2

        for i in plotList:
            if i[axis] > largest:
                largest = i[axis]
            else:
                pass
        return largest

    def findInterval(self, axis, line):
        mostticks = [self.__width, self.__height][axis] / 50

        minimum = self.highest(axis, line) / mostticks
        if minimum == 0:
            minimum = 1
        magnitude = 10 ** math.floor(math.log(minimum, 10))
        residual = minimum / magnitude
        if residual > 5:
            tick = 10 * magnitude
        elif residual > 2:
            tick = 5 * magnitude
        elif residual > 1:
            tick = 2 * magnitude
        else:
            tick = magnitude
        return tick

    def getPlots(self):
        return self.__plots1

    def getLabels(self):
        return [self.__xLabels, self.__yLabels]

    def generateLabels(self):
        xLine = 1
        yLine = 1
        try:
            if self.highest(0, 1) < self.highest(0, 2):
                xLine = 2
            if self.highest(1, 1) < self.highest(1, 2):
                yLine = 2
        except IndexError:
            if len(self.__plots1) == 0:
                xLine = 2
                yLine = 2
            elif len(self.__plots2) == 0:
                xLine = 1
                yLine = 1

        self.__xLabels = [self.__xLabels[0]]
        self.__yLabels = [self.__yLabels[0]]
        self.__xInterval = self.findInterval(0, xLine)
        self.__yInterval = self.findInterval(1, yLine)

        currentNum = self.__xLabels[0]
        while currentNum < self.highest(0, xLine):
            currentNum += self.__xInterval
            self.__xLabels.append(round(currentNum, 2))

        currentNum = self.__yLabels[0]
        while currentNum < self.highest(1, yLine):
            currentNum += self.__yInterval
            self.__yLabels.append(round(currentNum, 2))

    def labelSpacing(self):
        self.__ySpacing = self.__height // len(self.__yLabels)
        self.__xSpacing = self.__width // len(self.__xLabels)


if __name__ == "__main__":
    pg.init()
    pg.font.init()
    screen = pg.display.set_mode((1920, 1080))
    pgp = Pgp(screen, 500, 500, centre=(960, 500))

    x = 0
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event == pg.QUIT:
                pg.quit()
                quit()
        screen.fill((255, 255, 255))
        try:
            pgp.addPlot((x, math.sqrt(25-(x-5)**2)+5))
            pgp.addPlot((x, -math.sqrt(25 - (x - 5) ** 2) + 5))
        except ValueError:
            pass
        x += 0.01
        pgp.draw()
        pg.display.update()
        fps = str(int(clock.get_fps()))
        pg.display.set_caption('GRAPH | FPS: ' + fps)
        clock.tick()

