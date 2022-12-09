import os

from query import GameQuery


def clear_screen():
    """Clear the screen."""
    os.system("cls" if os.name == "nt" else "clear")


def request_option(options: list[str], option_name="an option") -> str:
    """Print available options and request an option from the user."""
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    print()

    while True:
        option = input("Select " + option_name +
                       " [1-" + str(len(options)) + "]: ")
        if option.isdigit() and int(option) in range(1, len(options) + 1):
            return options[int(option) - 1]
        print(f"Invalid option: {option}\n")


def request_query() -> str:
    """Request a query from the user."""
    return input("Enter a query: ")


def main():
    """Main function."""
    while True:
        clear_screen()
        print("Welcome to the Steam Games Search Engine CLI!")
        print("Remember to start the Solr instance before using this CLI.")
        print("==============================================")

        options = ["Perfom a query", "See demo queries", "Exit"]
        option = request_option(options)
        match option:
            case "Perfom a query":
                clear_screen()
                query_str = request_query()

                # get profile and get results
                query = GameQuery(query_str)
                query.print_results_in_pager()
                continue
            case "See demo queries":
                clear_screen()
                print("Demo queries")
            case "Exit":
                print("Bye!")
                break
            case _:
                print("Invalid option")

        print("\nPress enter to go back...")
        input()


if __name__ == "__main__":
    main()
