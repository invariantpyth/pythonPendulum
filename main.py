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


    # theta1 = (np.pi / 1),
    # theta2 = (np.pi / 1),
    pendulum = Pendulum(theta1=2 * np.pi * rnd.random(),
                        theta2=2 * np.pi * rnd.random(),
                        p1=1,
                        p2=1,
                        time=0,
                        mass=1,
                        length=0.5)
    frame = Frame(width=WIDTH,
                  height=HEIGHT,
                  pendulum=pendulum,
                  background_color=BACKGROUND_COLOR,
                  link_color=LINK_COLOR,
                  middle_color=MIDDLE_COLOR,
                  path_color=PATH_COLOR)


    # cv.imwrite('sample.png', frame.draw())
    out = cv.VideoWriter(f'/home/maxim/Yandex.Disk/Фильмы/pendulum_{pendulum.theta1}_{pendulum.theta2}_{pendulum.p1}_{pendulum.p2}.mp4', cv.VideoWriter_fourcc('m', 'p', '4', 'v'), FPS, (WIDTH, HEIGHT))

    percent = 0
    previous_percent = -1
    img = frame.draw()
    out.write(img)
    frame_amount = FPS * 60 * 2
    for i in range(frame_amount):
        percent = int(100 * (i + 0.5) / frame_amount)
        if percent > previous_percent:
            print(f'{percent}% of the video is recorded')
            previous_percent = percent
        frame.update()
        # print(pendulum.theta1, pendulum.theta2, pendulum.p1, pendulum.p2)
        img = frame.draw()
        out.write(img)

    out.release()


    print(f'{100}% of the video is recorded')

if __name__ == '__main__':
    main()
