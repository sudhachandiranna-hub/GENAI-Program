# calculator.py

def add(num1, num2):
    return num1 + num2


def subtract(num1, num2):
    return num1 - num2


def multiply(num1, num2):
    return num1 * num2


def divide(num1, num2):
    if num2 == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return num1 / num2


def get_number(prompt):
    """
    Continuously ask until a valid number is entered.
    """
    while True:
        try:
            value = input(prompt).strip()

            if not value:
                print("Error: Input cannot be empty.")
                continue

            return float(value)

        except ValueError:
            print("Error: Please enter a valid numeric value.")


def display_menu():
    """
    Display calculator menu.
    """
    print("\n" + "=" * 35)
    print("       SIMPLE CALCULATOR")
    print("=" * 35)
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Exit")
    print("=" * 35)


def perform_calculation(choice):
    """
    Execute selected operation.
    """

    num1 = get_number("Enter first number: ")
    num2 = get_number("Enter second number: ")

    try:
        if choice == "1":
            result = add(num1, num2)
            operation = "+"

        elif choice == "2":
            result = subtract(num1, num2)
            operation = "-"

        elif choice == "3":
            result = multiply(num1, num2)
            operation = "*"

        elif choice == "4":
            result = divide(num1, num2)
            operation = "/"

        else:
            print("Invalid operation.")
            return

        print("\nResult")
        print("-" * 20)
        print(f"{num1} {operation} {num2} = {result}")

    except ZeroDivisionError as error:
        print(f"Error: {error}")


def ask_continue():
    """
    Ask whether user wants another calculation.
    """
    while True:
        choice = input(
            "\nDo you want another calculation? (Y/N): "
        ).strip().upper()

        if choice in ["Y", "YES"]:
            return True

        if choice in ["N", "NO"]:
            return False

        print("Please enter Y or N.")


def main():
    """
    Main application entry point.
    """

    print("Welcome to Python Calculator!")

    while True:
        display_menu()

        choice = input("Choose an option (1-5): ").strip()

        if choice == "5":
            print("\nThank you for using the calculator!")
            break

        if choice not in ["1", "2", "3", "4"]:
            print("Error: Please select a valid option (1-5).")
            continue

        perform_calculation(choice)

        if not ask_continue():
            print("\nThank you for using the calculator!")
            break


if __name__ == "__main__":
    main()