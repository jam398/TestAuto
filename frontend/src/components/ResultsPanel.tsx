import { AlertTriangle, FileText } from "lucide-react";

import type { GenerateTestsResponse, TestCaseType } from "../types";
import { CodeBlock } from "./CodeBlock";

interface ResultsPanelProps {
  result: GenerateTestsResponse | null;
}

const typeLabels: Record<TestCaseType, string> = {
  api_endpoint: "API Endpoint",
  validation: "Validation",
  negative: "Negative",
  edge_case: "Edge Case",
  boundary: "Boundary",
  contract_schema: "Contract / Schema",
  error_handling: "Error Handling",
  smoke: "Smoke",
  unit: "Unit",
  integration: "Integration"
};

const providerLabels: Record<GenerateTestsResponse["provider_mode"], string> = {
  mock: "Mock mode",
  openai: "OpenAI mode"
};

export function ResultsPanel({ result }: ResultsPanelProps) {
  if (!result) {
    return (
      <section className="results-panel results-panel--empty">
        <FileText size={24} aria-hidden="true" />
        <h2>Results</h2>
        <p>Generated test plans will appear here.</p>
      </section>
    );
  }

  return (
    <section className="results-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Output</p>
          <h2>Review generated plan</h2>
        </div>
        <span className={`provider-badge provider-badge--${result.provider_mode}`}>
          {providerLabels[result.provider_mode]}
        </span>
      </div>

      <section className="result-section">
        <h3>Summary</h3>
        <div className="selected-type-list" aria-label="Selected test types">
          {result.selected_test_types.map((testType) => (
            <span className={`type-badge type-badge--${testType}`} key={testType}>
              {typeLabels[testType]}
            </span>
          ))}
        </div>
        <p>{result.summary}</p>
      </section>

      <section className="result-section">
        <h3>Test cases</h3>
        <div className="test-case-list">
          {result.test_cases.map((testCase) => (
            <article className="test-case" key={`${testCase.type}-${testCase.name}`}>
              <div className="test-case__header">
                <span className={`type-badge type-badge--${testCase.type}`}>{typeLabels[testCase.type]}</span>
                <h4>{testCase.name}</h4>
              </div>
              <p>{testCase.description}</p>
              <dl>
                <div>
                  <dt>Expected</dt>
                  <dd>{testCase.expected_result}</dd>
                </div>
                <div>
                  <dt>Why</dt>
                  <dd>{testCase.reason}</dd>
                </div>
              </dl>
            </article>
          ))}
        </div>
      </section>

      <section className="result-section">
        <CodeBlock code={result.generated_code} />
      </section>

      <section className="result-section">
        <h3>Evidence</h3>
        <ul className="evidence-list">
          {result.evidence.map((item, index) => (
            <li key={`${item.source}-${index}`}>
              <span>{item.source}</span>
              <p>{item.snippet}</p>
            </li>
          ))}
        </ul>
      </section>

      {result.warnings.length ? (
        <section className="warning-list" aria-label="Warnings">
          <AlertTriangle size={18} aria-hidden="true" />
          <div>
            <h3>Warnings</h3>
            <ul>
              {result.warnings.map((warning) => (
                <li key={warning}>{warning}</li>
              ))}
            </ul>
          </div>
        </section>
      ) : null}
    </section>
  );
}
