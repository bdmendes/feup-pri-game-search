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

        options = [
            "Perform a query (original setup)",
            "Perform a query (tuned setup)",
            "Perform a query (tuned with entity data)",
            "Perform a query (tuned with entity data and gamer profile detection)",
            "Exit"
        ]
        option = request_option(options)
        match option:
            case "Perform a query (original setup)":
                clear_screen()
                query_str = request_query()
                query = GameQuery(query_str, use_bf=False)
                query.print_results_in_pager()
                continue
            case "Perform a query (tuned setup)":
                clear_screen()
                query_str = request_query()
                query = GameQuery(query_str)
                query.print_results_in_pager()
            case "Perform a query (tuned with entity data)":
                clear_screen()
                query_str = request_query()
                query = GameQuery(query_str, use_entities_data=True)
                query.print_results_in_pager()
                continue
            case "Perform a query (tuned with entity data and gamer profile detection)":
                clear_screen()
                query_str = request_query()
                query = GameQuery(
                    query_str, use_gamer_profile=True, use_entities_data=True)
                query.print_results_in_pager()
                continue
            case "Exit":
                print("Bye!")
                break
            case _:
                print("Invalid option")

        print("\nPress enter to go back...")
        input()


if __name__ == "__main__":
    main()
