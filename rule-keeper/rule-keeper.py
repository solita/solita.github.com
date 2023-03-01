import jellyfish
import os

content_directory = './_posts'


class TagsFinder:
    posts_directory: str

    def __init__(self, posts_directory: str):
        self.posts_directory = posts_directory

    def find_tags(self):
        filepaths = self.find_post_files()
        tags = [self.extract_post_tags(filepath) for filepath in filepaths if filepath.endswith('.md')]
        return []

    def extract_post_tags(self, filepath: str):
        tags = PostDataExtractor(self.posts_directory + '/' + filepath).extract_metadata()

        print(tags)

        return tags

    def find_post_files(self) -> list[str]:
        return os.listdir(self.posts_directory)


class PostDataExtractor:
    post_filepath: str
    metadata_section_separator = '---'
    tags_metadata_header = 'tags:'

    def __init__(self, post_filepath: str):
        self.post_filepath = post_filepath

    def extract_data(self):
        append_line = False
        lines_with_metadata = []
        with open(self.post_filepath, 'r') as file_object:
            for line_number, line_content in enumerate(file_object):

                if line_number == 0 and not line_content.startswith(self.metadata_section_separator):
                    raise RuntimeError('Post file "' + self.post_filepath + '" must start with metadata')
                if line_number != 0 and line_content.startswith(self.metadata_section_separator):
                    break

                if line_number > 0 and line_content.startswith(self.tags_metadata_header):
                    append_line = True
                if append_line and not line_content.startswith(self.tags_metadata_header):
                    lines_with_metadata.append(line_content.replace('-', '', 1).strip())

        return lines_with_metadata

    def extract_metadata(self):
        pass


class IMetadataValidator:
    def validate(self, metadata: dict[str, list[str] | str]) -> list[str]:
        pass


class IContentValidator:
    def validate(self, content: list[str]) -> list[str]:
        pass


class IFilenameValidator:
    def validate(self, filename: str) -> list[str]:
        pass


class ValidatorExecutor:
    validator_registry: list[object]
    validator_type: str
    errors_list = []

    def __init__(self):
        self.validator_registry = []

    def register(self, validator: object):
        pass


class MetadataValidatorExecutor(ValidatorExecutor):
    validator_type = "metadata"
    validator_registry: list[IMetadataValidator]

    def validate(self, metadata: dict[str, list[str] | str]):
        for validator in self.validator_registry:
            self.errors_list[0:0] = validator.validate(metadata)


class ContentValidatorExecutor(ValidatorExecutor):
    validator_type = "content"
    validator_registry: list[IContentValidator]

    def validate(self, content: list[str]):
        for validator in self.validator_registry:
            self.errors_list[0:0] = validator.validate(content)


class FilenameValidatorExecutor(ValidatorExecutor):
    validator_type = "filename"
    validator_registry: list[IFilenameValidator]

    def validate(self, filename: str):
        for validator in self.validator_registry:
            self.errors_list[0:0] = validator.validate(filename)


tags = TagsFinder(content_directory).find_tags()
