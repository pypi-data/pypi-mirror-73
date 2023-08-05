import pygame as pg
import pgplot
import time
import math


def circle():
    screen = pg.display.set_mode((1920, 1080))
    pgp = pgplot.Pgp(screen, 500, 500, centre=(960, 500))
    x = 0
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event == pg.QUIT:
                pg.quit()
                quit()
        screen.fill((255, 255, 255))
        try:
            pgp.addPlot((x, math.sqrt(25 - (x - 5) ** 2) + 5))
            pgp.addPlot((x, -math.sqrt(25 - (x - 5) ** 2) + 5))
        except ValueError:
            pass
        x += 0.01
        pgp.draw()
        pg.display.update()
        fps = str(int(clock.get_fps()))
        pg.display.set_caption('Circle Example | FPS: ' + fps)
        clock.tick()


def idk():
    screen = pg.display.set_mode((1920, 1080))
    pgp = pgplot.Pgp(screen, 500, 500, centre=(960, 500))
    x = 0
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event == pg.QUIT:
                pg.quit()
                quit()
        screen.fill((255, 255, 255))
        if x <= 3:
            print(x)
            pgp.addPlot((x, abs(math.sin(x ** x) / (
                    2 ** (((x ** x) - math.pi / 2) / math.pi)))))
            x += 0.005
        pgp.draw()
        pg.display.update()
        fps = str(int(clock.get_fps()))
        pg.display.set_caption('Circle Example | FPS: ' + fps)
        clock.tick()


def sinCos():
    screen = pg.display.set_mode((1920, 1080))
    pgp = pgplot.Pgp(screen, 500, 500, centre=(960, 500))
    x = 0
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event == pg.QUIT:
                pg.quit()
                quit()
        screen.fill((255, 255, 255))
        if x <= 360:
            pgp.addPlot((x, math.sin(math.radians(x)) + 1))
            pgp.addPlot((x, math.cos(math.radians(x)) + 1), line=2)
        x += 1
        pgp.draw()
        pg.display.update()
        fps = str(int(clock.get_fps()))
        pg.display.set_caption('Circle Example | FPS: ' + fps)
        clock.tick()


def root():
    screen = pg.display.set_mode((1920, 1080))
    pgp = pgplot.Pgp(screen, 500, 50, centre=(960, 500))
    x = 0
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event == pg.QUIT:
                pg.quit()
                quit()
        screen.fill((255, 255, 255))
        if x <= 100:
            pgp.addPlot((x, math.sqrt(x)))
        x += 0.1
        pgp.draw()
        pg.display.update()
        fps = str(int(clock.get_fps()))
        pg.display.set_caption('Circle Example | FPS: ' + fps)
        clock.tick()


def ln():
    screen = pg.display.set_mode((1920, 1080))
    pgp = pgplot.Pgp(screen, 500, 300, centre=(960, 500))
    x = 1
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event == pg.QUIT:
                pg.quit()
                quit()
        screen.fill((255, 255, 255))
        if x <= 100:
            pgp.addPlot((x, math.log(x, math.e)))
        x += 0.1
        pgp.draw()
        pg.display.update()
        fps = str(int(clock.get_fps()))
        pg.display.set_caption('Circle Example | FPS: ' + fps)
        clock.tick()


def sinxx():
    screen = pg.display.set_mode((1920, 1080))
    pgp = pgplot.Pgp(screen, 500, 500, centre=(960, 500))
    x = 0
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event == pg.QUIT:
                pg.quit()
                quit()
        screen.fill((255, 255, 255))
        if x <= 10:
            pgp.addPlot((x, abs(math.sin(math.radians(x ** x)))))
        x += 0.0025
        pgp.draw()
        pg.display.update()
        fps = str(int(clock.get_fps()))
        pg.display.set_caption('Circle Example | FPS: ' + fps)
        clock.tick()


def idk2():
    screen = pg.display.set_mode((1920, 1080))
    pgp = pgplot.Pgp(screen, 500, 500, centre=(960, 500))
    x = 0
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event == pg.QUIT:
                pg.quit()
                quit()
        screen.fill((255, 255, 255))
        if x <= 1:
            print(x)
            pgp.addPlot((x, abs(math.sin(x ** x) / (
                    2 ** (((x ** x) - math.pi / 2) / math.pi)))))
            x += 0.005
        pgp.draw()
        pg.display.update()
        fps = str(int(clock.get_fps()))
        pg.display.set_caption('Circle Example | FPS: ' + fps)
        clock.tick()


if __name__ == "__main__":
    pg.init()
    pg.font.init()

    print('''


    @@@@@@@@@@@@@@@@@@@@@@@@
    @@                    @@
    @@                    @@
    @@     1) Circle      @@
    @@                    @@
    @@    2) Sin & Cos    @@
    @@                    @@
    @@     3) Root x      @@
    @@                    @@
    @@      4) Ln x       @@
    @@                    @@
    @@    5) Sin(x^x)     @@  
    @@                    @@
    @@    6) ¯\_(ツ)_/¯    @@
    @@                    @@
    @@@@@@@@@@@@@@@@@@@@@@@@

    ''')

    choice = 'None'
    choiceList = ['1', '2', '3', '4', '5', '6']

    while choice not in choiceList:
        choice = input('Enter choice [1/2/3/4/5/6]: ')
    if choice == "1":
        time.sleep(0.5)
        circle()
    if choice == "2":
        time.sleep(0.5)
        sinCos()
    if choice == "3":
        time.sleep(0.5)
        root()
    if choice == "4":
        time.sleep(0.5)
        ln()
    if choice == "5":
        time.sleep(0.5)
        sinxx()
    if choice == "6":
        time.sleep(0.5)
        idk()
