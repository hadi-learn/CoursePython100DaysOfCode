print("Welcome to the Love Calculator")
name1 = input("What is your name?\n")
name2 = input("What is their name?\n")

name = (name1 + name2).lower()

t = name.count("t")
r = name.count("r")
u = name.count("u")
e = name.count("e")
digit1 = str(t + r + u + e)
l = name.count("l")
o = name.count("o")
v = name.count("v")
e = name.count("e")
digit2 = str(l + o + v + e)
percent = int(digit1+digit2)
if percent < 10 or percent > 90:
    print(f"Your score is {percent}, you go together like coke and mentos.")
elif 40 <= percent <= 50:
    print(f"Your score is {percent}, you are alright together.")
else:
    print(f"Your score is {percent}.")
