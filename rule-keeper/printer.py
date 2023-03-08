from rule_keeper import RuleCheckResults


def print_results(results: RuleCheckResults) -> None:
    RECOMMENDATION = '\033[96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    results_types = {'recommendations': RECOMMENDATION, 'errors': FAIL, 'warnings': WARNING}

    for key in results_types.keys():
        if key in results and results[key]:
            print(results_types[key] + key.title() + ':')
            [print(result) for result in results[key]]
            print(ENDC)
