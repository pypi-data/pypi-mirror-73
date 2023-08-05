class Output:
    TEST_SEARCH_WITHOUT_ARGUMENTS = \
        "Usage: search [OPTIONS]\n" \
        "Try 'search --help' for help.\n\n" \
        "Error: Missing option '--from' / '-f'.\n"

    TEST_SEARCH_ONE_ARGUMENT_IS_MISSING = \
        "Usage: search [OPTIONS]\n" \
        "Try 'search --help' for help.\n\n" \
        "Error: Missing option '--to' / '-t'.\n"

    TEST_SEARCH_WITH_WRONG_ARGUMENT = \
        "Usage: search [OPTIONS]\n" \
        "Try 'search --help' for help.\n\n" \
        "Error: no such option: --fly\n"

    TEST_SEARCH_HELP_MESSAGE = \
        "Usage: search [OPTIONS]\n" \
        "\n" \
        "Options:\n" \
        "  -f, --from TEXT         Departure City  [required]\n" \
        "  -t, --to TEXT           Destination City (can be multiple)  [required]\n" \
        "  -a, --all-destinations  Shows flights for every destination. (default - shows\n" \
        "                          only the best destination\n" \
        "\n" \
        "  -e, --explain-result    If entered cities were misspelled, then it explains\n" \
        "                          what cities were searched and suggests correct city\n" \
        "                          name options\n" \
        "\n" \
        "  --help                  Show this message and exit.\n"

    TEST_SEARCH = \
        'From Paris, Paris Orly:\n' \
        'To London, Heathrow                                     $731 / 367 km        = $1.99 per km\n'

    TEST_SEARCH_ALL_DESTINATIONS = \
        'From Paris, Paris Orly:\n' \
        'To New York, John F. Kennedy International              $383 / 5834 km       = $0.07 per km\n' \
        'To New York, John F. Kennedy International              $383 / 5834 km       = $0.07 per km\n' \
        'To New York, John F. Kennedy International              $383 / 5834 km       = $0.07 per km\n'

    TEST_SEARCH_EXPLAIN_RESULTS = \
        'From Paris, Paris Orly:\n' \
        'To New York, John F. Kennedy International              $383 / 5834 km       = $0.07 per km\n\n' \
        'Explanation and suggestions:\n' \
        'City "pari" was misspelled. It was assumed as "Paris" in France. ' \
        'Maybe you meant next options: "Parikia", "Parintins", "Saint Joseph Parish"\n' \

    TEST_SEARCH_FLIGHT_NOT_FOUND = \
        'Unfortunately, there is no any flights to all destinations. Try other routes.\n'

    TEST_SEARCH_NO_FLIGHT_DUE_TO_CITY_NOT_FOUND = \
        'Unfortunately, there is no any flights to all destinations. Try other routes.\n\n' \
        'Explanation and suggestions:\n' \
        'City "asdghjaskgdj" was misspelled. No assumption found.\n'

    TEST_FLIGHT_OPTIMIZER_GET_RESULT_EXPLANATION = \
        '\nExplanation and suggestions:\n' \
        'City "pari" was misspelled. It was assumed as "Paris" in France. ' \
        'Maybe you meant next options: "Parikia", "Parintins", "Saint Joseph Parish"' \

