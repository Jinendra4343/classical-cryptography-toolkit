import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import App from "./App";

describe("toolkit shell", () => {
  it("renders the dashboard identity and working navigation", () => {
    render(<App />);
    expect(screen.getByText("Classical cryptography, made visible.")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /encrypt & decrypt/i })).toBeInTheDocument();
  });
});
