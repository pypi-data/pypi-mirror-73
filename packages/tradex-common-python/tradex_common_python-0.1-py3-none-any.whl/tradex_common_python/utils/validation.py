from __future__ import annotations
from typing import List, Optional, Any, Generic, Callable, TypeVar

from ..models.Response import ParamError
from ..errors.InvalidParameterError import InvalidParameterError
from ..errors.FieldRequireError import FieldRequireError
from ..errors.FieldLengthError import FieldLengthError
import re
T = TypeVar('T')


class ValidationResult(Generic[T]):
    __slots__ = 'success', 'data', 'params'

    def __init__(self, success: Optional[bool] = False, data: Optional[T] = None,
                 params: Optional[List[ParamError]] = []):
        self.success: bool = success
        self.data: T = data
        self.params: List[ParamError] = params


def create_fail_validation(code: str, message_params: List[str], param_name: str) -> ValidationResult:
    return ValidationResult(False, None, [ParamError(code, param_name, message_params)])


def create_fail_from_error(error: InvalidParameterError) -> ValidationResult:
    return ValidationResult(False, None, error.params)


def create_success_validation(data: T) -> ValidationResult[T]:
    return ValidationResult(True, data, None)


def is_empty(field_value: T) -> bool:
    return field_value is None or field_value == ''


class Validation(Generic[T]):
    def __init__(self, field_value: T, field_name: str, builder: Optional[ValidationBuilder] = None):
        self.builder: ValidationBuilder = builder
        self.results: List[ValidationResult] = []
        self.field_value: T = field_value
        self.field_name: str = field_name
        self.is_required: bool = False
        self.length: int = None
        self.checks: List[Callable[[T, str], ValidationResult]] = []
        self.on_success: Callable[[ValidationResult, List[ValidationResult]], None] = None

    def set_success(self, func: Callable[[ValidationResult, List[ValidationResult]], None]) -> Validation:
        self.on_success = func
        return self

    def set_require(self) -> Validation:
        self.is_required = True
        return self

    def set_length(self, length: int) -> Validation:
        self.length = length
        return self

    def add(self, func: Callable[[T, str], ValidationResult]) -> Validation:
        self.checks.append(func)
        return self

    def adds(self, funcs: List[Callable[[T, str], ValidationResult]]) -> Validation:
        if funcs is not None and len(funcs) > 0:
            self.checks = self.checks + funcs
        return self

    def throw_valid(self, invalid_parameter_error: InvalidParameterError) -> ValidationResult:
        result = self.valid()
        if result is not None and not result.success:
            if invalid_parameter_error is not None:
                invalid_parameter_error.adds(result.params)
                raise invalid_parameter_error
            else:
                raise InvalidParameterError().adds(result.params)
        return result

    def valid(self) -> ValidationResult:
        result: ValidationResult = create_success_validation(self.field_value)
        self.results.append(result)
        if self.is_required:
            if is_empty(self.field_value):
                return create_fail_from_error(FieldRequireError(self.field_name))
        if self.length is not None and (is_empty(self.field_value) or len(self.field_value) != self.length):
            return create_fail_from_error(FieldLengthError(self.field_name, self.length))
        if len(self.checks) > 0:
            if self.is_required or not is_empty(self.field_value):
                for i in range(len(self.checks)):
                    result = self.checks[i](self.field_value, self.field_name)
                    self.results.append(result)
                    if result is not None and not result.success:
                        return result
        if self.on_success is not None:
            self.on_success(result, self.results)
        return result

    def end(self) -> ValidationBuilder:
        return self.builder

    def validate_number(self):
        self.add(lambda field_value, field_name:
                 create_success_validation(field_value) if re.findall('^[0-9]+$', field_value)
                 else create_fail_validation("MUST_BE_NUMBER", [], field_name))
        return self

    def validate_max_len(self, max_len: int):
        self.add(lambda field_value, field_name:
                 create_success_validation(field_value) if field_value is None or len(field_value) <= max_len
                 else create_fail_validation("LENGTH_MUST_BE_LTE_THAN", [str(max_len)], field_name))
        return self

    def require_array(self):
        self.add(lambda field_value, field_name:
                 create_success_validation(field_value) if len(field_value) > 0
                 else create_fail_validation("ARRAY_SHOULD_CONTAIN_AT_LEAST_1_ITEM", [], field_name))
        return self


class ValidationBuilder:
    def __init__(self):
        self.validations: List[Validation] = []
        self.invalid_parameter_error: InvalidParameterError = InvalidParameterError()

    def addValidation(self, field_value: Any, field_name: str) -> Validation:
        validator: Validation = Validation(field_value, field_name, self)
        self.validations.append(validator)
        return validator

    def validate(self):
        error = InvalidParameterError()
        for i in range(len(self.validations)):
            result: ValidationResult = self.validations[i].valid()
            error.adds(result.params)
        check(error)


def build() -> ValidationBuilder:
    return ValidationBuilder()


def validate(field_value: T, field_name: str) -> Validation:
    return Validation(field_value, field_name)


def check(error: InvalidParameterError):
    if len(error.params) > 0:
        raise error
