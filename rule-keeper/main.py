import os

import git.diff

from post_data_extractor import PostDataExtractor
from tag_suggesters import ExistingTagsSuggester, KeyTagsSuggester
from validators import filename_starts_with_a_date
from rule_keeper import RuleKeeper
from printer import print_results
from git import Repo
from json import load

posts_directory = '_posts'


def find_files_to_check(path_prefix: str) -> list[str]:
    repository = Repo('.')
    current_branch_commits = repository.head.commit.tree
    master_branch_commits = repository.commit('master')
    diff_index = master_branch_commits.diff(current_branch_commits)
    file_paths = []

    # Collection all new files
    for file in diff_index.iter_change_type('A'):
        file_paths.append(file)

    # Collection all modified files
    for file in diff_index.iter_change_type('M'):
        file_paths.append(file)

    return [
        file_path.b_path for file_path in file_paths
        if file_path.b_path.startswith(path_prefix) and file_path.b_path.endswith('.md')
    ]


def find_existing_tags(
        data_extractor: PostDataExtractor,
        posts_source_directory: str,
        post_files_to_omit: list[str]
) -> list[str]:
    filenames_to_omit = [os.path.basename(post_file_path) for post_file_path in post_files_to_omit]

    existing_tags = []

    for filename in os.listdir(posts_source_directory):
        if filename in filenames_to_omit:
            continue

        post_data = data_extractor.extract_data(os.path.join(posts_source_directory, filename))
        if 'tags' in post_data.metadata:
            existing_tags = existing_tags + post_data.metadata['tags']

    return existing_tags


def load_tags_relations():
    with open('./rule-keeper/key_tags.json', 'r') as file:
        return load(file)


post_data_extractor = PostDataExtractor()
file_paths_to_check = find_files_to_check(posts_directory + '/')

existing_tags_suggester = ExistingTagsSuggester(
    find_existing_tags(post_data_extractor, './' + posts_directory, file_paths_to_check)
)

key_tags_suggester = KeyTagsSuggester(load_tags_relations())

rule_keeper = RuleKeeper(
    post_data_extractor=post_data_extractor,
    rule_checkers=[
        filename_starts_with_a_date,
        existing_tags_suggester.suggest_tags,
        key_tags_suggester.suggest_related_tags,
    ],
    results_printer=print_results,
)
error_found = rule_keeper.check_rules_for_files(file_paths_to_check)

if error_found:
    exit(1)
