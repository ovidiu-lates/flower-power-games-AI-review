import { apiRequest } from "./api";
import type { User } from "../types/game";

export function getCurrentUser(_token?: string) {
  return apiRequest<User>("/auth/me");
}
