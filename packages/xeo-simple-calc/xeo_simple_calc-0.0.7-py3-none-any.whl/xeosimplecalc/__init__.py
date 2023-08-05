class Calc():
    def add(self, num1, num2):
        return num1 + num2
    def subtract(self, num1, num2):
        return num1 - num2
    def multiply(self, num1, num2):
        return num1 * num2
    def divide(self, num1, num2):
        return num1 / num2
    def exponentiation(self, num, degree):
        return num ** degree
    def square_root(self, num):
        if num <= 0:
            return 0
        else:
            return num ** 0.5