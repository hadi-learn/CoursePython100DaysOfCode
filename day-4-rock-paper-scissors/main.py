import random

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

game_images = [rock, paper, scissors]
score = 0
game_is_on = True
while game_is_on:
    player = int(input("What do you choose?\n"
                       "Type 0 for Rock.\n"
                       "Type 1 for Paper.\n"
                       "Type 2 for Scissor.\n"
                       "Your Answer? "))
    if player == 0:
        print(game_images[player])
        print("Your choice is rock.")
    elif player == 1:
        print(game_images[player])
        print("Your choice is paper.")
    else:
        print(game_images[player])
        print("Your choice is scissors.")

    computer = random.randint(0, 2)
    if computer == 0:
        print(game_images[computer])
        print("Computer choice is rock.")
    elif computer == 1:
        print(game_images[computer])
        print("Computer choice is paper.")
    else:
        print(game_images[computer])
        print("Computer choice is scissors.")

    if computer == player:
        print(f"It's a Draw.\nScore: {score}")
    elif computer == 2 and player == 0:
        score += 1
        print(f"You Win!\nScore: {score}")
    elif computer == 0 and player == 2:
        print(f"You Lose!\nScore: {score}")
        again = input("Try again? y/n: ").lower()
        if again == "n":
            game_is_on = False
        else:
            score = 0
    elif computer > player:
        print(f"You Lose!\nScore: {score}")
        again = input("Try again? y/n: ").lower()
        if again == "n":
            game_is_on = False
        else:
            score = 0
    else:
        score += 1
        print(f"You Win!\nScore: {score}")
