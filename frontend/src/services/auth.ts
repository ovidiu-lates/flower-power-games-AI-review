import { apiRequest } from '../lib/api';
import type { AuthResponse } from '../types/auth';

export const login = (email: string, password: string) =>
    apiRequest<AuthResponse>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({
            username: email,
            password,
        }),
    });

export const register = (
    fullName: string,
    email: string,
    password: string,
) =>
    apiRequest<AuthResponse>('/auth/register', {
        method: 'POST',
        body: JSON.stringify({
            username: fullName,
            email,
            password,
        }),
    });

export function saveSession(response: AuthResponse) {
    localStorage.setItem('access_token', response.access_token);
    localStorage.setItem('current_user', JSON.stringify(response.user ?? {}));
}