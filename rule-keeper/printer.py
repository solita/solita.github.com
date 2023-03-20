from rule_keeper import RuleCheckResults


class Printer:
    RECOMMENDATION = '\033[96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'
    RESULT_TYPES = {'recommendations': RECOMMENDATION + BOLD, 'errors': FAIL + BOLD, 'warnings': WARNING + BOLD}

    def print(self, filepath: str, check_results: RuleCheckResults) -> None:
        if any(result_list for result_list in check_results.values()):
            to_print = ''

            for result_type in self.RESULT_TYPES.keys():
                if result_type in check_results and check_results[result_type]:
                    to_print += ''.join(
                        self.format_result(result_type, result) for result in check_results[result_type]
                    )

            print('Checks results for file: {}{} \n'.format(filepath, to_print))

    def format_result(self, result_type: str, result: str):
        return "\n{}* {}{}: {}".format(self.RESULT_TYPES[result_type], result_type.title(), self.ENDC, result)
