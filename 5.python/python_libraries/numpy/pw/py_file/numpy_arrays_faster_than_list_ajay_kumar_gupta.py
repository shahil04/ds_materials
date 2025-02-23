
For matrices, the dot product represents a more generalized operation. If A is an
m×n matrix and B is an  n×p matrix, the dot product (matrix multiplication) results in an
m×p matrix. In NumPy, this can be computed using the np.dot function or the @ operator for matrix multiplication.

For two vectors, A and B, with elements A[0], A[1], ..., A[n-1] and B[0], B[1], ..., B[n-1], the dot product (also known as the inner product or scalar product) is calculated as follows:

dot product=A[0]×B[0]+A[1]×B[1]+…+A[n−1]×B[n−1]
"""

import numpy as np

# Example matrices
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Using np.dot for matrix multiplication
matrix_product = np.dot(A, B)
print("Matrix product using np.dot:\n", matrix_product)

# Using @ operator for matrix multiplication (Python 3.5 and later)
matrix_product = A @ B
print("Matrix product using @ operator:\n", matrix_product)

import numpy as np
import time

# Generate two random NumPy arrays with one million elements each
array1 = np.random.rand(1000000)
array2 = np.random.rand(1000000)

# Measure time for the vectorized version using np.dot
start_time_vectorized = time.time()
result_vectorized = np.dot(array1, array2)
end_time_vectorized = time.time()

# Print the time taken for the vectorized version
print("Time taken for vectorized calculation: " + str(1000 * (end_time_vectorized - start_time_vectorized)) + " milliseconds")

# Reset result_vectorized to 0
result_vectorized = 0

# Measure time for the version using a for loop
start_time_for_loop = time.time()
for index in range(1000000):
    result_vectorized += array1[index] * array2[index]
end_time_for_loop = time.time()

# Print the time taken for the for loop version
print("Time taken for calculation using a for loop: " + str(1000 * (end_time_for_loop - start_time_for_loop)) + " milliseconds")

np.array(np.matrix([[1, 2], [5, 6]]))

arr = np.array([[1, 2, 3], [4, 5, 6]])

np.count_nonzero(arr)

import numpy as geek

my_scalar = 12

print ("Input  scalar : ", my_scalar)

out_arr = geek.asanyarray(my_scalar)
print ("output array from input scalar : ", out_arr)
print(type(out_arr))

