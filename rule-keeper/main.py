from post import PostDataExtractor
from tag_suggesters import ExistingTagsSuggester, KeyTagsSuggester, find_existing_tags
from validators import filename_starts_with_a_date
from rule_keeper import RuleKeeper
from printer import print_results
from post import find_upsert_posts
from json import load

posts_directory = '_posts'
def load_key_tags():
    with open('./rule-keeper/key_tags.json', 'r') as file:
        return load(file)


post_data_extractor = PostDataExtractor()
upsert_posts = find_upsert_posts(posts_directory + '/')

existing_tags_suggester = ExistingTagsSuggester(
    find_existing_tags(post_data_extractor, './' + posts_directory, find_upsert_posts)
)

key_tags_suggester = KeyTagsSuggester(load_key_tags())

rule_keeper = RuleKeeper(
    post_data_extractor=post_data_extractor,
    rule_checkers=[
        filename_starts_with_a_date,
        existing_tags_suggester.suggest_tags,
        key_tags_suggester.suggest_related_tags,
    ],
    results_printer=print_results,
)
error_found = rule_keeper.check_rules_for_files(find_upsert_posts)

if error_found:
    exit(1)
