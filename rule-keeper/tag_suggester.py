from post_data_extractor import PostData
from rule_keeper import RuleCheckResults


class ExistingTagsSuggester:
    all_tags = set()
    lookup_directory: str

    def __init__(self, lookup_directory: str):
        self.lookup_directory = lookup_directory

    def suggest_tags(self, post_data: PostData) -> RuleCheckResults:
        return {}


def suggest_related_tags(post_data: PostData) -> RuleCheckResults:
    product_specific_tags = []
    aws_tag_found = False
    aws_product_tag_found = False

    return {}
