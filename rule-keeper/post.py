from git import Repo, DiffIndex
from typing import NamedTuple
from os.path import basename
from yaml import load, Loader


class PostsRepository:
    def find_new_posts_identifiers(self) -> list[str]:
        pass

    def find_modified_posts_identifiers(self) -> list[str]:
        pass


class GitPostsRepository(PostsRepository):
    posts_path_prefix: str
    branches_diff: DiffIndex

    def __init__(self, repository_location: str, posts_path_prefix: str):
        self.posts_path_prefix = posts_path_prefix
        repository = Repo(repository_location)
        current_branch_commits = repository.head.commit.tree
        master_branch_commits = repository.commit('master')
        self.branches_diff = master_branch_commits.diff(current_branch_commits)

    def find_modified_posts_identifiers(self) -> list[str]:
        file_paths = []

        # Collection all new files
        for file in self.branches_diff.iter_change_type('M'):
            if self.is_file_a_post_file(file.b_path):
                file_paths.append(file.b_path)

        return file_paths

    def find_new_posts_identifiers(self) -> list[str]:
        file_paths = []

        # Collection all new files
        for file in self.branches_diff.iter_change_type('A'):
            if self.is_file_a_post_file(file.b_path):
                file_paths.append(file)

        return file_paths

    def is_file_a_post_file(self, file_path: str):
        return file_path.startswith(self.posts_path_prefix) and file_path.endswith('.md')


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
        self.current_section = None

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
