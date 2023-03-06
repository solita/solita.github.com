from validation import ContentValidationExecutor, FilenameValidationExecutor, MetadataValidationExecutor
from post_data_extractor import PostDataExtractor
from tags_cleaner import TagsCleaner
from filename_validators import filename_starts_with_a_date
from rule_keeper import RuleKeeper

posts_directory = './_posts'

filename_validation_executor = FilenameValidationExecutor()
filename_validation_executor.register([filename_starts_with_a_date])

metadata_validation_executor = MetadataValidationExecutor()
metadata_validation_executor.register([])

content_validation_executor = ContentValidationExecutor()
content_validation_executor.register([])

tags_cleaner = TagsCleaner()

rule_keeper = RuleKeeper(
    post_data_extractor=PostDataExtractor(),
    rule_checkers=[
        filename_validation_executor.validate,
        metadata_validation_executor.validate,
        content_validation_executor.validate,
        tags_cleaner.collect_tags,
    ],
    post_verification_actions=[tags_cleaner.suggest_tag_unification]
)
rule_keeper.verify_rules(posts_directory)
