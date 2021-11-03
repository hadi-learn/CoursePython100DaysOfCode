text_morse_pair = {
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    " ": " ",
}
playing = True
while playing:
    print("This is text to morse converter program!!!")
    user_input = input("Please input your text:\n").lower()
    text = [letter for letter in user_input]
    morse = [text_morse_pair[letter] for letter in text]
    print(" ".join(morse))
    again = input("Do you want to convert another text? (type y/n): ").lower()
    if again == "n":
        print("Thank you. Goodbye!")
        playing = False
