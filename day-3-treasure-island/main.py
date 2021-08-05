print('''
*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\` . "-._ /_______________|_______
|                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/_____ /
*******************************************************************************
''')

print("Welcome to Treasure Island.\nYour mission is to find the treasure.")
choose_direction = input("You're at a cross road. Where do you want to go? Type 'left' or 'right'\n").lower()
if choose_direction == "left":
    print("Game Over! You fell to a trap with a very deep hole with sharp spikes at the bottom of the hole.")
else:
    decision = input("You came to a lake. There is an island in the middle of the lake. "
                 "Type 'wait' to wait for a boat. Type 'swim' to swim across.\n").lower()
    if decision == "swim":
        print("Game Over! You are attacked by sea monster")
    else:
        print("A mysterious boat come and take you to the island.")
        choose_color = input("You arrive at the island unharmed. There is a house with 3 doors. "
                             "One red, one yellow, and one blue. Which color do you choose?\n").lower()
        if choose_color == "red":
            print("Game Over! You entered a beast cage.")
        elif choose_color == "blue":
            print("Congratulation! You have found the treasure. "
                  "There's a portal behind the treasure to teleport you to a safe place.")
        else:
            print("Game Over! It's room full of fire.")
