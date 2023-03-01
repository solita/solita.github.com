import jellyfish
from validation import ContentValidatorExecutor, FilenameValidatorExecutor, MetadataValidatorExecutor
from post_data_extractor import PostDataExtractor
import os

content_directory = './_posts'

# class TagsFinder:
#     posts_directory: str
#     post_data_extractor: PostDataExtractor
#     metadata_validator_executor: MetadataValidatorExecutor
#     content_validator_executor: ContentValidatorExecutor
#     filename_validator_executor: FilenameValidatorExecutor
#
#     def __init__(self, posts_directory: str, post_data_extractor: PostDataExtractor):
#         self.posts_directory = posts_directory
#         self.post_data_extractor = post_data_extractor
#
#     def find_tags(self):
#         filepaths = self.find_post_files()
#         tags = [self.extract_post_tags(filepath) for filepath in filepaths if filepath.endswith('.md')]
#         return []
#
#     def extract_post_tags(self, filepath: str):
#         post_data = self.post_data_extractor.extract_data(filepath)
#
#         return post_data
#
#     def find_post_files(self) -> list[str]:
#         return os.listdir(self.posts_directory)


filepaths = os.listdir(content_directory)
tags = [PostDataExtractor(content_directory).extract_data(filepath) for filepath in filepaths if filepath.endswith('.md')]
print(tags)
