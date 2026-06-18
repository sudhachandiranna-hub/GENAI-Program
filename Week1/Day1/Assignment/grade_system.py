# grade_system.py

def get_grade(mark):
    """Return the letter grade for a valid mark."""
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "E"


def main():
    try:
        user_input = input("Enter a mark (0-100): ").strip()

        # Convert input to a number
        mark = float(user_input)

        # Validate range
        if mark < 0 or mark > 100:
            print(f"Error: {mark} is outside the valid range of 0 to 100.")
            return

        grade = get_grade(mark)

        # Display result
        if mark.is_integer():
            mark_display = int(mark)
        else:
            mark_display = mark

        print(f"Mark entered: {mark_display}")
        print(f"Grade: {grade}")

    except ValueError:
        print("Error: Please enter a valid numeric mark between 0 and 100.")


if __name__ == "__main__":
    main()