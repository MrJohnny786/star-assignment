import argparse

def task1():
    print("Task 1 executed")

def task2():
    print("Task 2 executed")

def task3():
    print("Task 3 executed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A command-line interface to manage tasks")

    # Define the available tasks as sub-commands
    subparsers = parser.add_subparsers(title="Available Tasks")

    # Task 1
    parser_task1 = subparsers.add_parser("task1", help="Execute Task 1")
    parser_task1.set_defaults(func=task1)

    # Task 2
    parser_task2 = subparsers.add_parser("task2", help="Execute Task 2")
    parser_task2.set_defaults(func=task2)

    # Task 3
    parser_task3 = subparsers.add_parser("task3", help="Execute Task 3")
    parser_task3.set_defaults(func=task3)

    # Parse the command-line arguments and execute the selected task
    args = parser.parse_args()
    args.func()



