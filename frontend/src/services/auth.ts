import {
    apiRequest,
    clearAccessToken,
    setAccessToken,
} from '../lib/api';
import type { User } from '../types/game';
import type { AuthResponse } from '../types/auth';

export const login = (username: string, password: string) =>
    apiRequest<AuthResponse>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({
            username,
            password,
        }),
    });

export const register = (
    username: string,
    email: string,
    password: string,
) =>
    apiRequest<User>('/auth/register', {
        method: 'POST',
        body: JSON.stringify({
            username,
            email,
            password,
        }),
    });

export function saveSession(response: AuthResponse) {
    setAccessToken(response.access_token);
    if (response.user) {
        saveCurrentUser(response.user);
    }
}

export function getCurrentUser() {
    return apiRequest<User>('/auth/me');
}

export function saveCurrentUser(user: User): void {
    localStorage.setItem('current_user', JSON.stringify(user));
}

export function logout() {
    clearAccessToken();
}