import { AlertTriangle, Info } from "lucide-react";

interface StatusCalloutProps {
  variant: "error" | "info" | "warning";
  title: string;
  message: string;
}

export function StatusCallout({ variant, title, message }: StatusCalloutProps) {
  const Icon = variant === "error" || variant === "warning" ? AlertTriangle : Info;

  return (
    <div className={`status-callout status-callout--${variant}`} role={variant === "error" ? "alert" : "status"}>
      <Icon aria-hidden="true" size={18} />
      <div>
        <strong>{title}</strong>
        <p>{message}</p>
      </div>
    </div>
  );
}
