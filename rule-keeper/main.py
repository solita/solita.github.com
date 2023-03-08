import git.diff

from post_data_extractor import PostDataExtractor
from tag_suggester import ExistingTagsSuggester, KeyTagsSuggester
from validators import filename_starts_with_a_date
from rule_keeper import RuleKeeper
from printer import print_results
from git import Repo
from json import load

posts_directory = '_posts'


def find_files_to_check(path_prefix: str):
    repository = Repo('.')
    current_branch_commits = repository.head.commit.tree
    master_branch_commits = repository.commit('master')
    diff_index = master_branch_commits.diff(current_branch_commits)
    files_to_check = []

    # Collection all new files
    for file in diff_index.iter_change_type('A'):
        files_to_check.append(file)

    # Collection all modified files
    for file in diff_index.iter_change_type('M'):
        files_to_check.append(file)

    return [
        file.b_path for file in files_to_check
        if file.b_path.startswith(path_prefix) and file.b_path.endswith('.md')
    ]


def load_tags_relations():
    with open('./rule-keeper/key_tags.json', 'r') as file:
        return load(file)


existing_tags_suggester = ExistingTagsSuggester('./' + posts_directory)
key_tags_suggester = KeyTagsSuggester(load_tags_relations())

rule_keeper = RuleKeeper(
    post_data_extractor=PostDataExtractor(),
    rule_checkers=[
        filename_starts_with_a_date,
        existing_tags_suggester.suggest_tags,
        key_tags_suggester.suggest_related_tags,
    ],
    results_printer=print_results,
)
error_found = rule_keeper.check_rules_for_files(find_files_to_check(posts_directory + '/'))

if error_found:
    exit(1)
