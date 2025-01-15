from solid_geometry import *

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import transforms

from io import BytesIO


def normalize_section(section, point_1, point_2, point_3):
    if is_perpendicular_to_xy_plane(point_1, point_2, point_3):
        section[:, 2] += np.random.normal(scale=0.001, size=len(section))
    elif is_perpendicular_to_xz_plane(point_1, point_2, point_3):
        section[:, 1] += np.random.normal(scale=0.001, size=len(section))
    elif is_perpendicular_to_yz_plane(point_1, point_2, point_3):
        section[:, 0] += np.random.normal(scale=0.001, size=len(section))

    return section


def build_figure(vertices, faces):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.grid(True)

    ax.set_xlabel('Y')
    ax.set_ylabel('X')
    ax.set_zlabel('Z')
    ax.invert_yaxis()

    poly3d = [[(vertices[f]) for f in face] for face in faces]
    ax.add_collection3d(
        Poly3DCollection(poly3d, facecolors=['cyan', 'magenta'], alpha=0.05, linewidths=1, edgecolors='k'))

    # ax.view_init(elev=30, azim=70)
    # angle = np.deg2rad(30)
    #
    # # Создание аффинной трансформации
    # trans = transforms.Affine2D().rotate(angle)
    #
    # # Применение трансформации к оси
    # ax.set_transform(trans + ax.transData)

    return ax, fig


def build_parallelepiped(length: float, width: float, height: float):
    parallelepiped = Parallelepiped(length, width, height)

    vertices = parallelepiped.get_vertices()
    faces = parallelepiped.get_faces()

    ax, fig = build_figure(vertices, faces)

    return parallelepiped, ax, fig


def build_section_parallelepiped(length: float, width: float, height: float,
                                 point_1: point, point_2: point, point_3: point):
    parallelepiped, ax, fig = build_parallelepiped(length, width, height)

    section = normalize_section(parallelepiped.intersect_plane_with_edges(point_1, point_2, point_3),
                                point_1, point_2, point_3)

    if len(section) != 0:
        ax.scatter(section[:, 0], section[:, 1], section[:, 2], c='r', marker='o')
    else:
        message = "Нет точек сечения."
        return fig, message

    unique_points = np.unique(section, axis=0)
    if len(unique_points) < 3:
        message = "Недостаточно точек для визуализации сечения."
        return fig, message
    else:
        ax.plot_trisurf(section[:, 0], section[:, 1], section[:, 2], color='red', alpha=0.4)

    message = None
    return fig, message


def build_tetrahedron(coefficient: float):
    tetrahedron = Tetrahedron(coefficient)

    vertices = tetrahedron.get_vertices()
    faces = tetrahedron.get_faces()

    ax, fig = build_figure(vertices, faces)

    return tetrahedron, ax, fig


def build_section_tetrahedron(coefficient: float,
                              point_1: point, point_2: point, point_3: point):
    tetrahedron, ax, fig = build_tetrahedron(coefficient)

    section = normalize_section(tetrahedron.intersect_plane_with_edges(point_1, point_2, point_3),
                                point_1, point_2, point_3)

    message = None
    if len(section) != 0:
        ax.scatter(section[:, 0], section[:, 1], section[:, 2], c='r', marker='o')
    else:
        message = "Нет точек сечения."
        return fig, message

    unique_points = np.unique(section, axis=0)
    if len(unique_points) < 3:
        message = "Недостаточно точек для визуализации сечения."
        return fig, message
    else:
        ax.plot_trisurf(section[:, 0], section[:, 1], section[:, 2], color='red', alpha=0.4)

    return fig, message


def figure_to_bytes(fig) -> bytes:
    buf = BytesIO()
    fig.savefig(buf, format='png')
    return buf.getvalue()
