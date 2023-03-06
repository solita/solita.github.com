from typing import NamedTuple
from os.path import basename
from yaml import load, Loader


class PostData(NamedTuple):
    filename: str
    content: list[str]
    metadata: dict[str, list[str] | str]


class PostDataExtractor:
    metadata_section_name = 'METADATA'
    metadata_end_section_name = 'METADATA_END'
    content_section_name = 'CONTENT'

    posts_directory: str
    metadata_section_separator = '---'
    tags_metadata_header = 'tags:'
    current_section = None

    def extract_data(self, filepath: str) -> PostData:
        metadata = []
        filename = basename(filepath)
        content = []
        with open(filepath, 'r') as file_object:
            for line_number, line_content in enumerate(file_object):
                if line_number == 0 and not line_content.startswith('---'):
                    raise RuntimeError(
                        'File ' + filepath + ' does not have starting metadata section in first line'
                    )
                if line_number == 0:
                    continue

                section = self.identify_section(line_content)

                match section:
                    case self.metadata_section_name:
                        metadata.append(line_content)
                    case self.content_section_name:
                        content.append(line_content)

        return PostData(metadata=self.parse_metadata(metadata), filename=filename, content=content)

    def parse_metadata(self, metadata: list[str]) -> dict[str, list[str] | str]:
        return load(''.join(metadata), Loader)

    def identify_section(self, line_content: str) -> str:
        if self.current_section is None:
            self.current_section = self.metadata_section_name
        if self.current_section == self.metadata_end_section_name:
            self.current_section = self.content_section_name
        if self.current_section == self.metadata_section_name and line_content.startswith('---'):
            self.current_section = self.metadata_end_section_name

        return self.current_section
