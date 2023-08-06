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


class MeshObject:
    def __init__(self, Object, Name):
        if not isinstance(Object, dict):
            raise KeyError("Cannot load current file-type")
        else:
            self.Name = Name
            self.Clearobject = Object
            self.Object = Object[Name]

    def __mul__(self, Scalar):
        """Instructs to multiply each triangle, which is defined in Triangle.__mul__() """
        NewObject = []
        for i in range(len(self.Object)):
            NewObject.append(self.Object * Scalar)
        Object = {f'{self.Name}' : NewObject}
        return MeshObject(Object, self.Name)


    def __str__(self):
        """Print function call. """
        return f'{[tri for tri in self.Object]}'
        #json.dumps(self.Clearobjects, indent=4, sort_keys=True))


    def __len__(self):
        """Returns the length of the mesh, the number of triangles"""
        return len(self.Object)
        pass

    def __getitem__(self, index):
        """Given an attribute 'index', return the Triangle-object at index 'index'."""
        return self.Object[index]

"""
Cube = {
    "Cube" : [[[vec3d(0, 0, 0), vec3d(0, 1, 0), vec3d(1, 1, 0)],
    [vec3d(0, 0, 0), vec3d(1, 1, 0), vec3d(1, 0, 0)]],
    [[vec3d(1, 0, 0), vec3d(1, 1, 0), vec3d(1, 1, 1)],
    [vec3d(1, 0, 0), vec3d(1, 1, 1), vec3d(1, 0, 1)]],
    [[vec3d(1, 0, 1), vec3d(1, 1, 1), vec3d(0, 1, 1)],
    [vec3d(1, 0, 1), vec3d(0, 1, 1), vec3d(0, 0, 1)]],
    [[vec3d(0, 0, 1), vec3d(0, 1, 1), vec3d(0, 1, 0)],
    [vec3d(0, 0, 1), vec3d(0, 1, 0), vec3d(0, 0, 0)]],
    [[vec3d(0, 1, 0), vec3d(0, 1, 1), vec3d(1, 1, 1)],
    [vec3d(0, 1, 0), vec3d(1, 1, 1), vec3d(1, 1, 0)]],
    [[vec3d(1, 0, 1), vec3d(0, 0, 1), vec3d(0, 0, 0)],
    [vec3d(1, 0, 1), vec3d(0, 0, 0), vec3d(1, 0, 0)]]]
}
"""
"""
Cube = {
    "Cube" : [[Triangle(vec3d(0, 0, 0), vec3d(0, 1, 0), vec3d(1, 1, 0))],
    [Triangle(vec3d(0, 0, 0), vec3d(1, 1, 0), vec3d(1, 0, 0))],
    [Triangle(vec3d(1, 0, 0), vec3d(1, 1, 0), vec3d(1, 1, 1))],
    [Triangle(vec3d(1, 0, 0), vec3d(1, 1, 1), vec3d(1, 0, 1))],
    [Triangle(vec3d(1, 0, 1), vec3d(1, 1, 1), vec3d(0, 1, 1))],
    [Triangle(vec3d(1, 0, 1), vec3d(0, 1, 1), vec3d(0, 0, 1))],
    [Triangle(vec3d(0, 0, 1), vec3d(0, 1, 1), vec3d(0, 1, 0))],
    [Triangle(vec3d(0, 0, 1), vec3d(0, 1, 0), vec3d(0, 0, 0))],
    [Triangle(vec3d(0, 1, 0), vec3d(0, 1, 1), vec3d(1, 1, 1))],
    [Triangle(vec3d(0, 1, 0), vec3d(1, 1, 1), vec3d(1, 1, 0))],
    [Triangle(vec3d(1, 0, 1), vec3d(0, 0, 1), vec3d(0, 0, 0))],
    [Triangle(vec3d(1, 0, 1), vec3d(0, 0, 0), vec3d(1, 0, 0))]]
}

Cube2 = MeshObject(Cube, 'Cube')
"""

"""
MeshCube = {
    "South" : [(vec3d(0, 0, 0), vec3d(0, 1, 0), vec3d(1, 1, 0)),
    (vec3d(0, 0, 0), vec3d(1, 1, 0), vec3d(1, 0, 0))],
    "East" : [(vec3d(1, 0, 0), vec3d(1, 1, 0), vec3d(1, 1, 1)),
    (vec3d(1, 0, 0), vec3d(1, 1, 1), vec3d(1, 0, 1))],
    "North": [(vec3d(1, 0, 1), vec3d(1, 1, 1), vec3d(0, 1, 1)),
    (vec3d(1, 0, 1), vec3d(0, 1, 1), vec3d(0, 0, 1))],
    "West" : [(vec3d(0, 0, 1), vec3d(0, 1, 1), vec3d(0, 1, 0)),
    (vec3d(0, 0, 1), vec3d(0, 1, 0), vec3d(0, 0, 0))],
    "Top" : [(vec3d(0, 1, 0), vec3d(0, 1, 1), vec3d(1, 1, 1)),
    (vec3d(0, 1, 0), vec3d(1, 1, 1), vec3d(1, 1, 0))],
    "Bottom" : [(vec3d(1, 0, 1), vec3d(0, 0, 1), vec3d(0, 0, 0)),
    (vec3d(1, 0, 1), vec3d(0, 0, 0), vec3d(1, 0, 0))]
}
"""
