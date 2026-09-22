import { FormEvent, useState } from "react";
import { ArrowRight, Gamepad2, LockKeyhole, UserRound } from "lucide-react";
import { getCurrentUser, login } from "../services/authService";
import type { User } from "../types/api";

export default function LoginPage({ onLogin }: { onLogin: (user: User) => void }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault(); setSubmitting(true); setError("");
    try { await login(username, password); onLogin(await getCurrentUser()); }
    catch (caught) { setError(caught instanceof Error ? caught.message : "Could not sign in."); }
    finally { setSubmitting(false); }
  }

  return (
    <main className="login-page">
      <section className="login-story">
        <div className="login-brand"><Gamepad2 size={22} /> Flower Power Games</div>
        <div><span className="eyebrow">AI-powered review intelligence</span><h1>Know the table<br />before you play.</h1><p>Real player reviews, distilled into practical insight for your next board game night.</p></div>
        <p className="login-story__foot">Built for players who would rather spend time playing than researching.</p>
      </section>
      <section className="login-form-wrap">
        <form className="login-form" onSubmit={submit}>
          <span className="eyebrow">Welcome back</span><h2>Sign in to your shelf</h2><p>Use your existing account to explore game insights.</p>
          <label htmlFor="username">Username or email</label><div className="input-with-icon"><UserRound size={18} /><input id="username" autoComplete="username" placeholder="username or you@example.com" required value={username} onChange={(event) => setUsername(event.target.value)} /></div>
          <label htmlFor="password">Password</label><div className="input-with-icon"><LockKeyhole size={18} /><input id="password" type="password" autoComplete="current-password" required value={password} onChange={(event) => setPassword(event.target.value)} /></div>
          {error && <p className="form-error" role="alert">{error}</p>}
          <button className="button button--primary login-submit" disabled={submitting}>{submitting ? "Signing in..." : "Sign in"}<ArrowRight size={17} /></button>
        </form>
      </section>
    </main>
  );
}