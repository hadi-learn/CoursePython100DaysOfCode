print("Welcome to the Python pizza deliveries!")
size = input("What size pizza do you want? S, M, or L? ").lower()
add_pepperoni = input("Do you want pepperoni? Y or N? ").lower()
extra_cheese = input("Do you want extra cheese? Y or N? ").lower()

pizza_price = 0
pepperoni_price = 0
cheese_price = 0
if size == "s":
    pizza_price = 15
    if add_pepperoni == "y":
        pepperoni_price = 2
    elif add_pepperoni == "n":
        pepperoni_price = 0
elif size == "m":
    pizza_price = 20
    if add_pepperoni == "y":
        pepperoni_price = 3
    elif add_pepperoni == "n":
        pepperoni_price = 0
elif size == "l":
    pizza_price = 25
    if add_pepperoni == "y":
        pepperoni_price = 3
    elif add_pepperoni == "n":
        pepperoni_price = 0
if extra_cheese == "y":
    cheese_price = 1
elif extra_cheese == "n":
    cheese_price = 0
print(f"Your final bill is: ${pizza_price + pepperoni_price + cheese_price}")
