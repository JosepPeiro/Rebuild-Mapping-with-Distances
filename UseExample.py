"""
Josep Peiró Ramos

This is an example of how to use the RebuildMap algorithm.
The algorithm is designed to reconstruct a set of points in a 2D space based on a distance matrix.
"""

from RebuildMap import RebuildPoints, GenerateMatrix, WriteMatrix, ReadMatrix

p, m, d, l  = RebuildPoints()

print("The reconstructed coordinates according to the algorithm:")
print(p)

print("\nThe matrix of distances:")
print(m)

print("\nThe average deviation from the original distances to the ones calculated by the algorithm:")
print(d)

print("\nThe original coordinates, as they were randomly created:")
# This option is returned only if we don't give a matrix in the "matrix" parameter.
print(l)

# Here we add the option to see the graph of the points reconstructed by the algorithm next to the original points, created randomly.
# The reconstruction may appear different, but the distances are identical, even though the direction or orientation may be different.
# The algorithm is not designed to maintain the orientation of the points, but only the distances.
p, m, d, l  = RebuildPoints(show=True)

# Here we add the option of maintaining the orientation of the points, so that the first three points are always (0,0), (4,0), and (3,2).
# But the rest of the points are still randomly generated.
# And the reconstruction is identical, also in terms of orientation and directions, (and of course distances).
p, m, d, l  = RebuildPoints(show=True, maintain_orientation=True)

# Here we determine to create 1000 points instead of 10 (default value), and the algorithm will maintain the orientation of the points.
# We can specify any number of points.
# Take into account the running time is highly non lineal: O(n^2).
p, m, d, l  = RebuildPoints(show=True, maintain_orientation=True, n_points=1000)

# And here we determine a concrete matrix of distances, which is the one we want to reconstruct.
# The matrix should be a sqare matrix or at least superior triangular matrix.
# There are examples of how the structure of the matrix should be in the EXAMPLES folder.
# Although we are still creating a random matrix with GenerateMatrix function.
p, m, d  = RebuildPoints(show=True, matrix=GenerateMatrix(1000))
# In this case, the parameters "maintain_orientation" and "n_points" are not used, since we are giving a matrix to the algorithm.

# We can storage the matrix in a file, so we can use it later.
filewrite = "UseCase.txt"
WriteMatrix(m, filewrite)

# And we can read the matrix from a file, so we can use it later.
matrix_read = ReadMatrix(filewrite)
p, m, d  = RebuildPoints(show=True, matrix=matrix_read)
# The result is identical as before, since they are the same distance matrix.