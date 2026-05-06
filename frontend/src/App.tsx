import { useState } from "react";

import { ResultsPanel } from "./components/ResultsPanel";
import { StatusCallout } from "./components/StatusCallout";
import { TestGeneratorForm } from "./components/TestGeneratorForm";
import { generateTests } from "./lib/api";
import type { GenerateTestsRequest, GenerateTestsResponse } from "./types";

function App() {
  const [result, setResult] = useState<GenerateTestsResponse | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleGenerate(request: GenerateTestsRequest) {
    setIsLoading(true);
    setError("");
    try {
      const response = await generateTests(request);
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to generate tests.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="app-shell min-h-screen">
      <header className="app-header">
        <div>
          <p className="eyebrow">TestPilot AI</p>
          <h1>AI-powered test case generation for backend APIs and software functions.</h1>
        </div>
      </header>

      {error ? <StatusCallout variant="error" title="Generation failed" message={error} /> : null}

      <div className="workspace">
        <TestGeneratorForm isLoading={isLoading} onSubmit={handleGenerate} />
        <ResultsPanel result={result} />
      </div>
    </main>
  );
}

export default App;
