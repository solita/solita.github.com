from post_data_extractor import PostDataExtractor, PostData
from typing import Callable, NotRequired, TypedDict


class RuleCheckResults(TypedDict):
    warnings: NotRequired[list[str]]
    errors: NotRequired[list[str]]
    recommendations: NotRequired[list[str]]


class RuleKeeper:
    rule_checkers: list[Callable[[PostData], RuleCheckResults]] = []
    post_data_extractor: PostDataExtractor
    results_printer: Callable[[RuleCheckResults], None]

    def __init__(
            self,
            post_data_extractor: PostDataExtractor,
            rule_checkers: list[Callable[[PostData], RuleCheckResults]],
            results_printer: Callable[[RuleCheckResults], None]
    ):
        self.post_data_extractor = post_data_extractor
        self.rule_checkers = rule_checkers
        self.results_printer = results_printer

    def feed_tag_cleaner(self, post_data: PostData):
        pass

    def check_rules_for_files(self, files_to_check: list[str]) -> bool:
        issue_found = False
        for filepath in files_to_check:
            if not filepath.endswith('.md'):
                continue

            print('Checking file: ' + filepath)

            post_data = self.post_data_extractor.extract_data(filepath)

            issue_found_in_file = self.execute_rule_checkers(post_data)

            if issue_found_in_file:
                issue_found = True

        return issue_found

    def execute_rule_checkers(self, post_data: PostData) -> bool:
        any_error_found = False
        all_results: RuleCheckResults = ({'errors': [], 'warnings': [], 'recommendations': []})

        for rule_checker in self.rule_checkers:
            checker_results = rule_checker(post_data)
            if checker_results.keys():
                empty_array = []
                all_results = dict(
                    (key, all_results.get(key, empty_array) + checker_results.get(key, empty_array))
                    for key in all_results.keys()
                )

            if 'errors' in checker_results and checker_results['errors']:
                any_error_found = True

        self.results_printer(all_results)

        return any_error_found
