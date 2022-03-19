import cv2 as cv
import Pendulum
import numpy as np


class Frame:
    width: int
    height: int
    pendulum: Pendulum
    background_color: np.ndarray  # in BGR
    link_color: np.ndarray  # in BGR
    middle_color: np.ndarray  # in BGR
    path_color: np.ndarray  # in BGR

    def __init__(self, width: int,
                 height: int,
                 pendulum: Pendulum,
                 background_color: np.ndarray,
                 link_color: np.ndarray,
                 middle_color: np.ndarray,
                 path_color: np.ndarray) -> object:
        self.width = width
        self.height = height
        self.pendulum = pendulum
        self.background_color = background_color
        self.link_color = link_color
        self.middle_color = middle_color
        self.path_color = path_color

    def update(self):
        self.pendulum.iterate()

    def draw(self):
        n = int(min(self.width, self.height))

        def transform(point: np.ndarray, width: int, height: int):
            n = int(min(width, height) / 9)
            mid_w = int(width / 2)
            mid_h = int(height / 2)
            point_tr = 3.5 * n * point
            point_tr[0] += mid_w
            point_tr[1] = mid_h - point_tr[1]
            point_tr = np.array(point_tr, dtype=int)

            return point_tr

        img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        img[:] = self.background_color

        # # drawing path curve
        # for point in self.pendulum.path:
        #     if point[2] != 0:
        #         point_tr = transform(point, self.width, self.height)
        #         img[point_tr[0], point_tr[1]] = self.path_color

        # drawing links of the pendulum
        pt0 = tuple(transform(np.array([0, 0]), self.width, self.height))
        pt1 = tuple(transform(self.pendulum.get_cartesian1(), self.width, self.height))
        pt2 = tuple(transform(self.pendulum.get_cartesian2(), self.width, self.height))
        cv.line(img, pt0, pt1, self.link_color, 3)
        cv.line(img, pt1, pt2, self.link_color, 3)
        cv.circle(img, pt1, int(n / 40), self.middle_color, 3)
        cv.circle(img, pt2, int(n / 40), self.middle_color, 3)
        return img
