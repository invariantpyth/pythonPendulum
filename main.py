from Pendulum import Pendulum
from Frame import Frame
import numpy as np
import random as rnd
import cv2 as cv

# GLOBALS
FPS = 60
WIDTH = 1080
HEIGHT = 1920
BACKGROUND_COLOR = np.array([60.0, 51.0, 54.0])
LINK_COLOR = np.array([256.0, 256.0, 256.0])
MIDDLE_COLOR = np.array([2.0, 159.0, 254.0])
PATH_COLOR = np.array([55.0, 102.0, 219.0])


def main():
    # theta1 = 2 * np.pi * rnd.random(),
    # theta2 = 2 * np.pi * rnd.random()
    pendulum = Pendulum(theta1=(np.pi / 2),
                        theta2=(np.pi / 2),
                        p1=0,
                        p2=0,
                        time=0,
                        mass=10,
                        length=0.5)
    frame = Frame(width=WIDTH,
                  height=HEIGHT,
                  pendulum=pendulum,
                  background_color=BACKGROUND_COLOR,
                  link_color=LINK_COLOR,
                  middle_color=MIDDLE_COLOR,
                  path_color=PATH_COLOR)


    # cv.imwrite('sample.png', frame.draw())
    out = cv.VideoWriter('/home/maxim/Yandex.Disk/Фильмы/pendulum.mp4', cv.VideoWriter_fourcc('m', 'p', '4', 'v'), FPS, (WIDTH, HEIGHT))

    percent = 0
    previous_percent = -1
    img = frame.draw()
    out.write(img)
    for i in range(FPS * 60):
        percent = int(100 * i / (FPS * 60))
        if percent > previous_percent:
            print(f'{percent}% of the video is recorded')
            previous_percent = percent
        frame.pendulum.iterate()
        print(pendulum.theta1, pendulum.theta2, pendulum.p1, pendulum.p2)
        img = frame.draw()
        out.write(img)

    out.release()


if __name__ == '__main__':
    main()
