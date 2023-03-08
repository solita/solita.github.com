import re
from rule_keeper import RuleCheckResults
from post_data_extractor import PostData


def filename_starts_with_a_date(post_data: PostData) -> RuleCheckResults:
    if not re.search('^[0-9]{4}-[0-9]{2}-[0-9]{2}', post_data.filename):
        return {'errors': ['Filename must start with a date']}

    return {}
