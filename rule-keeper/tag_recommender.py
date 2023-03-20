from post import PostData, PostDataExtractor
from rule_keeper import RuleCheckResults
import jellyfish
from functools import reduce
from operator import iconcat


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


class ExistingTagsRecommender:
    existing_tags: set[str]

    def __init__(self, existing_tags: set[str]):
        self.existing_tags = existing_tags

    def recommend_tags(self, post_data: PostData) -> RuleCheckResults:
        if 'tags' not in post_data.metadata:
            return {}

        tags_recommendations = []
        for new_post_tag in post_data.metadata['tags']:
            for existing_tag in self.existing_tags:
                if new_post_tag and existing_tag and self.are_tags_similar(existing_tag, new_post_tag):
                    tags_recommendations.append(
                        'Tag "{}" looks similar to existing tag "{}". Consider changing it to the existing one'.format(
                            new_post_tag,
                            existing_tag
                        )
                    )

        if tags_recommendations:
            return {'recommendations': tags_recommendations}

        return {}

    def are_tags_similar(self, existing_tag: str, new_tag: str) -> bool:
        unified_existing_tag = existing_tag.lower()
        unified_new_tag = new_tag.lower()
        return jellyfish.jaro_similarity(unified_new_tag, unified_existing_tag) >= 0.90 \
            and (jellyfish.jaro_similarity(unified_new_tag, unified_existing_tag) != 1 or existing_tag != new_tag)


class KeyTagsRecommender:
    key_tags: list[str]

    def __init__(self, key_tags):
        self.key_tags = key_tags

    def recommend_tags(self, post_data: PostData) -> RuleCheckResults:
        post_tags: list[str] = post_data.metadata['tags'] if 'tags' in post_data.metadata else []

        unique_content_words = set(reduce(iconcat, [content_line.split(' ') for content_line in post_data.content], []))

        tags_recommendations = ['']

        for key_tag in self.key_tags:
            if key_tag in unique_content_words and key_tag not in post_tags:
                tags_recommendations.append(key_tag)

        if len(tags_recommendations) > 1:
            return {
                'recommendations': [
                    'Following tags would be recommended to add to the post: {}'.format(
                        "\n  - ".join(tags_recommendations)
                    )
                ]
            }

        return {}
