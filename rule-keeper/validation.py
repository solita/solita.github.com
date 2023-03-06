from post_data_extractor import PostData
from typing import Callable


class ValidationExecutor:
    validators: list[object]

    def __init__(self):
        self.validators = []

    def register(self, validator: object | list[object]):
        if type(validator) == list:
            self.validators = self.validators + validator
        else:
            self.validators.append(validator)


class MetadataValidationExecutor(ValidationExecutor):
    validators: list[Callable[[dict[str, list[str] | str]], list[str]]]

    def validate(self, post_data: PostData):
        errors_list = []
        for validator in self.validators:
            errors_list[0:0] = validator(post_data.metadata)

        return errors_list


class ContentValidationExecutor(ValidationExecutor):
    validators: list[Callable[[list[str]], list[str]]]

    def validate(self, post_data: PostData):
        errors_list = []
        for validator in self.validators:
            errors_list[0:0] = validator(post_data.content)

        return errors_list


class FilenameValidationExecutor(ValidationExecutor):
    validators: list[Callable[[str], list[str]]]

    def validate(self, post_data: PostData):
        errors_list = []
        for validator in self.validators:
            errors_list[0:0] = validator(post_data.filename)

        return errors_list
