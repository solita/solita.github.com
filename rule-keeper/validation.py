
class IMetadataValidator:
    def validate(self, metadata: dict[str, list[str] | str]) -> list[str]:
        pass


class IContentValidator:
    def validate(self, content: list[str]) -> list[str]:
        pass


class IFilenameValidator:
    def validate(self, filename: str) -> list[str]:
        pass


class ValidatorExecutor:
    validator_registry: list[object]
    validator_type: str
    errors_list = []

    def __init__(self):
        self.validator_registry = []

    def register(self, validator: object):
        pass


class MetadataValidatorExecutor(ValidatorExecutor):
    validator_type = "metadata"
    validator_registry: list[IMetadataValidator]

    def validate(self, metadata: dict[str, list[str] | str]):
        for validator in self.validator_registry:
            self.errors_list[0:0] = validator.validate(metadata)


class ContentValidatorExecutor(ValidatorExecutor):
    validator_type = "content"
    validator_registry: list[IContentValidator]

    def validate(self, content: list[str]):
        for validator in self.validator_registry:
            self.errors_list[0:0] = validator.validate(content)


class FilenameValidatorExecutor(ValidatorExecutor):
    validator_type = "filename"
    validator_registry: list[IFilenameValidator]

    def validate(self, filename: str):
        for validator in self.validator_registry:
            self.errors_list[0:0] = validator.validate(filename)
