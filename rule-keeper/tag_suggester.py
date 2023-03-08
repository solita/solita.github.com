from post_data_extractor import PostData
from rule_keeper import RuleCheckResults


class ExistingTagsSuggester:
    all_tags = set()
    lookup_directory: str

    def __init__(self, lookup_directory: str):
        self.lookup_directory = lookup_directory

    def suggest_tags(self, post_data: PostData) -> RuleCheckResults:
        if 'tags' not in post_data.metadata:
            return {}

        return {}


class KeyTagsSuggester:
    key_tags: dict[list[str]]

    def __init__(self, key_tags):
        self.key_tags = key_tags

    def suggest_related_tags(self, post_data: PostData) -> RuleCheckResults:
        if 'tags' not in post_data.metadata:
            return {}

        post_tags = post_data.metadata['tags']

        unique_content_words = set("\n".join(post_data.content).split(' '))

        tags_to_suggest = []
        for key_tag in self.key_tags:
            if key_tag in unique_content_words and key_tag not in post_tags:
                tags_to_suggest.append(key_tag)

        if tags_to_suggest:
            return {
                'recommendations': [
                    'Following tags would be recommended to add to the post '
                    + post_data.filename
                    + ": \n- "
                    + "\n- ".join(tags_to_suggest)
                ]
            }

        return {}
