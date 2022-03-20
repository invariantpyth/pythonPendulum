import cv2 as cv
import Pendulum
import numpy as np

PATH_LENGTH = 500
class Frame:
    width: int
    height: int
    pendulum: Pendulum
    path: np.ndarray
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
        self.path = np.zeros((PATH_LENGTH, 3))

    def update(self):
        self.pendulum.iterate()

    def draw(self):
        def transform(point: np.ndarray, width: int, height: int):
            n = int(min(width, height) / 9)
            mid_w = int(width / 2)
            mid_h = int(height / 2)
            point_tr = 3.5 * n * point
            point_tr[0] += mid_w
            point_tr[1] = mid_h + point_tr[1]
            point_tr = np.array(point_tr, dtype=int)

            return point_tr


        n = int(min(self.width, self.height))
        pt0 = tuple(transform(np.array([0, 0]), self.width, self.height))
        pt1 = tuple(transform(self.pendulum.get_cartesian1(), self.width, self.height))
        pt2 = tuple(transform(self.pendulum.get_cartesian2(), self.width, self.height))

        coord = np.asarray(pt2)
        coord.resize((1, 3))
        coord[0, 2] = 1
        # print(pt2, coord)
        self.path = np.append(self.path, coord, 0)
        self.path = self.path[1:]

        img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        img[:] = self.background_color

        # drawing path curve
        for index, point in enumerate(self.path):
            if point[2] != 0 and index != PATH_LENGTH - 1:
                cv.line(img,
                        (int(point[0]), int(point[1])),
                        (int(self.path[index + 1][0]), int(self.path[index + 1][1])),
                        self.path_color,
                        3)


        # drawing links of the pendulum

        cv.line(img, pt0, pt1, self.link_color, 3)
        cv.line(img, pt1, pt2, self.link_color, 3)
        cv.circle(img, pt1, int(n / 40), self.middle_color, 3)
        cv.circle(img, pt2, int(n / 40), self.middle_color, 3)
        return img
