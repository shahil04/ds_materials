# -*- coding: utf-8 -*-

# Import library numpy
import numpy as np #2005 by Travis Oliphant

# check the version
np.__version__

print(np.__doc__)

#Why numpy
#-mathematical function
#Faster

l = [1, 2, 3, 4, 5]

arr = np.array(l)

arr

type(np.array(l))

type(np.array(l))

arr.ndim

l = [1, 2, 3, 4, 5, "Rishi"]
arr1 = np.array(l)
arr1

arr.ndim

arr

arr1 = np.array([[1, 2, 3], [4, 5, 6]])

arr1

arr1.ndim

l = [1, 2, 3, 4]

np.array(l)

mat = np.matrix(l) #matris will be by default 2d

np.matrix([[[1, 2], [5, 6], [7, 8]]])

np.array([[[1, 2], [5, 6], [7, 8]]])

#more way to convert to array
np.asarray([[[1, 2], [5, 6], [7, 8]]])

np.asanyarray([[[1, 2], [5, 6], [7, 8]]]) #Convert the input to an ndarray, but pass ndarray subclasses through.

mat

np.asanyarray(mat)

np.asarray([[[1, 2], [5, 6], [7, 8]]])

np.array([[[1, 2], [5, 6], [7, 8]]])

t = ([1, 2, 3], [4, 5, 6])
type(t)

np.array(t)

a = 5
np.array(a)

l = [1, 2, 3, 4, 5]
arr = np.array(l)
arr

a = arr

a

arr[0] = 1000

arr

a

a

b = a.copy()
b[0] = 2000

b

a

#to create array >> .array, .asasrray, .asanyarray, deep copy, shallow copy

#There are multiple ways to generating arrays

np.fromfunction(lambda i, j : i==j, (3, 3))

arr

arr.shape

arr1

arr1.shape

arr.size

arr1.size

np.fromfunction(lambda i, j : i==j, (3, 3))

np.fromfunction(lambda i, j : i*j, (3, 3))

for i in range(5):
    print(i)

[i for i in range(5)]

list(i for i in range(5))

list(range(5))

iterable = (i*i for i in range(5))

np.fromiter(iterable, int)

np.fromstring('23 34 67', sep = ' ')

np.fromstring('23,34,67', sep = ',')

np.fromstring('Suhani,Ajay,Anwesha', sep = ',')

arr

arr.size

arr.shape

arr.dtype

l = [1, 2,3, "Ajay"]
arr = np.array(l)
arr.dtype

arr

list(range(5))

range(5)

list(range(1.0, 2.10))

list(np.arange(0.1, 10.2, 0.1))

np.linspace(1, 5, 10)

np.logspace(1, 5, 10, base = 2)

np.logspace(1, 5, 10, base = 10)

arr1 = np.zeros(5)
arr1.shape

arr1

arr1.ndim

arr2 = np.zeros((3, 4))
arr2.shape

arr2

arr2.ndim

arr3 = np.zeros((1, 3, 4))
arr3.shape

arr3.ndim

arr4 = np.zeros((1, 1, 3, 4))
arr4.shape

arr4.ndim

arr4

np.ones(5)

arr = np.ones((3,4))

arr

arr+5

arr * 3

np.array([[[[[[[[[[[[[[1, 1, 1, 1, ,1 ]]]]]]]]]]]]]])

np.twos((2,3))

l = [1, 2,3, 4,5, "Prince"]
arr = np.array(l)
arr.dtype

arr





