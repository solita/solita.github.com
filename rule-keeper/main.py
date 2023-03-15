from post import PostDataExtractor
from tag_recommender import ExistingTagsRecommender, KeyTagsRecommender, find_existing_tags
from validators import filename_starts_with_a_date
from rule_keeper import RuleKeeper
from printer import Printer
from post import GitPostsRepository
from json import load
import os

posts_directory = '_posts'


def load_key_tags():
    with open('./rule-keeper/key_tags.json', 'r') as file:
        return load(file)


post_data_extractor = PostDataExtractor()
posts_provider = GitPostsRepository('.', posts_directory + '/')
upserted_posts_identifiers = posts_provider.find_new_posts_identifiers() + posts_provider.find_modified_posts_identifiers()

existing_tags_recommender = ExistingTagsRecommender(
    set(
        find_existing_tags(
            post_data_extractor,
            [
                filepath for filepath in
                [os.path.join(posts_directory, filename) for filename in os.listdir(posts_directory)]
                if filepath not in upserted_posts_identifiers
            ],
        ))
)

key_tags_recommender = KeyTagsRecommender(load_key_tags())

rule_keeper = RuleKeeper(
    post_data_extractor=post_data_extractor,
    rule_checkers=[
        filename_starts_with_a_date,
        existing_tags_recommender.recommend_tags,
        key_tags_recommender.recommend_tags,
    ],
    results_printer=Printer().print,
)
error_found = rule_keeper.check_rules_for_files(upserted_posts_identifiers)

if error_found:
    exit(1)
