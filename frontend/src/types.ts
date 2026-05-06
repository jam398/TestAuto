export type TestFramework = "pytest" | "jest_supertest";

export type TestType =
  | "api_endpoint"
  | "validation"
  | "negative"
  | "edge_case"
  | "boundary"
  | "contract_schema"
  | "error_handling"
  | "smoke"
  | "unit"
  | "integration";

export type TestCaseType = TestType;
export type ProviderMode = "mock" | "openai";

export interface GenerateTestsRequest {
  project_context: string;
  target_name?: string;
  test_framework: TestFramework;
  selected_test_types: TestType[];
  extra_instructions?: string;
}

export interface TestCase {
  name: string;
  type: TestCaseType;
  description: string;
  input: string;
  expected_result: string;
  reason: string;
}

export interface EvidenceSnippet {
  snippet: string;
  source: string;
}

export interface GenerateTestsResponse {
  provider_mode: ProviderMode;
  selected_test_types: TestType[];
  summary: string;
  test_cases: TestCase[];
  generated_code: string;
  evidence: EvidenceSnippet[];
  warnings: string[];
}
