import unittest
from unittest import mock
from tag_recommender import find_existing_tags, ExistingTagsRecommender, KeyTagsRecommender
from rule_keeper import RuleCheckResults
from post import PostData


class TestKeyTagsrecommender(unittest.TestCase):
    content = [
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse ut ligula vel augue tincidunt '
        'convallis. Sed quis lectus ut nisl ultricies maximus. Duis consequat, magna eget consequat bibendum, '
        'eros sapien dignissim erat, eu dapibus mauris leo ac nisi. Pellentesque ac massa in mauris euismod '
        'porttitor. Donec tristique nisl non lorem mollis malesuada. Nullam congue nunc quis sapien luctus '
        'dignissim. Nam condimentum neque non risus bibendum, ut faucibus arcu feugiat.',
        'Azure est purus vel libero dictum, eget pharetra risus interdum. Morbi sit amet nibh malesuada, '
        'commodo nisi ut, ultricies nulla. Etiam ut enim massa. Azure blandit eros ac tellus sagittis '
        'fringilla. Aliquam tempus elit sed dolor blandit, ut elementum nisl molestie. Integer a lacinia '
        'velit. Nulla ultricies lobortis urna, vitae feugiat sapien convallis nec. Nullam eget sapien vel '
        'turpis eleifend tristique non at nunc.',
        'AWS sed vitae sapien id diam eleifend mattis vel in sapien. Mauris pharetra lectus vel velit ultrices, '
        'ac euismod quam ultricies. Donec aliquam, turpis vitae sollicitudin hendrerit, sapien dui molestie turpis, '
        'non gravida odio lacus vel lectus.'
    ]

    def test_expect_single_tag_recommended_even_when_keyword_appears_multiple_times(self):
        key_tags_recommender = KeyTagsRecommender(['Azure', 'Google Cloud'])
        post_data = PostData(filename='some-file.md', content=self.content, metadata={})
        result = key_tags_recommender.recommend_tags(post_data)
        self.assertIn('recommendations', result)
        self.assertEqual(len(result['recommendations']), 1)
        self.assertTrue(
            'Azure' in result['recommendations'][0],
            'Azure tag is missing in recommendation'
        )
        self.assertTrue(
            result['recommendations'][0].count('Azure') == 1,
            'Azure tag was recommended more than once'
        )

    def test_expect_multiple_tags_recommended_when_multiple_possible_keywords_appear(self):
        key_tags_recommender = KeyTagsRecommender(['Azure', 'AWS'])
        post_data = PostData(filename='some-file.md', content=self.content, metadata={})
        result = key_tags_recommender.recommend_tags(post_data)
        self.assertIn('recommendations', result)
        self.assertEqual(len(result['recommendations']), 1)
        self.assertTrue(
            'Azure' in result['recommendations'][0],
            'Azure tag is missing in recommendation'
        )
        self.assertTrue(
            'AWS' in result['recommendations'][0],
            'AWS tag is missing in recommendation'
        )

    def test_expect_tag_key_tag_to_not_be_recommended_when_already_in_tags_list(self):
        key_tags_recommender = KeyTagsRecommender(['Azure', 'Google Cloud'])
        post_data = PostData(filename='some-file.md', content=self.content, metadata={'tags': ['Azure']})
        result = key_tags_recommender.recommend_tags(post_data)
        self.assertNotIn('recommendations', result)

    def test_expect_no_tags_recommended_when_no_keywords_found(self):
        key_tags_recommender = KeyTagsRecommender(['Microsoft', 'Google Cloud'])
        post_data = PostData(filename='some-file.md', content=self.content, metadata={})
        result = key_tags_recommender.recommend_tags(post_data)
        self.assertNotIn('recommendations', result)


class TestExistingTagsrecommender(unittest.TestCase):
    def setUp(self) -> None:
        self.existing_tags_recommender = ExistingTagsRecommender({'Software development', 'Low-code', 'JavaScript'})

    def test_expect_existing_tag_recommended_when_similar_is_used(self):
        matches = {'lowcode': 'Low-code'}
        post_data = PostData(filename='some-file.md', content=[], metadata={'tags': ['lowcode', 'software', 'code']})
        result = self.existing_tags_recommender.recommend_tags(post_data)
        self.assertIn('recommendations', result)
        self.assertTrue(self.all_matches_found(result, matches))
        self.assertEqual(len(result['recommendations']), 1)

    def test_expect_multiple_existing_tags_recommended_when_multiple_new_tags_is_similar(self):
        matches = {'lowcode': 'Low-code', 'javascript': 'JavaScript'}
        post_data = PostData(filename='some-file.md', content=[], metadata={'tags': ['lowcode', 'javascript', 'code']})
        result = self.existing_tags_recommender.recommend_tags(post_data)
        self.assertIn('recommendations', result)
        self.assertTrue(self.all_matches_found(result, matches))
        self.assertEqual(len(result['recommendations']), 2)

    def test_expect_same_tag_will_be_recommended_multiple_times_if_many_similar_tags_match(self):
        matches = {'lowcode': 'Low-code', 'low-code': 'Low-code'}
        post_data = PostData(
            filename='some-file.md', content=[],
            metadata={'tags': ['lowcode', 'low-code', 'software', 'code']}
        )
        result = self.existing_tags_recommender.recommend_tags(post_data)
        self.assertIn('recommendations', result)
        self.assertTrue(self.all_matches_found(result, matches))
        self.assertEqual(len(result['recommendations']), 2)
        pass

    def test_expect_no_recommendation_when_no_similar_existing_tags_found(self):
        post_data = PostData(
            filename='some-file.md', content=[],
            metadata={'tags': ['Course', 'Talent', 'Dev academy']}
        )
        result = self.existing_tags_recommender.recommend_tags(post_data)
        self.assertNotIn('recommendations', result)

    def all_matches_found(self, result: RuleCheckResults, matches: dict[str, str]) -> bool:
        matches_found = []
        for key, value in matches.items():
            for recommendation in result['recommendations']:
                if key in recommendation and value in recommendation:
                    matches_found.append(True)
                    break

        return all(matches_found) and len(matches_found) == len(matches)


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
