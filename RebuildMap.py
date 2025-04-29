"""
Josep Peiró Ramos
https://github.com/JosepPeiro/Rebuild-Mapping-with-Distances

RebuildMap.py
In this algorithm we aim to reconstruct a set of points in a 2D space based on a distance matrix.
As there are several ways to embed points in a an space given their distances, this algorithm can
guarantee a deterministic and exact method to project the points in a 2D space.
Even though, the orientation and direction of the space may change, the distances between the points
will remain the same, so the main goal is achieved.

The distances must be euclidean.
The format needed for the distance is a square symetric matrix, or at least a superior triangular matrix,
where the first diagonal must be all 0s, and the rest of the matrix must be distances between the points.

We permit to see the result generated in a plot.
Also it is possible to generate random points, and then reconstruct them. For that it is needed to set
matrix parameter as None.
In this case we can force to maintain the orientation of the points, so the first three points are
always (0,0), (4,0), and (3,2).
Also, if we generate random points, we can set the number of points to generate with n_points parameter.

There is an explanation of how to use the algorithm in the UseExample.py file.
"""

import matplotlib.pyplot as plt
import random

def RebuildPoints(matrix = None, n_points = 10, maintain_orientation = False, show = False):
    """
    Rebuild 2D coordinates of a set of points given the distances between them.

    Parameters:
        matrix: List of list:          Square symmetric matrix with the distances between points.
                                       If None, random points will be generated.
        n_points: Integer:             Number of points to generate if matrix is None.
        maintain_orientation: Boolean: If True, and matrix is None, when generating random
                                       points we will constrint the first so it's possible to
                                       recover the original orientation.
        show: Boolean:                 If True, the function will show the reconstructed points.
                                       If matrix is None, the function will show both the random
                                       points and the reconstructed ones.
    
    Returns:
        points: List of tuples:       List of tuples with the reconstructed points.
        matrix: List of list:         Distances between original points.
        deviation: Float:             Average distance deviation between the original and reconstructed points.
        dots_list: List of tuples:    List of tuples with the generated random points if we generate random points.
                                      Otherwise, it will be empty.
    """
    
    gen_tpl = set() # Storage unique points
    if matrix is None: # If no matrix is provided, generate random points
        if maintain_orientation:
            gen_tpl = set([(0,0), (4,0), (3,2)]) # Necessary points for maintaining orientation and direction
        
        while len(gen_tpl) < n_points: # Create n_points random different points
            tpl = (random.uniform(-100, 100), random.uniform(-100, 100)) # 2D uniform distribution
            gen_tpl.add(tpl)

        dots_list = list(gen_tpl) # Convert to list for matrix calculation

        if maintain_orientation: # If we need to maintain orientation, we need to set the first three points
            dots_list.remove((0,0))
            dots_list.insert(0, (0,0))

            dots_list.remove((4,0))
            dots_list.insert(1, (4,0))

            dots_list.remove((3,2))
            dots_list.insert(2, (3,2))

        matrix = CalculateDistances(dots_list) # Create distance matrix from the points

    # The firsts distances are needed as parameters to reconstruct points
    n = round(matrix[0][1], 12) # Distance between the first two points
    alpha = round(matrix[0][2]**2, 12) # Distance between the first and third points
    beta = round(matrix[1][2]**2, 12)  # Distance between the second and third points

    s = (alpha - ((n ** 2 + alpha - beta) / (2 * n)) ** 2) ** 0.5 # Calculate a provisional y coordinate
    r = (alpha - s ** 2) ** 0.5 # Calculate a provisional x coordinate

    # Set all initial points in the first quadrant (all coordinates positive)
    # Although this may change orientation
    l, m = round(abs(r), 12), round(abs(s), 12)
    points = [(0,0), (n, 0), (l, m)] # They will be the reference from now on

    for point in range(3, len(matrix)): # Iterate over the rest of the points with the same method as before
        alpha = round(matrix[0][point]**2, 6)
        beta = round(matrix[1][point]**2, 6)
        gamma = round(matrix[2][point]**2, 2)

        s = (alpha - ((n ** 2 + alpha - beta) / (2 * n)) ** 2) ** 0.5
        r = (alpha - s ** 2) ** 0.5

        # Check all combinations of signs
        # As, with the previous results we get square roots, but they can be negative
        for comb in ((r,s), (r,-s), (-r,s), (-r,-s)):
            calc_gamma = (comb[0] - l) ** 2 + (comb[1] - m) ** 2
            if isinstance(calc_gamma, float) and round(calc_gamma, 2) == gamma: # The combination that matches with the third point
                points.append(comb)
                break

    if show: # If we want to show the results
        if len(gen_tpl): # If we generated random points
            # Convert 2D tuples into 2 lists
            # One for the original points and one for the reconstructed points
            x_coords = [tpl[0] for tpl in gen_tpl]
            y_coords = [tpl[1] for tpl in gen_tpl]

            x_coords_rec = [recons[0] for recons in points]
            y_coords_rec = [recons[1] for recons in points]

            # Show the two plots together
            _, ax = plt.subplots(1,2, figsize=(12, 6))
            ax[0].scatter(x_coords, y_coords, marker='o', color='blue')
            ax[1].scatter(x_coords_rec, y_coords_rec, marker='o', color='red')

            ax[0].set_title("Random Points")
            ax[0].grid(True)
            ax[1].set_title("Reconstructed Points")

        else: # If we have a matrix of distances
            # We can only show reconstructed points
            x_coords = [tpl[0] for tpl in points]
            y_coords = [tpl[1] for tpl in points]

            plt.figure(figsize=(8, 6))
            plt.scatter(x_coords, y_coords, marker='o', color='red')
            plt.title("Reconstructed points")

        plt.grid(True)
        plt.show()
    
    if len(gen_tpl):# If we generated random points
        # Return reconstructed points, matrix of distances, deviation from original to reconstructed and generated points
        return points, matrix, DeviationRemap(CalculateDistances(points), matrix), dots_list
    # Return reconstructed points, matrix of distances, deviation from original to reconstructed
    return points, matrix, DeviationRemap(CalculateDistances(points), matrix), None


def DeviationRemap(mat1, mat2):
    """
    Calculate the deviation between two matrices of distances.
    I.e. the average of the absolute differences between the distances of the two matrices.
    """
    a, b = 0, 0
    for i in range(len(mat1)):
        for j in range(len(mat1[i])):
            a += abs(mat1[i][j] - mat2[i][j])
            b += 1
    return a / b


def CalculateDistances(lpoints):
    """
    Calculate the distance matrix between a list of 2D points.
    """
    matrix = []
    for i in lpoints:
        ref = []
        for j in lpoints:
            dd = ((i[0] - j[0])**2 + (i[1] - j[1])**2) ** 0.5
            ref.append(dd)
        matrix.append(ref)
    return matrix


def GenerateMatrix(n_points = 1000):
    """
    Generate a random distance matrix of n_points.
    """
    gen_tpl = set()
    while len(gen_tpl) < n_points:
        gen_tpl.add((random.uniform(-100, 100), random.uniform(-100, 100)))
    matrix = CalculateDistances(list(gen_tpl))
    return matrix


def WriteMatrix(matrix, filename):
    """
    Write a distance matrix to a txt file.
    The format is a tab separated file, with the distances between points.
    The same format as the one needed by ReadMatrix function.
    """
    with open(filename, "w") as f:
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                f.write(f"{matrix[i][j]}")
                if j == len(matrix[i]) - 1:
                    f.write("\n")
                else:
                    f.write("\t")


def ReadMatrix(filename):
    """
    Read a distance matrix from a txt file.
    The same format as the one generated by WriteMatrix function.
    """
    matrix = []
    try:
        with open(filename, "r") as f:
            return [list(map(float, line.strip().split('\t'))) for line in f if line.strip()]
    except:
        print(f"Error: File '{filename}' not found.")
    return matrix