
import numpy as np
data = np.array([[1], [2], [3]])

data.ndim

data

a=np.squeeze(data)

a

a.ndim

#repeat
data

np.repeat(data, 4)

a = np.array([[1, 2], [3, 4]])

a

np.repeat(a, 2)

a

np.repeat(a, 2, axis = 1)

np.repeat(a, 2, axis = 0)

data

np.roll(data, -2)

np.diag(np.array([1, 2, 3, 4]))

a = np.array([[[1, 2], [3, 4], [5,6]]])

a

np.roll(a, 2, axis = 0)

#binary operation on array

arr1 = np.random.randint(1, 10, (3, 4))
arr2 = np.random.randint(1, 10, (3, 4))

arr1

arr2

arr1+arr2

arr1*arr2

arr1 / arr2

arr1 - arr2

arr1 ** arr2

arr1

arr2

arr1 > arr2

~arr1

arr1

#Numpy string function

arr = np.array(["pw", "skills"])

arr

np.char.upper(arr)

np.char.upper(np.array(["Ajay"]))

np.char.capitalize(arr)

np.char.title(arr)

#Mathematical function
arr1

np.sin(arr1)

np.cos(arr1)

np.tan(arr1)

np.log10(arr1)

np.exp(arr1)

np.power(arr1, 3)

np.mean(arr1)

np.max(arr1)

np.std(arr1)

np.var(arr1)

np.max(arr1)

arr1 - arr2

np.subtract(arr1, arr2)

arr1 * arr2

np.multiply(arr1, arr2)

np.mod(arr1, arr2) #return element wise remainder

np.power(arr1, arr2)

np.sqrt(arr1)

#sort search

arr = np.array([5, 6, 1, 2])

arr

np.sort(arr)

arr = np.array([5, 6,100, 200, 1, 2, 8, 9])

# a = np.sort(arr)

arr

np.sort(arr)

np.searchsorted(arr, 3)



np.searchsorted(arr, 3)

arr1 = np.array([0, 1, 2, 3, 0, 4])
np.count_nonzero(arr1)

arr1 > 0

arr1

np.where(arr1 > 0)

np.extract(arr1 > 0, arr1)

arr1.byteswap()

#matrix >> 2d array

import numpy.matlib as nm

nm.zeros(5)

nm.ones((3, 4))

#Numpy linear algebra

arr1

arr1 = np.random.randint(1, 10, (3, 4))
arr2 = np.random.randint(1, 10, (3, 4))

arr1 = np.array([[2, 3], [4, 5]])
arr2 = np.array([[1, 3], [4, 5]])

arr1 @ arr2

a  = np.array([[7, 5.3, -3], [3, -5, 2], [5, 3, -7]])

a

b = np.array([16, -8, 0])

b

np.linalg.solve(a, b)

arr1

5*2 - 3*4

np.linalg.det(arr1)

np.linalg.inv(arr1)

