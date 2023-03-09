from rule_keeper import RuleCheckResults


def print_results(filepath: str, check_results: RuleCheckResults) -> None:
    RECOMMENDATION = '\033[96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    results_types = {'recommendations': RECOMMENDATION, 'errors': FAIL, 'warnings': WARNING}
    if any(result_list for result_list in check_results.values()):
        print('Checks results for file: ' + filepath)

        for key in results_types.keys():
            if key in check_results and check_results[key]:
                print(results_types[key] + key.title() + ':')
                [print(result) for result in check_results[key]]
                print(ENDC)
