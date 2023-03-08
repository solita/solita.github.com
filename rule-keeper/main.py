from post_data_extractor import PostDataExtractor
from tag_suggester import ExistingTagsSuggester, suggest_related_tags
from validators import filename_starts_with_a_date
from rule_keeper import RuleKeeper
from printer import print_results

posts_directory = './_posts'

existing_tags_suggester = ExistingTagsSuggester(posts_directory)

rule_keeper = RuleKeeper(
    post_data_extractor=PostDataExtractor(),
    rule_checkers=[
        filename_starts_with_a_date,
        existing_tags_suggester.suggest_tags,
        suggest_related_tags
    ],
    results_printer=print_results
)
error_found = rule_keeper.check_rules_for_files(posts_directory)

if error_found:
    exit(1)
