import os
import unittest
from post import PostDataExtractor, PostData
from yaml.scanner import ScannerError


class TestPostDataExtractor(unittest.TestCase):
    post_data_extractor: PostDataExtractor

    def setUp(self) -> None:
        self.post_data_extractor = PostDataExtractor()

    def test_expect_to_extract_data_from_valid_post_file(self):
        file_to_process = 'tests/fixtures/2023-03-13-valid-post.md'
        expected_post_data = PostData(
            filename='2023-03-13-valid-post.md',
            content=[
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse ut ligula vel augue tincidunt convallis. Sed quis',
                'lectus ut nisl ultricies maximus. Duis consequat, magna eget consequat bibendum, eros sapien dignissim erat, eu dapibus',
                'mauris leo ac nisi. Pellentesque ac massa in mauris euismod porttitor. Donec tristique nisl non lorem mollis malesuada.',
                'Nullam congue nunc quis sapien luctus dignissim. Nam condimentum neque non risus bibendum, ut faucibus arcu feugiat.',
                '',
                'Azure est purus vel libero dictum, eget pharetra risus interdum. Morbi sit amet nibh malesuada, commodo nisi ut,',
                'ultricies nulla. Etiam ut enim massa. Duis blandit eros ac tellus sagittis fringilla. Aliquam tempus elit sed dolor',
                'blandit, ut elementum nisl molestie. Integer a lacinia velit. Nulla ultricies lobortis urna, vitae feugiat sapien',
                'convallis nec. Nullam eget sapien vel turpis eleifend tristique non at nunc.',
                '',
                'Azure sed vitae sapien id diam eleifend mattis vel in sapien. Mauris pharetra lectus vel velit ultrices, ac euismod quam',
                'ultricies. Donec aliquam, turpis vitae sollicitudin hendrerit, sapien dui molestie turpis, non gravida odio lacus vel',
                'lectus.',

            ],
            metadata={
                'layout': 'post',
                'title': 'Test Valid Post',
                'author': 'andrzejw',
                'excerpt': 'Some valid post',
                'tags': ['Test', 'Nothing special']
            }
        )

        self.assertSequenceEqual(self.post_data_extractor.extract_data(file_to_process), expected_post_data)

    def test_expect_error_when_metadata_section_is_invalid_yaml(self):
        file_to_process = 'tests/fixtures/2023-03-13-invalid-metadata-post.md'

        with self.assertRaisesRegex(RuntimeError, 'metadata could not be parsed. Metadata might be invalid.'):
            self.post_data_extractor.extract_data(file_to_process)

    def test_expect_error_when_metadata_is_not_closed(self):
        file_to_process = 'tests/fixtures/2023-03-13-not-closed-metadata-post.md'

        with self.assertRaisesRegex(RuntimeError, 'metadata could not be parsed. File does not seem to close metadata'):
            self.post_data_extractor.extract_data(file_to_process)

    def test_expect_error_when_file_dont_start_with_metadata(self):
        file_to_process = 'tests/fixtures/2023-03-13-not-starting-with-metadata-post.md'

        with self.assertRaisesRegex(RuntimeError, 'does not have starting metadata section in first line'):
            self.post_data_extractor.extract_data(file_to_process)
