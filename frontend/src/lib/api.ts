import type { ApiErrorResponse } from '../types/auth';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api';

export class ApiError extends Error {
    constructor(public status: number, body: ApiErrorResponse) {
        super(body.error?.message ?? 'The request failed.');
        this.name = 'ApiError';
    }
}

export async function apiRequest<T>(path: string, options: RequestInit = {}): Promise<T> {
    let response: Response;
    try {
        response = await fetch(`${API_BASE_URL}${path}`, {
            ...options,
            headers: { 'Content-Type': 'application/json', ...(options.headers ?? {}) },
        });
    } catch {
        throw new Error('Unable to connect to the server.');
    }

    const body = await response.json().catch(() => ({}));
    if (!response.ok) throw new ApiError(response.status, body as ApiErrorResponse);
    return body as T;
}
