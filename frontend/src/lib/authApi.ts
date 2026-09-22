import type { User } from "../types/game";

export async function getCurrentUser(token: string): Promise<User> {
  const response = await fetch("/api/auth/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch current user: ${response.status}`);
  }

  return response.json();
}