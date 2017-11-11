import numpy as np

array = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int16)
print(np.zeros((3, 3), dtype=np.int))
print(np.arange(10, 20, 2))
print(np.arange(12).reshape(3, 4))
print(np.linspace(1, 10, 5, dtype=int))
print(array)
print(array.dtype)
print(array.ndim)
print(array.shape)
print(array.size)

a = np.array([[10, 20, 30, 40], [1, 2, 3, 4]])
b = np.arange(8).reshape(2, 4)
c = a-b
d = a+b
print(c)
print(d)
print(b**2)
print(np.sin(a)*10)
print(b < 4)
a = np.array([[1, 2], [3, 4]])
b = np.arange(4).reshape(2, 2)
print(np.dot(a, b))
print(a.dot(b))
a = np.random.random((2, 4))
print(a)
print(a.sum(axis=1))
print(a.min(axis=0))


