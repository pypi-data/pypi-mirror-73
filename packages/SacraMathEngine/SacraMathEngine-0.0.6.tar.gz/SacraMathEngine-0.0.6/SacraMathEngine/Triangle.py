from .Vector import vec3d
from .Matrix import matrix3d
#from SacraMathEngine import vec3d
#import json

class Triangle:
    def __init__(self, vec1, vec2, vec3):
        """
        if not isinstance((vec1, vec2, vec3), vec3d):
            raise TypeError("Wrong format in Triangle")
        """
        self.vec1 = vec1
        self.vec2 = vec2
        self.vec3 = vec3
        self.set = (self.vec1, self.vec2, self.vec3)

    def __str__(self):
        """Print statement for Triangle-object"""
        return f'[{self.vec1}, {self.vec2}, {self.vec3}]'

    def __len__(self):
        """Return the length of triangle, which is 3 by definition. """
        return 3 #Could be len(self.set)

    def __getitem__(self, index):
        """Get the vector defined at index 'index', given the attribute 'index'."""
        return self.set[index]

    def __mul__(self, Scalar):
        """Returns a Triangle-object where each vector i multiplied by the scalar 'Scalar'."""
        if isinstance(Scalar, (float, int)):
            return Triangle(self.vec1 * Scalar, self.vec2 * Saclar, self.vec3 * Scalar)
        else:
            pass
