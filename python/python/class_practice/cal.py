
num1 = float(input("Enter the 1st number "))
num2 = float(input("Enter the 2nd number "))

print("option 1. for Add")
print("option 2. for Sub")
print("option 3. for Mul")
print("option 4. for Div")

opt = int(input("Choose the option "))

if(opt==1):
    print("Addition of 2 number is ", num1 + num2)
elif(opt==2):
    print("subtraction of 2 number is ", num1 - num2)
elif(opt==3):
    print("Multiplication of 2 number is ", num1 * num2)   
elif(opt==4):
    print("divide of 2 number is ", num1 / num2)
else:
    print("Choose a valid option")

