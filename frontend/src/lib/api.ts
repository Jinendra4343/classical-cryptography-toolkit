import type { CipherInfo, CipherResponse, CompareRow, CipherId } from "../types";

export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
    ...init,
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.detail || "The API could not complete that operation.");
  return body as T;
}

export const getCiphers = () => request<CipherInfo[]>("/ciphers");
export const runCipher = (operation: "encrypt" | "decrypt", algorithm: CipherId, text: string, key: string) =>
  request<CipherResponse>(`/${operation}`, { method: "POST", body: JSON.stringify({ algorithm, text, key }) });
export const generateKey = (algorithm: CipherId, text: string) => request<{ key: string }>(`/keys/generate?algorithm=${algorithm}&text=${encodeURIComponent(text)}`, { method: "POST" });
export const compareCiphers = (text: string, algorithms: CipherId[], keys: Record<string, string>) =>
  request<{ results: CompareRow[]; runs: number; note: string }>("/compare", { method: "POST", body: JSON.stringify({ text, algorithms, keys, runs: 15 }) });

export async function processFile(operation: "encrypt" | "decrypt", file: File, algorithm: CipherId, key: string) {
  const form = new FormData();
  form.append("file", file);
  form.append("algorithm", algorithm);
  form.append("key", key);
  const response = await fetch(`${API_URL}/files/${operation}`, { method: "POST", body: form });
  const body = await response.json();
  if (!response.ok) throw new Error(body.detail || "The file could not be processed.");
  return body as CipherResponse & { filename: string };
}
