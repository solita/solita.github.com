from post_data_extractor import PostData


class ExistingTagsSuggester:
    all_tags = set()
    lookup_directory: str

    def __init__(self, lookup_directory: str):
        self.lookup_directory = lookup_directory

    def suggest_tags(self, post_data: PostData):
        print("\n".join(sorted(filter(None, self.all_tags), key=str.casefold)))
        print(len(self.all_tags))
        new_set = set()
        # [new_set.add(new_element.lower().replace('-','')) for new_element in self.all_tags if new_element]
        # print(sorted(new_set))
        # print(len(new_set))
        return []

def suggest_related_tags(post_data: PostData) -> list[str]:
    product_specific_tags = []
    aws_tag_found = False
    aws_product_tag_found = False


    return []