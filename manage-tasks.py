import argparse
import api.get_character


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A command-line interface to manage tasks")

    # Define the available tasks as sub-commands
    subparsers = parser.add_subparsers(title="Available Tasks")

    # Task 1
    parser.add_argument('--search', type=str,
                        help='Find a star wars character')

    # Parse the command-line arguments and execute the selected task
    args = parser.parse_args()
    task1 = api.get_character.Character(args.search).main()
    # args.func()
