import type { GenerateTestsRequest, GenerateTestsResponse } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

function formatErrorDetail(payload: unknown): string {
  if (typeof payload === "string") {
    return payload;
  }
  if (payload && typeof payload === "object" && "detail" in payload) {
    const detail = (payload as { detail: unknown }).detail;
    if (typeof detail === "string") {
      return detail;
    }
    if (Array.isArray(detail)) {
      return detail
        .map((item) => {
          if (item && typeof item === "object" && "msg" in item) {
            return String((item as { msg: unknown }).msg);
          }
          return String(item);
        })
        .join(" ");
    }
  }
  return "Unable to generate tests. Check the backend and try again.";
}

export async function generateTests(request: GenerateTestsRequest): Promise<GenerateTestsResponse> {
  const response = await fetch(`${API_BASE_URL}/api/generate-tests`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(request)
  });

  const payload = (await response.json().catch(() => null)) as unknown;
  if (!response.ok) {
    throw new Error(formatErrorDetail(payload));
  }
  return payload as GenerateTestsResponse;
}
