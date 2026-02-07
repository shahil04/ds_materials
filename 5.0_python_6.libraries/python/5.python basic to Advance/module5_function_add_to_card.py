# To store multiple  product
cart={"product_name":[],"product_quantity":[] }

# Q. write a  program to check item is already in the cart or not.
def add_to_Card1(product_name, product_quantity):
    if product_name not in cart["product_name"]:
        cart["product_name"].append(product_name)
        cart["product_quantity"].append(product_quantity)

        print("Item added Successfully to the cart.",product_name, product_quantity)
        print(cart)
    else:
        print('already in cart')

def remove_item(product_name):
    if product_name in cart["product_name"]:
         index = cart["product_name"].index(product_name)  
         cart["product_name"].pop(index)
         cart["product_quantity"].pop(index)

         print(product_name , " item Discard Successfully ")
         print("Left items :",cart)
    else:
        print(product_name , " item not found in cart ")

# create a functions  to update quantity of product in cart
# update_qantity()
def update_qantity(product_name, new_quantity):
  if product_name in cart["product_name"]:
    print("Previues cart value ",cart )
    a = cart["product_name"].index(product_name)
    cart["product_quantity"][a] = new_quantity

    print("Item updated Successfully to the cart.", product_name,new_quantity)
  else:
    print(product_name , " item not found in cart ")

# show_cart()
def show_cart():
  print(cart)

def remove_all():
    cart["product_name"].clear()
    cart["product_quantity"].clear()
    print("All items removed from cart.")

def buy_now():
    cart["product_name"].clear()
    cart["product_quantity"].clear()
    print("Your order has been placed successfully!")

# 1. add_to_Card()
# 2. update_qantity()
# 3. delete_card_item()
# 4. show_card()
# 5. Buy
# 6. Exit
# create a options Menu
def menu():
  print("Welcome to Flipkart")
  print("====================")
  print("1. add_to_Card()")
  print("2. update_qantity()")
  print("3. delete_card_item()")
  print("4. show_card()")
  print("5. Buy ")
  print("6. Exit")
  print("====================")
  user_input = int(input("enter the option: "))
  
  if user_input ==1:
    n =input("enter the product name ")
    q =input('enter the quantity')
    add_to_Card1(n,q)

  elif user_input ==2:
    n =input("enter the product name ")
    q =input('enter the new quantity')
    update_qantity(n,q)

  elif user_input ==3:
    n =input("enter the product name ")
    remove_item(n)

  elif user_input ==4:
    show_cart()
    
  elif user_input ==5:
    buy_now()

  else:
    print("Invalid option")


# create a options Menu with LOOP
while True:
  menu()
  print("==========================")
  user_input = input("Do you want to continue? (y/n): ")
  if user_input != "y":
    break

# ========================================
# import streamlit as st

# # ======================================
# # PAGE CONFIG
# # ======================================
# st.set_page_config(page_title="Add to Cart System", page_icon="🛒")

# # ======================================
# # SESSION INITIALIZATION
# # ======================================
# if "cart" not in st.session_state:
#     st.session_state.cart = {}

# if "menu" not in st.session_state:
#     st.session_state.menu = "Add to Cart"

# # ======================================
# # PRODUCT CATALOG
# # ======================================
# PRODUCTS = {
#     "Laptop": 55000,
#     "Mobile": 25000,
#     "Headphones": 2000,
#     "Keyboard": 1500,
#     "Mouse": 800
# }

# # ======================================
# # CART FUNCTIONS (LOGIC LAYER)
# # ======================================
# def add_to_cart(product_name, quantity):
#     if product_name in st.session_state.cart:
#         st.session_state.cart[product_name]["qty"] += quantity
#     else:
#         st.session_state.cart[product_name] = {
#             "price": PRODUCTS[product_name],
#             "qty": quantity
#         }

# def update_quantity(product_name, new_quantity):
#     if product_name in st.session_state.cart:
#         st.session_state.cart[product_name]["qty"] = new_quantity

# def remove_item(product_name):
#     if product_name in st.session_state.cart:
#         del st.session_state.cart[product_name]

# def clear_cart():
#     st.session_state.cart.clear()

# def buy_now():
#     clear_cart()

# # ======================================
# # UI HEADER
# # ======================================
# st.title("🛒 Flipkart Add-to-Cart System")

# # ======================================
# # MENU (STREAMLIT VERSION)
# # ======================================
# menu = st.sidebar.radio(
#     "📋 Menu",
#     [
#         "Add to Cart",
#         "Update Quantity",
#         "Remove Item",
#         "Show Cart",
#         "Buy Now"
#     ]
# )

# # ======================================
# # ADD TO CART
# # ======================================
# if menu == "Add to Cart":
#     st.subheader("➕ Add Product")

#     product = st.selectbox("Select Product", PRODUCTS.keys())
#     quantity = st.number_input("Quantity", min_value=1, step=1)

#     st.write(f"💰 Price: ₹ {PRODUCTS[product]}")

#     if st.button("Add to Cart"):
#         add_to_cart(product, quantity)
#         st.success(f"{product} added to cart")

# # ======================================
# # UPDATE QUANTITY
# # ======================================
# elif menu == "Update Quantity":
#     st.subheader("✏️ Update Quantity")

#     if st.session_state.cart:
#         product = st.selectbox("Select Product", st.session_state.cart.keys())
#         new_qty = st.number_input(
#             "New Quantity",
#             min_value=1,
#             value=st.session_state.cart[product]["qty"]
#         )

#         if st.button("Update"):
#             update_quantity(product, new_qty)
#             st.success("Quantity updated")
#     else:
#         st.info("Cart is empty")

# # ======================================
# # REMOVE ITEM
# # ======================================
# elif menu == "Remove Item":
#     st.subheader("❌ Remove Item")

#     if st.session_state.cart:
#         product = st.selectbox("Select Product", st.session_state.cart.keys())

#         if st.button("Remove"):
#             remove_item(product)
#             st.success(f"{product} removed")
#             st.experimental_rerun()
#     else:
#         st.info("Cart is empty")

# # ======================================
# # SHOW CART
# # ======================================
# elif menu == "Show Cart":
#     st.subheader("🧺 Your Cart")

#     if st.session_state.cart:
#         total = 0

#         for product, details in st.session_state.cart.items():
#             st.write(
#                 f"📦 {product} | Qty: {details['qty']} | "
#                 f"Price: ₹ {details['price'] * details['qty']}"
#             )
#             total += details["price"] * details["qty"]

#         st.divider()
#         st.subheader(f"💳 Total Amount: ₹ {total}")

#         if st.button("🧹 Clear Cart"):
#             clear_cart()
#             st.success("Cart cleared")
#             st.experimental_rerun()
#     else:
#         st.info("Cart is empty")

# # ======================================
# # BUY NOW
# # ======================================
# elif menu == "Buy Now":
#     st.subheader("🛍 Checkout")

#     if st.session_state.cart:
#         total = sum(
#             item["price"] * item["qty"]
#             for item in st.session_state.cart.values()
#         )

#         st.success(f"Total payable amount: ₹ {total}")

#         if st.button("Confirm Order"):
#             buy_now()
#             st.success("Order placed successfully 🎉")
#     else:
#         st.info("Cart is empty")

# # ======================================
# # FOOTER
# # ======================================
# st.caption("Single-file Streamlit Add-to-Cart App | Interview-Ready")

