weight = int(input("What's your weight (kg): "))
height = float(input("What's your height (m): "))
bmi = round(weight / (height ** 2), 2)
if bmi < 18.5:
    category = "underweight"
elif 18.5 <= bmi < 25:
    category = "at normal weight"
elif 25 <= bmi < 30:
    category = "slightly overweight"
elif 30 <= bmi < 35:
    category = "obese"
else:
    category = "clinically obese"
print(f"Your BMI is {bmi}, you are {category}")
