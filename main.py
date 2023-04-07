import argparse
import api.get_character


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A command-line interface to manage tasks")

    subparsers = parser.add_subparsers(title="Available Tasks")

    parser.add_argument('--search', type=str,
                        help='Find a star wars character.')

    parser.add_argument('--world', action='store_true',
                        help='Find a star wars character and correlate their worlds to earth.')

    parser.add_argument('--clean', action='store_true',
                        help='Clean cache')

    parser.add_argument('--virtualize', action='store_true',
                        help='Virtualize data')

    # Parse the command-line arguments and execute the selected task
    args = parser.parse_args()
    task1 = api.get_character.Character(
        args.search, args.world, args.clean, args.virtualize).main()
    # args.func()
