class Obj(object):
    def __init__(self, filename):
        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        try:
            with open(filename, "r") as file:
                lines = file.read().splitlines()

            for line in lines:
                line = line.rstrip()

                try:
                    prefix, value = line.split(" ", 1)
                except ValueError:
                    continue

                if prefix == "v":
                    try:
                        vert = value.split(" ")
                        vert = [float(coord) for coord in vert]
                        self.vertices.append(vert)
                    except ValueError:
                        print("Advertencia: Se encontró un vértice con valores no numéricos.")
                elif prefix == "vt":
                    try:
                        vts = value.split(" ")
                        vts = [float(coord) for coord in vts]
                        self.texcoords.append([vts[0], vts[1]])
                    except ValueError:
                        print("Advertencia: Se encontró una coordenada de textura con valores no numéricos.")
                elif prefix == "vn":
                    try:
                        norm = value.split(" ")
                        norm = [float(coord) for coord in norm]
                        self.normals.append(norm)
                    except ValueError:
                        print("Advertencia: Se encontró una normal con valores no numéricos.")
                elif prefix == "f":
                    try:
                        face = []
                        verts = value.split(" ")
                        for vert in verts:
                            vert = vert.split("/")
                            face.append([int(i) for i in vert])
                        self.faces.append(face)
                    except ValueError:
                        print("Advertencia: Se encontró una cara con índices no numéricos.")
        except FileNotFoundError:
            print(f"Error: El archivo {filename} no se encontró.")
        except Exception as e:
            print(f"Error inesperado: {e}")
