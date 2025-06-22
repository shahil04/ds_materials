cart={}

# add
def add_to_cart():
  product= input("enter the product name:  ")
  quantity = int(input("enter the quantity:  "))

  cart[product]=quantity
  cart

# update the cart value
def update_cart():
  product= input("enter the product name which you want to update: ")
  quantity = int(input("enter the new  quantity: "))
  cart[product]=quantity
 

# Delete the product
def delete_product():
  product= input("enter the product name which you want to delete: ")
  print(cart.keys())
  if product in cart.keys():
    cart.pop(product)
  else:
    print("product not found ")
  cart



def main():
    flag = True
    while flag:
        print()
        print("===========================")
        print("press 1 .to add product")
        print("press 2 .to update product")
        print("press 3 .to delete product")
        print("press 4 .to show cart")
        print("press 5 .to exit")
        print("==========================")

        user_choice = int(input("enter your choice:  "))
        if user_choice ==1:
            add_to_cart()

        elif user_choice ==2:
            update_cart()

        elif user_choice ==3:
            delete_product()

        elif user_choice ==4:
            print(cart)

        else:
            flag =False
            print("buy successfully ")
            print("exit")


main()