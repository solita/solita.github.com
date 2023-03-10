from post import PostData, PostDataExtractor
from rule_keeper import RuleCheckResults
import jellyfish
import os


def find_existing_tags(
        data_extractor: PostDataExtractor,
        post_filepaths_to_extract_tags_from: list[str],
) -> list[str]:
    existing_tags = []

    for filepath in post_filepaths_to_extract_tags_from:
        post_data = data_extractor.extract_data(filepath)
        if 'tags' in post_data.metadata:
            existing_tags = existing_tags + post_data.metadata['tags']

    return existing_tags


class ExistingTagsSuggester:
    all_tags = set()
    existing_tags: list[str]

    def __init__(self, existing_tags: list[str]):
        self.existing_tags = existing_tags

    def suggest_tags(self, post_data: PostData) -> RuleCheckResults:
        if 'tags' not in post_data.metadata:
            return {}

        tags_suggestions = []

        for new_post_tag in post_data.metadata['tags']:
            for existing_tag in self.existing_tags:
                if new_post_tag \
                        and existing_tag \
                        and jellyfish.jaro_similarity(new_post_tag, existing_tag) >= 0.90 \
                        and jellyfish.jaro_similarity(new_post_tag, existing_tag) != 1:
                    tags_suggestions.append(
                        'Tag "'
                        + new_post_tag
                        + '" looks similar to existing tag "'
                        + existing_tag
                        + '". Consider changing it to the existing one'
                    )

        if tags_suggestions:
            return {'recommendations': tags_suggestions}

        return {}


class KeyTagsSuggester:
    key_tags: list[str]

    def __init__(self, key_tags):
        self.key_tags = key_tags

    def suggest_related_tags(self, post_data: PostData) -> RuleCheckResults:
        if 'tags' not in post_data.metadata:
            return {}

        post_tags: list[str] = post_data.metadata['tags']

        unique_content_words = set("\n".join(post_data.content).split(' '))

        tags_to_suggest = []
        for key_tag in self.key_tags:
            if key_tag in unique_content_words and key_tag not in post_tags:
                tags_to_suggest.append(key_tag)

        if tags_to_suggest:
            return {
                'recommendations': [
                    "Following tags would be recommended to add to the post: \n- "
                    + "\n- ".join(tags_to_suggest)
                ]
            }

        return {}
