from .Vector import vec3d
from math import tan, pi

class matrix3d:
    """ Intalizes a matrix which is in R^3 space; Of which the basic eigen-values can be computed. """
    def __init__(self, vec1, vec2, vec3):
        self.vec1 = vec1
        self.vec2 = vec2
        self.vec3 = vec3
        self.matrix = (self.vec1, self.vec2, self.vec3)

    def __str__(self):
        return f'<({self.vec1[0]}, {self.vec1[1]}, {self.vec1[2]})\n ({self.vec2[0]}, {self.vec2[1]}, {self.vec2[2]})\n ({self.vec3[0]}, {self.vec3[1]}, {self.vec3[2]})>'

    def __add__(self, other):
        if isinstance(other, matrix3d):
            return matrix3d(self.vec1 + other.vec1, self.vec2 + other.vec2, self.vec3 + other.vec3)
        else:
            pass

    def __radd__(self, other):
        if isinstance(other, matrix3d):
            return matrix3d(self.vec1 + other.vec1, self.vec2 + other.vec2, self.vec3 + other.vec3)
        else:
            pass

    def __sub__(self, other):
        if isinstance(other, matrix3d):
            return matrix3d(self.vec1 - other.vec1, self.vec2 - other.vec2, self.vec3 - other.vec3)
        else:
            pass

    def __rsub__(self, other):
        if isinstance(other, matrix3d):
            return matrix3d(self.vec1 - other.vec1, self.vec2 - other.vec2, self.vec3 - other.vec3)
        else:
            pass

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return matrix3d(vec1 * other, vec2 * other, vec3 * other)
        elif isinstance(other, vec3d):
            col1 = self.vec1[0] * other[0] + self.vec1[1] * other[1] + self.vec1[2] * other[2]
            col2 = self.vec2[0] * other[0] + self.vec2[1] * other[1] + self.vec2[2] * other[2]
            col3 = self.vec3[0] * other[0] + self.vec3[1] * other[1] + self.vec3[2] * other[2]
            return vec3d(col1, col2, col3)
        elif isinstance(other, matrix3d):
            x1 = self.vec1[0] * other.vec1[0] + self.vec1[1] * other.vec2[0] + self.vec1[2] * other.vec3[0]
            x2 = self.vec1[0] * other.vec1[1] + self.vec1[1] * other.vec2[1] + self.vec1[2] * other.vec3[1]
            x3 = self.vec1[0] * other.vec1[2] + self.vec1[1] * other.vec2[2] + self.vec1[2] * other.vec3[2]
            nvec1 = vec3d(x1, x2, x3)
            y1 = self.vec2[0] * other.vec1[0] + self.vec2[1] * other.vec2[0] + self.vec2[2] * other.vec3[0]
            y2 = self.vec2[0] * other.vec1[1] + self.vec2[1] * other.vec2[1] + self.vec2[2] * other.vec3[1]
            y3 = self.vec2[0] * other.vec1[2] + self.vec2[1] * other.vec2[2] + self.vec2[2] * other.vec3[2]
            nvec2 = vec3d(y1, y2, y3)
            z1 = self.vec3[0] * other.vec1[0] + self.vec3[1] * other.vec2[0] + self.vec3[2] * other.vec3[0]
            z2 = self.vec3[0] * other.vec1[1] + self.vec3[1] * other.vec2[1] + self.vec3[2] * other.vec3[1]
            z3 = self.vec3[0] * other.vec1[2] + self.vec3[1] * other.vec2[2] + self.vec3[2] * other.vec3[2]
            nvec3 = vec3d(z1, z2, z3)
            return matrix3d(nvec1, nvec2, nvec3)
        else:
            pass

    def trace(self):
        return self.vec1[0] + self.vec2[1] + self.vec3[2]

class Matrix4d:

    def __init__(self, type = None, size = (1000,1000)):
        """ Each vector is a fourdimensional tuple """
        self.size = size
        if type == None:
            self.type = "Projection"
            self.InitializeProjection()

    def InitializeProjection(self):
        self.Near = 0.1
        self.Far = 1000
        self.Fov = 90
        self.Aspectratio = self.size[0] / self.size[1]
        self.fFovRad = 1 / tan(self.Fov * 0.5 / 180 * pi)
        vec1 = [self.Aspectratio * self.fFovRad, 0, 0, 0]
        vec2 = [0, self.fFovRad, 0, 0]
        vec3 = [0, 0, (-self.far * self.Near) / (self.Far - self.Near), 1]
        vec4 = [0, 0, self.Near, 0]

    def Mat4xvec4(self, vector):
        pass
