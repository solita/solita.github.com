from post_data_extractor import PostData


class TagsCleaner:
    all_tags = set()

    def collect_tags(self, post_data: PostData) -> list[str]:
        if 'tags' in post_data.metadata:
            [self.all_tags.add(tag) for tag in post_data.metadata['tags']]
        return []

    def suggest_tag_unification(self):
        print(self.all_tags)
        return []
