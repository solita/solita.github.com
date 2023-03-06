from post_data_extractor import PostDataExtractor, PostData
from typing import Callable
from os import path
import os


class RuleKeeper:
    WARNING = '\033[93m'
    ENDC = '\033[0m'

    rule_checkers: list[Callable[[PostData], list[str]]] = []
    post_verification_actions: list[Callable[[], list[str]]]
    post_data_extractor: PostDataExtractor
    error_found = False

    def __init__(
            self,
            post_data_extractor: PostDataExtractor,
            rule_checkers: list[Callable[[PostData], list[str]]],
            post_verification_actions: list[Callable[[], list[str]]]
    ):
        self.post_data_extractor = post_data_extractor
        self.rule_checkers = rule_checkers
        self.post_verification_actions = post_verification_actions

    def feed_tag_cleaner(self, post_data: PostData):
        pass

    def verify_rules(self, lookup_directory: str) -> bool:
        issue_found = False

        filepaths = os.listdir(lookup_directory)
        for filepath in filepaths:
            if not filepath.endswith('.md'):
                continue

            print('Checking file: ' + filepath)

            post_data = self.post_data_extractor.extract_data(path.join(lookup_directory, filepath))

            issues = []
            for rule_checker in self.rule_checkers:
                issues = issues + rule_checker(post_data)

            if issues:
                issue_found = True
                self.print_issues(issues)

        return issue_found

    def print_issues(self, issues: list[str]):
        print(self.WARNING)
        [print(issue) for issue in issues]
        print(self.ENDC)
