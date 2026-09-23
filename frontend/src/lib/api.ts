import type { ApiErrorResponse } from '../types/auth';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api';
const ACCESS_TOKEN_KEY = 'access_token';

export class ApiError extends Error {
    constructor(public status: number, body: ApiErrorResponse) {
        super(body.error?.message ?? body.detail ?? 'The request failed.');
        this.name = 'ApiError';
    }
}

export function getAccessToken(): string | null {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function setAccessToken(token: string): void {
    localStorage.setItem(ACCESS_TOKEN_KEY, token);
}

export function clearAccessToken(): void {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem('current_user');
}

export async function apiRequest<T>(path: string, options: RequestInit = {}): Promise<T> {
    let response: Response;
    try {
        const token = getAccessToken();
        response = await fetch(`${API_BASE_URL}${path}`, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...(token ? { Authorization: `Bearer ${token}` } : {}),
                ...(options.headers ?? {}),
            },
        });
    } catch {
        throw new Error('Unable to connect to the server.');
    }

    const body = await response.json().catch(() => ({}));
    if (!response.ok) throw new ApiError(response.status, body as ApiErrorResponse);
    return body as T;
}
