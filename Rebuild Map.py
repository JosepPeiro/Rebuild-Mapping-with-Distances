import matplotlib.pyplot as plt
import random

def RebuildPoints(matrix = None, n_points = 1000, maintain_orientation = False, show = False, deviation = False):
    
    gen_tpl = set()
    if matrix is None:
        if maintain_orientation:
            gen_tpl = set([(0,0), (4,0), (3,2)])
        
        while len(gen_tpl) < n_points:
            tpl = (random.uniform(-100, 100), random.uniform(-100, 100))
            gen_tpl.add(tpl)

        dots_list = list(gen_tpl)

        if maintain_orientation:
            dots_list.remove((0,0))
            dots_list.insert(0, (0,0))

            dots_list.remove((4,0))
            dots_list.insert(1, (4,0))

            dots_list.remove((3,2))
            dots_list.insert(2, (3,2))

        matrix = CalculateDistances(dots_list)

    n = round(matrix[0][1], 12)
    alpha = round(matrix[0][2]**2, 12)
    beta = round(matrix[1][2]**2, 12)

    s = (alpha - ((n ** 2 + alpha - beta) / (2 * n)) ** 2) ** 0.5
    r = (alpha - s ** 2) ** 0.5

    l, m = round(abs(r), 12), round(abs(s), 12)

    points = [(0,0), (n, 0), (l, m)]

    for point in range(3, len(matrix)):
        alpha = round(matrix[0][point]**2, 6)
        beta = round(matrix[1][point]**2, 6)
        gamma = round(matrix[2][point]**2, 2)

        s = (alpha - ((n ** 2 + alpha - beta) / (2 * n)) ** 2) ** 0.5
        r = (alpha - s ** 2) ** 0.5

        for comb in ((r,s), (r,-s), (-r,s), (-r,-s)):
            calc_gamma = (comb[0] - l) ** 2 + (comb[1] - m) ** 2
            if isinstance(calc_gamma, float) and round(calc_gamma, 2) == gamma:
                points.append(comb)
                break

    if show:
        if len(gen_tpl):
            x_coords = [tpl[0] for tpl in gen_tpl]
            y_coords = [tpl[1] for tpl in gen_tpl]

            x_coords_rec = [recons[0] for recons in points]
            y_coords_rec = [recons[1] for recons in points]

            _, ax = plt.subplots(1,2, figsize=(12, 6))
            ax[0].scatter(x_coords, y_coords, marker='o', color='blue')
            ax[1].scatter(x_coords_rec, y_coords_rec, marker='o', color='red')

            ax[0].set_title("Random Points")
            ax[0].grid(True)
            ax[1].set_title("Reconstructed Points")

        else:
            x_coords = [tpl[0] for tpl in points]
            y_coords = [tpl[1] for tpl in points]

            plt.figure(figsize=(8, 6))
            plt.scatter(x_coords, y_coords, marker='o', color='red')
            plt.title("Gráfica de Puntos Reconstruidos")

        plt.grid(True)
        plt.show()
    
    if len(gen_tpl):
        return points, matrix, DeviationRemap(CalculateDistances(points), matrix), dots_list
    return points, matrix, DeviationRemap(CalculateDistances(points), matrix)


def DeviationRemap(mat1, mat2):
    a, b = 0, 0
    for i in range(len(mat1)):
        for j in range(len(mat1[i])):
            a += abs(mat1[i][j] - mat2[i][j])
            b += 1
    return a / b


def CalculateDistances(lpoints):
    matrix = []
    for i in lpoints:
        ref = []
        for j in lpoints:
            dd = ((i[0] - j[0])**2 + (i[1] - j[1])**2) ** 0.5
            ref.append(dd)
        matrix.append(ref)
    return matrix


def GenerateMatrix(n_points = 1000):
    gen_tpl = set()
    while len(gen_tpl) < n_points:
        gen_tpl.add((random.uniform(-100, 100), random.uniform(-100, 100)))
    matrix = CalculateDistances(list(gen_tpl))
    return matrix


def WriteMatrix(matrix, filename):
    with open(filename, "w") as f:
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                f.write(f"{matrix[i][j]}")
                if j == len(matrix[i]) - 1:
                    f.write("\n")
                else:
                    f.write("\t")


def ReadMatrix(filename):
    matrix = []
    try:
        with open(filename, "r") as f:
            return [list(map(float, line.strip().split('\t'))) for line in f if line.strip()]
    except:
        print(f"Error: File '{filename}' not found.")
    return matrix