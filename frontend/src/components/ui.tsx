import type { ButtonHTMLAttributes, ReactNode } from "react";

export function Button({ children, variant = "primary", className = "", ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: "primary" | "secondary" | "ghost" | "danger"; children: ReactNode }) {
  return <button className={`button button-${variant} ${className}`} {...props}>{children}</button>;
}

export function Panel({ children, className = "", id }: { children: ReactNode; className?: string; id?: string }) {
  return <section id={id} className={`panel ${className}`}>{children}</section>;
}

export function Badge({ children, tone = "default" }: { children: ReactNode; tone?: "default" | "green" | "violet" | "amber" }) {
  return <span className={`badge badge-${tone}`}>{children}</span>;
}
