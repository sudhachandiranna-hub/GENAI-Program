# Python Calculator

A menu-driven calculator application written in Python using only the Python Standard Library.

## Features

- Addition
- Subtraction
- Multiplication
- Division
- Input validation
- Exception handling
- Division-by-zero protection
- User-friendly terminal interface
- Continuous calculations until user exits

## Requirements

- Python 3.8+

No external libraries are required.

## File Structure

```text
project/
│
├── calculator.py
└── README.md
```

## Run

```bash
python calculator.py
```

## Supported Operations

| Option | Operation |
|----------|----------|
| 1 | Addition |
| 2 | Subtraction |
| 3 | Multiplication |
| 4 | Division |
| 5 | Exit |

## Error Handling

The application safely handles:

- Empty input
- Non-numeric values
- Invalid menu selections
- Division by zero
- Invalid Y/N responses

## Example

```text
Choose an option (1-5): 4

Enter first number: 10
Enter second number: 2

Result
--------------------
10.0 / 2.0 = 5.0
```

