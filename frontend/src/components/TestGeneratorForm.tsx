import { ChevronDown, Loader2, Send } from "lucide-react";
import { FormEvent, useState } from "react";

import type { GenerateTestsRequest, TestFramework, TestType } from "../types";

const SAMPLE_CONTEXT = `POST /api/debts

Creates a new debt record for a user.

Required fields:
- name: string, required
- principal: number, must be greater than 0
- apr: number, must be between 0 and 100
- minimumPayment: number, must be greater than 0

Successful response:
- 201 Created
- returns id, name, principal, apr, minimumPayment, createdAt

Validation errors:
- 400 Bad Request
- returns a message describing invalid fields`;

const TEST_TYPE_OPTIONS: Array<{ value: TestType; label: string; description: string }> = [
  {
    value: "api_endpoint",
    label: "API Endpoint Tests",
    description: "HTTP method, route, status code, and response behavior."
  },
  {
    value: "validation",
    label: "Validation Tests",
    description: "Required fields, invalid values, types, formats, and input rules."
  },
  {
    value: "negative",
    label: "Negative Tests",
    description: "Bad, unexpected, malformed, or unsupported input."
  },
  {
    value: "edge_case",
    label: "Edge Case Tests",
    description: "Unusual but possible inputs like empty strings, zero, or special values."
  },
  {
    value: "boundary",
    label: "Boundary Tests",
    description: "Exact limits and just-outside values for numeric or length constraints."
  },
  {
    value: "contract_schema",
    label: "Contract / Schema Tests",
    description: "Expected response fields, types, and structure."
  },
  {
    value: "error_handling",
    label: "Error Handling Tests",
    description: "Clean failure behavior for documented error paths."
  },
  {
    value: "smoke",
    label: "Smoke Tests",
    description: "Basic sanity checks for the most important behavior."
  },
  {
    value: "unit",
    label: "Unit Tests",
    description: "One function, method, or module in isolation."
  },
  {
    value: "integration",
    label: "Integration Tests",
    description: "Multiple documented parts or workflow steps working together."
  }
];

const DEFAULT_SELECTED_TEST_TYPES: TestType[] = [
  "api_endpoint",
  "validation",
  "negative",
  "edge_case",
  "contract_schema"
];

interface TestGeneratorFormProps {
  isLoading: boolean;
  onSubmit: (request: GenerateTestsRequest) => void;
}

export function TestGeneratorForm({ isLoading, onSubmit }: TestGeneratorFormProps) {
  const [projectContext, setProjectContext] = useState(SAMPLE_CONTEXT);
  const [targetName, setTargetName] = useState("");
  const [testFramework, setTestFramework] = useState<TestFramework>("pytest");
  const [extraInstructions, setExtraInstructions] = useState("Assume validation errors return JSON with a top-level message field.");
  const [selectedTestTypes, setSelectedTestTypes] = useState<Set<TestType>>(
    () => new Set(DEFAULT_SELECTED_TEST_TYPES)
  );
  const [isTestTypeMenuOpen, setIsTestTypeMenuOpen] = useState(false);
  const [validationMessage, setValidationMessage] = useState("");

  const selectedCountLabel = selectedTestTypes.size ? `${selectedTestTypes.size} selected` : "Defaults will apply";

  function toggleTestType(value: TestType) {
    setSelectedTestTypes((current) => {
      const next = new Set(current);
      if (next.has(value)) {
        next.delete(value);
      } else {
        next.add(value);
      }
      return next;
    });
  }

  function selectedTestTypeValues(): TestType[] {
    return TEST_TYPE_OPTIONS.map((option) => option.value).filter((value) => selectedTestTypes.has(value));
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedContext = projectContext.trim();
    if (trimmedContext.length < 30) {
      setValidationMessage("Project context must be at least 30 characters.");
      return;
    }
    setValidationMessage("");
    onSubmit({
      project_context: trimmedContext,
      target_name: targetName.trim() || undefined,
      test_framework: testFramework,
      selected_test_types: selectedTestTypeValues(),
      extra_instructions: extraInstructions.trim() || undefined
    });
  }

  return (
    <form className="tool-panel" onSubmit={handleSubmit}>
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Context</p>
          <h2>Generate tests</h2>
        </div>
      </div>

      <label className="field field--stacked">
        <span>Project context</span>
        <textarea
          value={projectContext}
          onChange={(event) => setProjectContext(event.target.value)}
          spellCheck={false}
        />
      </label>

      <div className="form-grid">
        <label className="field">
          <span>Target <em>optional</em></span>
          <input
            placeholder="Example: GET /api/users/{id}"
            value={targetName}
            onChange={(event) => setTargetName(event.target.value)}
          />
          <small>Primary focus when provided. Leave blank if the context has one clear target.</small>
        </label>

        <label className="field">
          <span>Framework</span>
          <select value={testFramework} onChange={(event) => setTestFramework(event.target.value as TestFramework)}>
            <option value="pytest">Pytest</option>
            <option value="jest_supertest">Jest / Supertest</option>
          </select>
        </label>
      </div>

      <div className="test-type-select">
        <span className="field-label">Choose test types</span>
        <button
          aria-expanded={isTestTypeMenuOpen}
          className="test-type-select__trigger"
          onClick={() => setIsTestTypeMenuOpen((current) => !current)}
          type="button"
        >
          <span>{selectedCountLabel}</span>
          <ChevronDown aria-hidden="true" size={18} />
        </button>

        {isTestTypeMenuOpen ? (
          <div className="test-type-menu">
            {TEST_TYPE_OPTIONS.map((option) => (
              <label className="test-type-option" key={option.value}>
                <input
                  checked={selectedTestTypes.has(option.value)}
                  onChange={() => toggleTestType(option.value)}
                  type="checkbox"
                />
                <span>
                  <strong>{option.label}</strong>
                  <small>{option.description}</small>
                </span>
              </label>
            ))}
          </div>
        ) : null}
      </div>

      <label className="field field--stacked">
        <span>Additional instructions</span>
        <textarea
          className="textarea--short"
          value={extraInstructions}
          onChange={(event) => setExtraInstructions(event.target.value)}
          spellCheck={false}
        />
      </label>

      {validationMessage ? <p className="form-error">{validationMessage}</p> : null}

      <button className="primary-button" type="submit" disabled={isLoading}>
        {isLoading ? <Loader2 className="spin" size={18} aria-hidden="true" /> : <Send size={18} aria-hidden="true" />}
        <span>{isLoading ? "Generating" : "Generate Tests"}</span>
      </button>
    </form>
  );
}
