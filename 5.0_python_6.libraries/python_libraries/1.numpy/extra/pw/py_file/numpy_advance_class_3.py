
import numpy as np
arr = np.ones((3, 4))

arr

arr + 5

arr*5

np.empty((3, 4))

np.eye(3, dtype = int) #n*n matrix #tO calculate inverse of matroix

arr

#optional

import pandas as pd
pd.DataFrame(arr)

#extra topics
import random
random.choice((1, 2, 3, 4, 5, 6))

random.choice('Ajay')
random.randrange(1, 10)
random.random() # a random no is generated between o (included), 1 will be excluded

lis = [1, 2, 3, 4, 5]
random.shuffle(lis)

random.uniform(7, 14) #a no between 7 and 14

np.array([])

np.random.random_sample()

type(np.random.random_sample())

np.random.random_sample((5,))

np.random.rand(1)

np.random.rand(2, 3)

np.random.randn(2, 3)

np.random.random_sample()

np.random.randint(1, 5, size = (3, 4))

arr = np.random.randint(1, 5, size = (3, 4))

arr

arr.size

arr.shape

arr.ndim

arr

arr.reshape(2, 6) #array size can not change, multiples of array size

arr.reshape(6, 2)

arr.reshape(12,)

arr.reshape(12, 1)

arr.reshape(12,2)

arr.reshape(4, 3)

arr.reshape(3,4)

arr

arr.reshape(4, -1)

arr.reshape(4, -100)

arr.reshape(3, -100)

arr.reshape(-1, 4)

arr

arr.reshape(12, ).base

arr

arr.size

arr.reshape(2, 2, 3)

arr.reshape(1, 2, 2, 3)

arr.reshape(4, 3, 1)

arr.reshape(1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3)

lis = [1, 2, 3, 4]
arr = np.array(lis)

arr

arr.ndim

arr2 = np.array([[2, 3], [4, 5]])
arr2

arr2.ndim

arr2 = np.zeros((3, 4))
arr2

arr2.ndim

arr3 = np.zeros((1, 3, 4)) # 3 rows, 4 columns >> 2d array + 1d
arr3

arr3.ndim

arr3.shape

arr4 = np.zeros((1, 1, 3, 4)) # 3 rows, 4 columns >> 2d array + 1d +1d
arr4

arr4.ndim

arr4.shape

arr3 = np.zeros((3, 3, 4))
arr3

arr3.ndim

arr3.shape

arr1 = np.random.randint(1, 10, (5, 6))

arr1

arr1 > 5

arr1[arr1 > 5]

arr1[arr1 < 5]

arr1

arr

arr[0]

arr[0]

arr1

arr1[0:2, [0,2]] #0th - 1st row in continuation and 0th and 2nd column

#slicing on both rows and column
arr1[0:2, 1:3]

arr1[0:2, [0, 1]]

arr

arr1[0, [1,3]]

arr1[2:4, [0, 2]]

arr1

arr1[2:5]

arr1[2:5, 0:2] #slicing

arr1[2:5, [0, 2]]

arr1[[2,4]]

arr1

arr1

arr1[[2, 4]] #selecting specific column

arr1[2 : 4] #slicing

arr1

arr1[2:4, [1, 3]]

arr1 = np.random.randint(1, 3, (3,3))
arr2 = np.random.randint(1, 3, (3,3))

arr1

"""##"""

arr2

arr1 + arr2

arr1 - arr2

arr1 * arr2

#matrix multiplication


arr1

arr2

arr1 @ arr2

arr1

arr2

arr1 / arr2 #index wise divison

arr1

arr1 / 0

#Broad casting

arr = np.zeros((3, 4))

arr

arr + 5

arr

a = np.array([1, 2, 3, 4])

a.shape

a

arr + a

arr

a

a = np.array([1, 2, 3])

a = np.array([[1, 2, 3]])

a.T

arr

a

arr + a.T

a.T

a = np.array([1, 2, 3])
a.T

arr1

np.sqrt(arr1)

np.log10(arr1)

np.exp(arr1)

a

np.min(a)

arr1

np.min(arr1)

np.max(arr1)

arr1

arr1.T

arr1.flatten() #reduce higher dimension to 1 d

#expand_dims >>  expands the array by inserting a new axis

arr = np.array([[1, 2, 3], [4, 5, 6], [1, 2, 3]])

arr

np.sum(arr)

np.sum(arr, axis = 0)

np.sum(arr, axis = 1)

#expand_dims >>expand the dimension of array
arr = np.array([1, 2, 3, 4])
arr

arr.ndim

arr1 = np.expand_dims(arr, axis = 0)
arr1

arr1.ndim

arr2 = np.expand_dims(arr1, axis = 0)
arr2

arr2.shape

arr

arr1 = np.expand_dims(arr, axis = 1)
arr1

arr = np.zeros((3, 4))

arr

arr1 = np.expand_dims(arr, axis = 1)
arr1

arr1 = np.expand_dims(arr, axis = 0)
arr1

