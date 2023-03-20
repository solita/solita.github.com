import unittest
from validators import filename_starts_with_a_date, PostData


class TestFilenameStartsWithDate(unittest.TestCase):
    def test_expect_success_when_filepath_starts_with_iso_date(self):
        result = filename_starts_with_a_date(PostData(filename='2020-12-31-some-name.md', content=[], metadata={}))
        self.assertNotIn('errors', result)

    def test_expect_failure_when_filepath_starts_with_not_iso_date(self):
        result = filename_starts_with_a_date(PostData(filename='31-12-2020-some-file.md', content=[], metadata={}))
        self.assertIn('errors', result)
        self.assertEqual(len(result['errors']), 1)

    def test_expect_failure_when_filepath_starts_with_not_date(self):
        result = filename_starts_with_a_date(PostData(filename='random-file-name.md', content=[], metadata={}))
        self.assertIn('errors', result)
        self.assertEqual(len(result['errors']), 1)
