## ********Day 55 Continue from Day 54**********
## Functions can have inputs/functionality/output
# def add(n1, n2):
#     return n1 + n2
#
#
# def subtract(n1, n2):
#     return n1 - n2
#
#
# def multiply(n1, n2):
#     return n1 * n2
#
#
# def divide(n1, n2):
#     return n1 / n2
#
#
# ## Functions are first-class objects, can be passed around as arguments e.g. int/string/float etc.
#
# def calculate(calc_function, n1, n2):
#     return calc_function(n1, n2)
#
# result = calculate(add, 2, 3)
# print(result)
#
#
# ## Functions can be nested in other functions
#
# def outer_function():
#     print("I'm outer")
#
#     def nested_function():
#         print("I'm inner")
#
#     nested_function()
#
# outer_function()
#
#
# ## Functions can be returned from other functions
# def outer_function():
#     print("I'm outer")
#
#     def nested_function():
#         print("I'm inner")
#
#     return nested_function
#
#
# inner_function = outer_function()
# inner_function()
#
# ## Simple Python Decorator Functions
# import time
#
#
# def delay_decorator(function):
#     def wrapper_function():
#         time.sleep(2)
#         # Do something before
#         function()
#         function()
#         # Do something after
#
#     return wrapper_function
#
#
# @delay_decorator
# def say_hello():
#     print("Hello")
#
#
# # With the @ syntactic sugar
# @delay_decorator
# def say_bye():
#     print("Bye")
#
#
# # Without the @ syntactic sugar
# def say_greeting():
#     print("How are you?")
#
#
# decorated_function = delay_decorator(say_greeting)
# decorated_function()

# Advanced Python Decorator Functions

class User:
    def __init__(self, name):
        self.name = name
        self.is_logged_in = False


# create a decorator function to check is the user have the authorization to create a blog
def is_authenticated_user(function):
    def wrapper_function(*args, **kwargs):  # args needed so the user name can be passed into the wrapper function
        if args[0].is_logged_in == True:  # args position index 0 should be checked because only 1 argument passed in
            function(args[0])  # execute the function with the argument on position index 0
    return wrapper_function

@is_authenticated_user
def create_blog_post(user):
    print(f"This is {user.name}'s new blog post.")


# a new user without authorization try to create a blog
new_user_not_login_yet = User("Syukri")
create_blog_post(new_user_not_login_yet)

# a new user with authorization try to create a blog
new_user_logged_in = User("Hadi")
new_user_logged_in.is_logged_in = True
create_blog_post(new_user_logged_in)

# an old user with authorization
old_user = User("Kamil")
old_user.is_logged_in = True
create_blog_post(old_user)
