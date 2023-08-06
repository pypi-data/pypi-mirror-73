
class vec3d:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vector = (self.x, self.y, self.z)

    def __repr__(self):
        """Default print statement"""
        return f'<({self.x}, {self.y}, {self.z})>'

    def __str__(self):
        """Default print statement"""
        return f'<({self.x}, {self.y}, {self.z})>'

    def __add__(self, other):
        """Defintion of addition of two vectors, returns a vec3d-object."""
        if isinstance(other, vec3d):
            return vec3d(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            pass

    def __radd__(self, other):
        """Definition of reverse addition of two vectors, returns a vec3d-object."""
        if isinstance(other, vec3d):
            return vec3d(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            pass

    def __sub__(self, other):
        """Definition of subtraction of two vectors, returns a vec3d-object.s"""
        if isinstance(other, vec3d):
            return vec3d(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            pass

    def __rsub__(self, other):
        """Definition of reverse-subtraction of two vectors, returns a vec3d-object.s"""
        if isinstance(other, vec3d):
            return vec3d(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            pass

    def __mul__(self, value):
        """Definition of scalar multiplication, only works with float or integers; Returns a vec3d-object.s"""
        if isinstance(value, vec3d):
            pass
        elif isinstance(value, (float, int)):
            return vec3d(self.x * value, self.y * value, self.z * value)
        else:
            pass

    def __rmul__(self, value):
        """Definition of reverse-scalar multiplication, only works with float or integers; Returns a vec3d-object.s"""
        if isinstance(value, vec3d):
            pass
        else:
            return vec3d(self.x * value, self.y * value, self.z * value)

    def __getitem__(self, Index):
        """Get the value of the vec3d-object at index 'Index'."""
        return self.vector[Index]

    def dot(self, other):
        """Compute the dot-product of two vectors, returns a float or integer."""
        if isinstance(other, vec3d):
            value = self.x * other.x + self.y * other.y + self.z * other.z
            if value != 0:
                return value
            else:
                return None
        else:
            pass

    def cross(self, other):
        """Compute the cross-product of two vec3d-objects; Returns a vec3d-object."""
        if isinstance(other, vec3d):
            col1 = self.y * other.z - self.z * other.y
            col2 = self.z * other.x - self.x * other.z
            col3 = self.x * other.y - self.y * other.z
            return vec3d(col1, col2, col3)
        else:
            pass

    def norm(self):
        """Calculates the norm of a given vector, returns a scalar of either type integer or float."""
        value = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** (1/2)
        return value

    def normalize(self):
        """Normalizes a vector with self.norm() function and returns a vec3d-object"""
        return 1 / (self.norm()) * vec3d(self.vec1, self.vec2, self.vec3) # a valid solution is * self


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
