import numpy as np
from math import sqrt
from typing import Tuple
import re

point = Tuple[float, float, float]


def is_correct_coordinates(s: str) -> bool:
    pattern = r'^[-+]?\d+\.\d+|[-+]?\d+$'
    parts = s.split()

    if len(parts) != 3:
        return False

    for part in parts:
        if not re.match(pattern, part):
            return False

    return True


def is_positive_number(s: str) -> bool:
    try:
        number = float(s)
        if number > 0:
            return True
        else:
            return False
    except ValueError:
        return False


def are_points_collinear(point_1: point, point_2: point, point_3: point) -> bool:
    ab = np.array(point_2) - np.array(point_1)
    ac = np.array(point_3) - np.array(point_1)
    cross_product = np.cross(ab, ac)
    return np.allclose(cross_product, np.zeros_like(cross_product))


def is_perpendicular_to_xy_plane(a: point, b: point, c: point):
    ab = np.array([b[0] - a[0], b[1] - a[1], b[2] - a[2]])
    ac = np.array([c[0] - a[0], c[1] - a[1], c[2] - a[2]])

    n = np.cross(ab, ac)

    return np.isclose(n[0], 0) and np.isclose(n[1], 0)


def is_perpendicular_to_xz_plane(a: point, b: point, c: point):
    ab = np.array([b[0] - a[0], b[1] - a[1], b[2] - a[2]])
    ac = np.array([c[0] - a[0], c[1] - a[1], c[2] - a[2]])

    n = np.cross(ab, ac)

    return np.isclose(n[0], 0) and np.isclose(n[2], 0)


def is_perpendicular_to_yz_plane(a: point, b: point, c: point):
    ab = np.array([b[0] - a[0], b[1] - a[1], b[2] - a[2]])
    ac = np.array([c[0] - a[0], c[1] - a[1], c[2] - a[2]])

    n = np.cross(ab, ac)

    return np.isclose(n[1], 0) and np.isclose(n[2], 0)


class PointsConverter:
    def __init__(self, point_1: point, point_2: point, point_3: point):
        self.points = np.array([
            point_1,
            point_2,
            point_3
        ])

    def normal_vector(self):
        a = self.points[1] - self.points[0]
        b = self.points[2] - self.points[0]
        n = np.cross(a, b)
        return n / np.linalg.norm(n)

    def plane_coefficients(self):
        n = self.normal_vector()
        a, b, c = n
        d = -np.dot(n, self.points[0])
        return a, b, c, d


class Parallelepiped:
    def __init__(self, length: float, width: float, height: float):
        self.length = length
        self.width = width
        self.height = height

        self.vertices = np.array([
            [0, 0, 0],
            [length, 0, 0],
            [length, width, 0],
            [0, width, 0],
            [0, 0, height],
            [length, 0, height],
            [length, width, height],
            [0, width, height]
        ])

        self.faces = [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [0, 1, 5, 4],
            [1, 2, 6, 5],
            [2, 3, 7, 6],
            [3, 0, 4, 7]
        ]

    def get_vertices(self):
        return self.vertices

    def get_faces(self):
        return self.faces

    def intersect_plane_with_edges(self, point_1: point, point_2: point, point_3: point):
        section_vertices = []

        points_convertor = PointsConverter(point_1, point_2, point_3)

        a, b, c, d = points_convertor.plane_coefficients()

        for face in self.faces:
            v1, v2, v3, v4 = self.vertices[face]

            edges = [(v1, v2), (v2, v3), (v3, v4), (v4, v1)]

            for edge in edges:
                p1, p2 = edge
                denom = a * (p2[0] - p1[0]) + b * (p2[1] - p1[1]) + c * (p2[2] - p1[2])
                if abs(denom) > 1e-8:
                    t = -(a * p1[0] + b * p1[1] + c * p1[2] + d) / denom
                    if 0 <= t <= 1:
                        intersection = p1 + t * (p2 - p1)
                        section_vertices.append(intersection)

        return np.array(section_vertices)


class Tetrahedron:
    def __init__(self, coefficient: float):
        self.coefficient = coefficient

        self.vertices = np.array([
            [0, 0, 0],
            [coefficient, 0, 0],
            [coefficient / 2, sqrt(3) * coefficient / 2, 0],
            [coefficient / 2, sqrt(3) * coefficient / 5, sqrt(3) * coefficient / 2]
        ])

        self.faces = [
            [0, 1, 2],
            [1, 2, 3],
            [2, 0, 3],
            [0, 1, 3]
        ]

    def get_vertices(self):
        return self.vertices

    def get_faces(self):
        return self.faces

    def intersect_plane_with_edges(self, point_1: point, point_2: point, point_3: point):
        section_vertices = []

        points_convertor = PointsConverter(point_1, point_2, point_3)

        a, b, c, d = points_convertor.plane_coefficients()

        for face in self.faces:
            v1, v2, v3, = self.vertices[face]

            edges = [(v1, v2), (v2, v3), (v3, v1)]

            for edge in edges:
                p1, p2 = edge
                denom = a * (p2[0] - p1[0]) + b * (p2[1] - p1[1]) + c * (p2[2] - p1[2])
                if abs(denom) > 1e-8:
                    t = -(a * p1[0] + b * p1[1] + c * p1[2] + d) / denom
                    if 0 <= t <= 1:
                        intersection = p1 + t * (p2 - p1)
                        section_vertices.append(intersection)

        return np.array(section_vertices)
