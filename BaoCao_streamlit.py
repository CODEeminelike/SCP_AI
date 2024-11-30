import streamlit as st
import numpy as np
import cv2

def build_adjacency_matrix(constraints, names):
    n = len(names)
    matrix = np.zeros((n, n), dtype=int)
    for (region1, region2), _ in constraints:
        index1 = names.index(region1)
        index2 = names.index(region2)
        matrix[index1][index2] = 1
        matrix[index2][index1] = 1
    return matrix

class Region:
    def __init__(self, degree, color):
        self.degree = degree
        self.color = -1
        self.neighbourRegion = []
        self.numberOfPossibleColors = len(color)
        self.possibleColors = [True] * self.numberOfPossibleColors
        self.changed = []

    def setColor(self, color):
        if not self.possibleColors[color]:
            return False
        self.color = color
        for i in self.neighbourRegion:
            if i not in visitedRegion:
                if listOfRegion[i].possibleColors[color]:
                    listOfRegion[i].possibleColors[color] = False
                    listOfRegion[i].numberOfPossibleColors -= 1
                    self.changed.append(i)
        return True

    def restore(self, color):
        for i in self.changed:
            listOfRegion[i].possibleColors[color] = True
            listOfRegion[i].numberOfPossibleColors += 1
        self.changed.clear()
        self.color = -1

    def addNeighbourRegion(self, l):
        self.neighbourRegion.append(l)

    def __lt__(self, other):
        if self.numberOfPossibleColors > other.numberOfPossibleColors:
            return True
        elif self.numberOfPossibleColors == other.numberOfPossibleColors:
            if self.degree < other.degree:
                return True
        return False

def setRegion():
    length = len(matrix)
    for i in range(length):
        listOfRegion.append(Region(np.sum(matrix[i]), colors))
        for j in range(length):
            if matrix[i][j] == 1:
                listOfRegion[i].addNeighbourRegion(j)

def checkConstrain(x, color):
    for i in listOfRegion[x].neighbourRegion:
        if color == listOfRegion[i].color:
            return False
    return True

def findNextRegion():
    flag = True
    nextRegion = -1
    for x in range(len(listOfRegion)):
        if x not in visitedRegion:
            if flag:
                nextRegion = x
                flag = False
            else:
                if listOfRegion[nextRegion] < listOfRegion[x]:
                    nextRegion = x
    return nextRegion

def mrv(x):
    if x == -1:
        for i in range(len(listOfRegion)):
            ans.append(listOfRegion[i].color)
        return True

    for color in range(len(colors)):
        if checkConstrain(x, color):
            if listOfRegion[x].setColor(color):
                visitedRegion.add(x)
                y = findNextRegion()
                if mrv(y):
                    return True
                visitedRegion.remove(x)
                listOfRegion[x].restore(color)

    return False

def run_mrv(_matrix, _colors):
    global matrix, colors, listOfRegion, visitedRegion, ans
    matrix = _matrix
    colors = _colors
    listOfRegion = []
    visitedRegion = set()
    ans = []
    setRegion()
    x = findNextRegion()
    if not mrv(x):
        return [0] * len(matrix)
    return ans

names = ['Bayern', 'Baden', 'Rheinland', 'Saarland', 'Hessen', 'Thuringen', 'Sachsen', 'Brandenburg', 'Berlin', 
          'SachsenAnhalt', 'Niedersachsen', 'NordrheinWestfalen', 'SchleswigHolstein', 'MecklenburgVorpommern', 
          'Hamburg', 'Bremen']

 # Tọa độ trung tâm của từng vùng trên ảnh (sử dụng để tô màu)
names_point = [(769, 778), (532, 761), (404, 616), (374, 674), (542, 536), (701, 516), (872, 494), (826, 265), 
                (881, 312), (747, 372), (587, 308), (445, 432), (622, 116), (799, 160), (627, 193), (550, 251)]

constraints = [
    (('Bayern', 'Baden'), None),
    (('Bayern', 'Hessen'), None),
    (('Bayern', 'Thuringen'), None),
    (('Bayern', 'Sachsen'), None),
    (('Baden', 'Hessen'), None),
    (('Baden', 'Rheinland'), None),
    (('Baden', 'Bayern'), None),
    (('Rheinland', 'Saarland'), None),
    (('Rheinland', 'Hessen'), None),
    (('Rheinland', 'NordrheinWestfalen'), None),
    (('Rheinland', 'Baden'), None),
    (('Saarland', 'Rheinland'), None),
    (('Hessen', 'Baden'), None),
    (('Hessen', 'Rheinland'), None),
    (('Hessen', 'Thuringen'), None),
    (('Hessen', 'NordrheinWestfalen'), None),
    (('Hessen', 'Niedersachsen'), None),
    (('Hessen', 'Bayern'), None),
    (('Thuringen', 'Bayern'), None),
    (('Thuringen', 'Hessen'), None),
    (('Thuringen', 'Sachsen'), None),
    (('Thuringen', 'SachsenAnhalt'), None),
    (('Thuringen', 'Niedersachsen'), None),
    (('Sachsen', 'Bayern'), None),
    (('Sachsen', 'Thuringen'), None),
    (('Sachsen', 'SachsenAnhalt'), None),
    (('Sachsen', 'Brandenburg'), None),
    (('Brandenburg', 'Sachsen'), None),
    (('Brandenburg', 'SachsenAnhalt'), None),
    (('Brandenburg', 'Niedersachsen'), None),
    (('Brandenburg', 'MecklenburgVorpommern'), None),
    (('Brandenburg', 'Berlin'), None),
    (('Berlin', 'Brandenburg'), None),
    (('SachsenAnhalt', 'Sachsen'), None),
    (('SachsenAnhalt', 'Thuringen'), None),
    (('SachsenAnhalt', 'Brandenburg'), None),
    (('SachsenAnhalt', 'Niedersachsen'), None),
    (('Niedersachsen', 'Hessen'), None),
    (('Niedersachsen', 'Thuringen'), None),
    (('Niedersachsen', 'SachsenAnhalt'), None),
    (('Niedersachsen', 'Brandenburg'), None),
    (('Niedersachsen', 'MecklenburgVorpommern'), None),  
    (('Niedersachsen', 'NordrheinWestfalen'), None),
    (('Niedersachsen', 'SchleswigHolstein'), None),
    (('Niedersachsen', 'Hamburg'), None),
    (('Niedersachsen', 'Bremen'), None),
    (('NordrheinWestfalen', 'Rheinland'), None),
    (('NordrheinWestfalen', 'Hessen'), None),
    (('NordrheinWestfalen', 'Niedersachsen'), None),
    (('SchleswigHolstein', 'Niedersachsen'), None),
    (('SchleswigHolstein', 'Hamburg'), None),
    (('SchleswigHolstein', 'MecklenburgVorpommern'), None),
    (('Hamburg', 'Niedersachsen'), None),
    (('Hamburg', 'SchleswigHolstein'), None),
    (('MecklenburgVorpommern', 'Brandenburg'), None),
    (('MecklenburgVorpommern', 'SchleswigHolstein'), None),
    (('MecklenburgVorpommern', 'Hamburg'), None),
    (('MecklenburgVorpommern', 'Niedersachsen'), None),  
]



matrix = build_adjacency_matrix(constraints, names)
colors = ['red', 'green', 'blue', 'gray']

st.title("Map Coloring with MRV Algorithm")
uploaded_image = st.file_uploader("Upload your map image (in grayscale)", type=["jpg", "png"])
if uploaded_image is not None:
    image = cv2.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    st.image(image, caption="Uploaded Map", use_container_width=True)

if st.button("Run MRV Algorithm"):
    solution = run_mrv(matrix, colors)
    st.write("### Color Mapping:")
    for i, color in enumerate(solution):
        st.write(f"{names[i]} => {colors[color]}")

    # Tô màu trên ảnh
    image_colored = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    mask = np.zeros((image.shape[0] + 2, image.shape[1] + 2), np.uint8)
    color_map = {'red': (0, 0, 255), 'green': (0, 255, 0), 'blue': (255, 0, 0), 'gray': (128, 128, 128)}

    for i, color in enumerate(solution):
        point = names_point[i]
        cv2.floodFill(image_colored, mask, point, color_map[colors[color]])

    st.image(image_colored, caption="Colored Map", use_container_width=True)
