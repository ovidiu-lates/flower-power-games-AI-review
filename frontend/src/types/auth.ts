import type { User } from './game';

export type AuthMode = 'login' | 'register';

export interface LoginRequest { email: string; password: string; }
export interface RegisterRequest extends LoginRequest { fullName: string; confirmPassword: string; }
export interface AuthResponse { access_token: string; token_type: string; user?: User; }
export interface ApiErrorResponse {
    detail?: string;
    error?: { code?: string; message?: string; requestId?: string };
}
