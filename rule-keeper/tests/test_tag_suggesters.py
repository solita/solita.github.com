import unittest
from unittest import mock
from tag_suggesters import find_existing_tags


class TestKeyTagsSuggester(unittest.TestCase):
    pass


class TestExistingTagsSuggester(unittest.TestCase):
    pass


class TestFindExistingTags(unittest.TestCase):
    filename1 = '_posts/2020-01-01-file1.md'
    filename2 = '_posts/2021-01-01-file1.md'

    existing_tags: dict[str, list[str]] = {}

    def setUp(self) -> None:
        self.existing_tags = {
            self.filename1: ['tag1', 'tag2', 'tag3'],
            self.filename2: ['tag4', 'tag5', 'tag6'],
        }
        self.post_data_extractor_mock = mock.Mock()
        self.post_data_extractor_mock.extract_data = mock.MagicMock(
            side_effect=lambda filepath: type('obj', (object,), {'metadata': {'tags': self.existing_tags[filepath]}})
        )

    def test_expect_all_tags_from_processed_files_to_be_combined(self):
        expected_result_tags = self.existing_tags[self.filename1] + self.existing_tags[self.filename2]

        self.assertEqual(
            find_existing_tags(
                self.post_data_extractor_mock,
                [self.filename1, self.filename2]
            ),
            expected_result_tags
        )
