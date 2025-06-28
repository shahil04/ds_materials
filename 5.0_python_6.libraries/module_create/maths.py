def add(a, b):
    return a + b


def mul(a,b):
    return a * b


def finc(n):
  num1 = 0
  num2 =1 
  print(num1,end=" ")
  print(num2 ,end=" ")
  for i in range(n):
    next = num1+num2
    print(next, end=" ")
    num1 = num2
    num2 =next
