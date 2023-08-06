
class vec3d:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vector = (self.x, self.y, self.z)

    def __str__(self):
        return f'<({self.x}, {self.y}, {self.z})>'

    def __add__(self, other):
        if isinstance(other, vec3d):
            return vec3d(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            pass

    def __radd__(self, other):
        if isinstance(other, vec3d):
            return vec3d(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            pass

    def __sub__(self, other):
        if isinstance(other, vec3d):
            return vec3d(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            pass

    def __rsub__(self, other):
        if isinstance(other, vec3d):
            return vec3d(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            pass

    def __mul__(self, value):
        if isinstance(value, vec3d):
            pass
        else:
            return vec3d(self.x * value, self.y * value, self.z * value)

    def __rmul__(self, value):
        if isinstance(value, vec3d):
            pass
        else:
            return vec3d(self.x * value, self.y * value, self.z * value)

    def __getitem__(self, index):
        return self.vector[index]

    def dot(self, other):
        if isinstance(other, vec3d):
            value = self.x * other.x + self.y * other.y + self.z * other.z
            return value
        else:
            pass

    def cross(self, other):
        if isinstance(other, vec3d):
            col1 = self.y * other.z - self.z * other.y
            col2 = self.z * other.x - self.x * other.z
            col3 = self.x * other.y - self.y * other.z
            return vec3d(col1, col2, col3)
        else:
            pass

    def norm(self):
        value = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** (1/2)
        return value

    def normalize(self):
        return 1 / (self.norm()) * self


class vec4d:

    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.vector = (self.x, self.y, self.z, self.w)

    def __truediv__(self, value):
        if value != 0:
            x, y, z, w = self.x / value, self.y / value, self.z / value, self.w / value
            return vec4d(x, y, z, w)
        else:
            pass
    def __add__(self, other):
        return vec4d(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)
