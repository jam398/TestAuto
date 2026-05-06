from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator


class TestFramework(str, Enum):
    __test__ = False

    PYTEST = "pytest"
    JEST_SUPERTEST = "jest_supertest"


class TestCaseType(str, Enum):
    __test__ = False

    API_ENDPOINT = "api_endpoint"
    VALIDATION = "validation"
    NEGATIVE = "negative"
    EDGE_CASE = "edge_case"
    BOUNDARY = "boundary"
    CONTRACT_SCHEMA = "contract_schema"
    ERROR_HANDLING = "error_handling"
    SMOKE = "smoke"
    UNIT = "unit"
    INTEGRATION = "integration"


TestType = TestCaseType


DEFAULT_SELECTED_TEST_TYPES = [
    TestType.API_ENDPOINT,
    TestType.VALIDATION,
    TestType.NEGATIVE,
    TestType.EDGE_CASE,
    TestType.CONTRACT_SCHEMA,
]


def default_selected_test_types() -> list[TestType]:
    return list(DEFAULT_SELECTED_TEST_TYPES)


class ProviderMode(str, Enum):
    MOCK = "mock"
    OPENAI = "openai"


class GenerateTestsRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project_context: str = Field(..., min_length=30)
    target_name: str | None = None
    test_framework: TestFramework = TestFramework.PYTEST
    selected_test_types: list[TestType] = Field(default_factory=default_selected_test_types)
    extra_instructions: str | None = None

    @field_validator("project_context")
    @classmethod
    def project_context_must_have_content(cls, value: str) -> str:
        normalized = value.strip()
        if len(normalized) < 30:
            raise ValueError("project_context must contain at least 30 non-whitespace characters")
        return normalized

    @field_validator("target_name", "extra_instructions")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("selected_test_types")
    @classmethod
    def default_empty_selected_test_types(cls, value: list[TestType]) -> list[TestType]:
        return value or default_selected_test_types()


class TestCase(BaseModel):
    __test__ = False

    model_config = ConfigDict(extra="forbid")

    name: str
    type: TestCaseType
    description: str
    input: str
    expected_result: str
    reason: str


class EvidenceSnippet(BaseModel):
    model_config = ConfigDict(extra="forbid")

    snippet: str
    source: str


class GenerateTestsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider_mode: ProviderMode
    selected_test_types: list[TestType]
    summary: str
    test_cases: list[TestCase]
    generated_code: str
    evidence: list[EvidenceSnippet]
    warnings: list[str]

    @field_validator("generated_code")
    @classmethod
    def generated_code_must_have_content(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("generated_code must contain starter test code")
        return value
