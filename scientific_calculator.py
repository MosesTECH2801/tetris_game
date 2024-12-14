import math

class ScientificCalculator:
    def __init__(self):
        self.result = 0
        self.history = []

    def add(self, x, y):
        self.result = x + y
        self.history.append(f"{x} + {y} = {self.result}")
        return self.result

    def subtract(self, x, y):
        self.result = x - y
        self.history.append(f"{x} - {y} = {self.result}")
        return self.result

    def multiply(self, x, y):
        self.result = x * y
        self.history.append(f"{x} × {y} = {self.result}")
        return self.result

    def divide(self, x, y):
        if y == 0:
            return "Error: Division by zero"
        self.result = x / y
        self.history.append(f"{x} ÷ {y} = {self.result}")
        return self.result

    def power(self, x, y):
        self.result = math.pow(x, y)
        self.history.append(f"{x} ^ {y} = {self.result}")
        return self.result

    def square_root(self, x):
        if x < 0:
            return "Error: Cannot calculate square root of negative number"
        self.result = math.sqrt(x)
        self.history.append(f"√{x} = {self.result}")
        return self.result

    def sin(self, x):
        self.result = math.sin(math.radians(x))
        self.history.append(f"sin({x}°) = {self.result}")
        return self.result

    def cos(self, x):
        self.result = math.cos(math.radians(x))
        self.history.append(f"cos({x}°) = {self.result}")
        return self.result

    def tan(self, x):
        self.result = math.tan(math.radians(x))
        self.history.append(f"tan({x}°) = {self.result}")
        return self.result

    def show_history(self):
        print("\nCalculation History:")
        for calculation in self.history:
            print(calculation)

def main():
    calculator = ScientificCalculator()
    
    while True:
        print("\nScientific Calculator")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Power")
        print("6. Square Root")
        print("7. Sine")
        print("8. Cosine")
        print("9. Tangent")
        print("10. Show History")
        print("11. Exit")

        choice = input("\nEnter your choice (1-11): ")

        if choice == '11':
            print("Thank you for using the Scientific Calculator!")
            break

        if choice == '10':
            calculator.show_history()
            continue

        try:
            if choice in ['1', '2', '3', '4', '5']:
                x = float(input("Enter first number: "))
                y = float(input("Enter second number: "))
                
                if choice == '1':
                    print("Result:", calculator.add(x, y))
                elif choice == '2':
                    print("Result:", calculator.subtract(x, y))
                elif choice == '3':
                    print("Result:", calculator.multiply(x, y))
                elif choice == '4':
                    print("Result:", calculator.divide(x, y))
                elif choice == '5':
                    print("Result:", calculator.power(x, y))

            elif choice in ['6', '7', '8', '9']:
                x = float(input("Enter number: "))
                
                if choice == '6':
                    print("Result:", calculator.square_root(x))
                elif choice == '7':
                    print("Result:", calculator.sin(x))
                elif choice == '8':
                    print("Result:", calculator.cos(x))
                elif choice == '9':
                    print("Result:", calculator.tan(x))

            else:
                print("Invalid choice! Please select a number between 1 and 11.")

        except ValueError:
            print("Invalid input! Please enter numeric values.")

if __name__ == "__main__":
    main()

