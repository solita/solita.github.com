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


class RelatedTagsSuggester:
    tag_relations: dict[list[str]]

    def __init__(self, tag_relations):
        self.tag_relations = tag_relations

    def suggest_related_tags(self, post_data: PostData) -> RuleCheckResults:
        if 'tags' not in post_data.metadata:
            return {}

        post_tags = post_data.metadata['tags']

        tags_to_suggest = []

        for parent_tag in self.tag_relations.keys():
            if self.does_any_post_tag_have_a_relation(self.tag_relations[parent_tag], post_tags):
                tags_to_suggest.append(parent_tag)

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

    def does_any_post_tag_have_a_relation(self, children_tags: list[str], post_tags: list[str]) -> bool:
        for post_tag in post_tags:
            for children_tag in children_tags:
                # we have "NULL" post tag in single article, which is then parsed to None,
                # resulting in everything to fail
                if post_tag and post_tag in children_tag:
                    return True
