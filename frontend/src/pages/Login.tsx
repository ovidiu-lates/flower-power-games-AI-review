import { useState, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import Field from '../components/ui/Field';
import { ApiError } from '../lib/api';
import { login, register, saveSession } from '../services/auth';
import type { AuthMode } from '../types/auth';

export default function Login() {
    const [mode, setMode] = useState<AuthMode>('login');

    const [values, setValues] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
    });

    const [error, setError] = useState<string | null>(null);
    const [message, setMessage] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();

    function update(field: keyof typeof values, value: string) {
        setValues((current) => ({
            ...current,
            [field]: value,
        }));
    }

    function changeMode(nextMode: AuthMode) {
        setMode(nextMode);
        setError(null);
        setMessage(null);
    }

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();

        setError(null);
        setMessage(null);

        if (values.password.length < 8) {
            setError('Password must have at least 8 characters.');
            return;
        }

        if (
            mode === 'register' &&
            values.password !== values.confirmPassword
        ) {
            setError('Passwords do not match.');
            return;
        }

        setLoading(true);

        try {
            if (mode === 'login') {
                const response = await login(
                    values.username,
                    values.password,
                );

                saveSession(response);
                navigate('/discover');
            } else {
                await register(
                    values.username,
                    values.email,
                    values.password,
                );

                setMode('login');
                setValues({
                    username: '',
                    email: '',
                    password: '',
                    confirmPassword: '',
                });

                setMessage(
                    'Account created successfully. You can now log in.',
                );
            }
        } catch (caught) {
            if (caught instanceof ApiError || caught instanceof Error) {
                setError(caught.message);
            } else {
                setError('Request failed.');
            }
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className= "login-page" >
        <div className="login-container" >
            <header className="login-brand" >
                <div className="login-brand-icon" >* </div>

                    < div >
                    <p className="login-brand-name" >
                        Flower Power Games
                            </p>
                            < p className = "login-brand-subtitle" >
                                AI Review
                                    </p>
                                    </div>
                                    </header>

                                    < section className = "login-card" >
                                        <div className="login-tabs" >
                                            <button
              type="button"
    className = {`login-tab ${mode === 'login' ? 'active' : ''
        }`
}
onClick = {() => changeMode('login')}
            >
    Log in
    </button>

    < button
type = "button"
className = {`login-tab ${mode === 'register' ? 'active' : ''
    }`}
onClick = {() => changeMode('register')}
            >
    Create account
        </button>
        </div>

        < h1 className = "login-title" >
        { mode === 'login'
            ? 'Welcome back'
            : 'Join Flower Power'}
</h1>

    < p className = "login-description" >
    { mode === 'login'
        ? 'Find your next board game through real player insights.'
        : 'Start discovering games through AI-analyzed reviews.'}
</p>

{
    error && (
        <div className="login-error" role = "alert" >
        { error }
            </div>
          )
}

{
    message && (
        <div className="login-message" role = "status" >
        { message }
            </div>
          )
}

<form
            className="login-form"
onSubmit = { handleSubmit }
    >
    <Field
              label="Username"
type = "text"
placeholder = ""
value = { values.username }
onChange = {(value) => update('username', value)}
autoComplete = "username"
    />

{ mode === 'register' && (
        <Field
                label="Email"
type = "email"
placeholder = "you@example.com"
value = { values.email }
onChange = {(value) => update('email', value)}
autoComplete = "email"
    />
            )}

<Field
              label="Password"
type = "password"
placeholder = "Min. 8 characters"
value = { values.password }
onChange = {(value) => update('password', value)}
autoComplete = {
    mode === 'login'
    ? 'current-password'
    : 'new-password'
              }
minLength = { 8}
    />

{ mode === 'register' && (
        <Field
                label="Confirm password"
type = "password"
placeholder = "Repeat password"
value = { values.confirmPassword }
onChange = {(value) =>
update('confirmPassword', value)
                }
autoComplete = "new-password"
minLength = { 8}
    />
            )}

<button
              type="submit"
className = "login-submit"
disabled = { loading }
    >
{
    loading
    ? 'Please wait...'
        : mode === 'login'
            ? 'Log in'
            : 'Create account'
}
    </button>
    </form>

    < p className = "login-footer" >
    { mode === 'login'
        ? "Don't have an account?"
        : 'Already have an account?'}{ ' ' }
<button
              type="button"
onClick = {() =>
changeMode(
    mode === 'login'
        ? 'register'
        : 'login',
)
              }
            >
{ mode === 'login'
    ? 'Create one free'
    : 'Log in'}
</button>
    </p>
    </section>
    </div>
    </div>
  );
}