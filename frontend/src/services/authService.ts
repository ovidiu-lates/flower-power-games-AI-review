import type { User } from "../types/api";
import { apiRequest, clearAccessToken, setAccessToken } from "./apiClient";

interface TokenResponse {
  access_token: string;
  token_type: string;
}

export async function login(username: string, password: string) {
  const response = await apiRequest<TokenResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
  setAccessToken(response.access_token);
  return response;
}

export function getCurrentUser() {
  return apiRequest<User>("/auth/me");
}

export function logout() {
  clearAccessToken();
}