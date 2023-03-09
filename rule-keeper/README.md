# Rule Keeper

This script takes care ensuring quality of posts created by Solitans

- Validate filename, content and metadata of post
- Recommend tags based on post content
- Suggest tags which could be corrected to use existing one

## Running

To run the script, ensure you do it on Linux/Mac and you have installed Docker.

Then, while your terminal session is in root directory of the project, execute following command:

`./rule-keeper/run.sh`

It will build docker image with needed Python version and all dependencies, and then run it to check all added and
modified post files in your current branch.

## Writing more checks

You are welcome to create more validators and/or tag suggesters.

To create one, create function or class method with following signature:

```python
def my_validator(post_data: PostData) -> RuleCheckResults:
    pass


class MyValidator:
    def my_validator_method(self, post_data: PostData) -> RuleCheckResults:
        pass
```

where PostData represents following structure:

```python
from typing import NamedTuple


class PostData(NamedTuple):
    filename: str
    content: list[str]
    metadata: dict[str, list[str] | str]
```

and `RuleCheckResults`:

```python
from typing import TypedDict, NotRequired


class RuleCheckResults(TypedDict):
    warnings: NotRequired[list[str]]
    errors: NotRequired[list[str]]
    recommendations: NotRequired[list[str]]
```

Check files `validators.py` and `tag_suggesters.py` for examples.

When mentioned class/function is created, add it to the `main.py` under list of `rule_checkers` of RuleKeeper
initialization.

```python

rule_keeper = RuleKeeper(
    post_data_extractor=post_data_extractor,
    rule_checkers=[
        filename_starts_with_a_date,
        existing_tags_suggester.suggest_tags,
        key_tags_suggester.suggest_related_tags,
        # Add new validator/tag suggester here
    ],
    results_printer=print_results,
)
```