import numpy as np
import math as m

FPS = 60
DT = 1 / FPS
G = 9.81


class Pendulum:
    theta1: float
    theta2: float
    p1: float
    p2: float
    time: float
    mass: float
    length: float
    path: np.ndarray

    def __init__(self, theta1, theta2, p1, p2, time, mass, length, path=np.zeros((500, 3))):
        self.theta1 = theta1
        self.theta2 = theta2
        self.p1 = p1
        self.p2 = p2
        self.time = time
        self.mass = mass
        self.length = length
        self.path = path

    # translators from angles between pendulum links and vertical line to cartesian coordinates
    def get_cartesian1(self) -> np.ndarray:
        x, y = np.array((self.length * m.sin(self.theta1) / (2 * self.length),
                         self.length * m.cos(self.theta1) / (2 * self.length)))
        return np.array([x, y])

    def get_cartesian2(self) -> np.ndarray:
        x, y = np.array((self.length * (m.sin(self.theta1) + m.sin(self.theta2)) / (2.0 * self.length),
                         self.length * (m.cos(self.theta1) + m.cos(self.theta2)) / (2.0 * self.length)))
        return np.array([x, y])

    # right part of the differential equation dtheta/dt = f(theta)
    # f1 is for the first link of the pendulum, f2 is for the second
    def f1(self) -> float:
        f: float = ((6 / (self.mass * self.length ** 2)) *
                    (2 * self.p1 - 3 * m.cos(self.theta1 - self.theta2) * self.p2) /
                    (16 - 9 * m.cos(self.theta1 - self.theta2) ** 2))
        return f

    def f2(self) -> float:
        f: float = ((6 / (self.mass * self.length ** 2)) *
                    (8 * self.p2 - 3 * m.cos(self.theta1 - self.theta2) * self.p1) /
                    (16 - 9 * m.cos(self.theta1 - self.theta2) ** 2))
        return f

    def corrector1(self):
        p = Pendulum(theta1=(self.theta1 + DT * self.f1()),
                     theta2=self.theta2,
                     p1=self.p1,
                     p2=self.p2,
                     time=self.time,
                     length=self.length,
                     mass=self.mass,
                     path=self.path)
        return p

    def corrector2(self):
        p = Pendulum(theta2=(self.theta2 + DT * self.f2()),
                     theta1=self.theta1,
                     p1=self.p1,
                     p2=self.p2,
                     time=self.time,
                     length=self.length,
                     mass=self.mass,
                     path=self.path)
        return p

    def iterate(self):
        self.theta1 = (self.theta1 +
                       DT * (self.f1() + self.corrector1().f1()) / 2.0)
        self.theta1 = self.theta1 - (self.theta1 // (2 * np.pi)) * (2 * np.pi)

        self.theta2 = (self.theta2 +
                       DT * (self.f2() + self.corrector2().f2()) / 2.0)
        self.theta2 = self.theta2 - (self.theta2 // (2 * np.pi)) * (2 * np.pi)

        self.time += DT

        dp1 = ((self.mass * self.length ** 2 / 2.0) *
               (self.f1() * self.f2() * m.sin(self.theta1 - self.theta2) +
                3.0 * G * m.sin(self.theta1) / self.length) * DT)
        dp2 = ((self.mass * self.length ** 2 / 2.0) *
               (-self.f1() * self.f2() * m.sin(self.theta1 - self.theta2) +
                G * m.sin(self.theta1) / self.length) * DT)

        self.p1 += dp1

        self.p2 += dp2

        # add new coordinate to the end of the path array and removing the first coordinate
        coord = self.get_cartesian2()
        coord = np.array([coord[0], coord[1], 1], dtype=float)
        coord.resize((1, 3))
        self.path = np.append(self.path, coord, 0)
        self.path = self.path[1:]
