export type CipherId = "caesar" | "monoalphabetic" | "playfair" | "hill" | "vigenere" | "otp" | "rail-fence" | "columnar";

export interface CipherInfo {
  id: CipherId;
  name: string;
  category: "Substitution" | "Transposition";
  key_hint: string;
  default_key: string;
  description: string;
}

export interface CipherResponse {
  result: string;
  algorithm: string;
  operation: string;
  elapsed_ms: number;
  input_length: number;
  output_length: number;
  normalized_length: number;
  metadata: Record<string, unknown>;
}

export interface CompareRow {
  algorithm: CipherId;
  status: string;
  error?: string;
  encrypt_ms: number | null;
  decrypt_ms: number | null;
  output_length: number;
  metadata?: Record<string, unknown>;
}

export interface HistoryItem {
  id: string;
  timestamp: string;
  algorithm: string;
  operation: string;
  inputLength: number;
  outputLength: number;
  duration: number;
  success: boolean;
}
