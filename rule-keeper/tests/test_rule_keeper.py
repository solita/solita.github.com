from unittest import TestCase, mock
from rule_keeper import RuleKeeper


class TestRuleKeeper(TestCase):
    filename1 = '_posts/2020-01-01-file1.md'
    filename2 = '_posts/2021-01-01-file1.md'
    filename3 = '_posts/2022-01-01-file1.txt'

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
        self.printer = mock.Mock()

    def test_expect_only_markdown_files_to_be_processed(self):
        expected_result_tags = self.existing_tags[self.filename1] + self.existing_tags[self.filename2]

        RuleKeeper(self.post_data_extractor_mock, [], self.printer) \
            .check_rules_for_files([self.filename1, self.filename2, self.filename3])

        self.post_data_extractor_mock.extract_data.assert_has_calls(
            [mock.call(self.filename1), mock.call(self.filename2)])

        with self.assertRaises(AssertionError):
            self.post_data_extractor_mock.extract_data.assert_has_calls([mock.call(self.filename3)])

    def test_expect_all_results_to_be_merged_and_grouped_by_type_when_passing_to_printer(self):
        RuleKeeper(
            self.post_data_extractor_mock,
            [
                lambda post_data: {},
                lambda post_data: {'recommendations': ['Recommendation1', 'Recommendation2']},
                lambda post_data: {'recommendations': ['Recommendation3', 'Recommendation4'], 'warnings': ['Warning1']},
                lambda post_data: {'warnings': ['Warning2'], 'errors': ['Error1', 'Error2']}
            ],
            self.printer
        ).check_rules_for_files([self.filename1, self.filename2])

        expected_results_per_file = {
            'errors': ['Error1', 'Error2'],
            'warnings': ['Warning1', 'Warning2'],
            'recommendations': ['Recommendation1', 'Recommendation2', 'Recommendation3', 'Recommendation4'],
        }

        self.printer.assert_has_calls([
            mock.call(self.filename1, expected_results_per_file),
            mock.call(self.filename2, expected_results_per_file),
        ])

    def test_expect_to_return_true_when_any_checker_returns_error(self):
        self.assertTrue(RuleKeeper(
            self.post_data_extractor_mock,
            [
                lambda post_data: {'warnings': ['Warning2'], 'errors': ['Error1', 'Error2']}
            ],
            self.printer
        ).check_rules_for_files([self.filename1, self.filename2]))

