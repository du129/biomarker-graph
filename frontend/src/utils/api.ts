const DEFAULT_API_BASE_URL = "http://localhost:8000";

const rawBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim() || DEFAULT_API_BASE_URL;

export const API_BASE_URL = rawBaseUrl.replace(/\/+$/, "");

export function apiUrl(path: string): string {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${API_BASE_URL}${normalizedPath}`;
}
