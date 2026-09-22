import { useState } from "react";
import { useNavigate } from "react-router-dom";
import type { User } from "../../types/game";

type NavbarProps = {
	user: User | null;
	search: string;
	onSearchChange: (value: string) => void;
	onSignOut?: () => void;
};

function getInitials(user: User | null) {
	if (!user) {
		return "--";
	}

	return user.username.slice(0, 2).toUpperCase();
}

export default function Navbar({ user, search, onSearchChange, onSignOut }: NavbarProps) {
	const [profileOpen, setProfileOpen] = useState(false);
	const navigate = useNavigate();

	const handleSignOut = () => {
		setProfileOpen(false);
		localStorage.removeItem("access_token");
		onSignOut?.();
		navigate("/login");
	};

	return (
		<nav className="navbar">
			<div className="navbar-inner">
				<a href="/discover" className="navbar-logo" aria-label="Flower Power Games AI Review">
					<div className="navbar-logo-mark">✿</div>
					<span>
						Flower Power<br />
						<small>Games - AI Review</small>
					</span>
				</a>

				<div className="navbar-links" aria-label="Primary navigation">
					<a className="navbar-link active" href="/discover">
						Discover
					</a>
					<span className="navbar-link disabled" title="No profile reviews endpoint exists yet">
						My Reviews
					</span>
				</div>

				<div className="navbar-search">
					<svg aria-hidden="true" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
					</svg>
					<input
						type="text"
						placeholder="Search board games..."
						value={search}
						onChange={(event) => onSearchChange(event.target.value)}
					/>
				</div>

				<div className="navbar-spacer" />

				<div className="profile-menu">
					<button
						type="button"
						onClick={() => setProfileOpen((open) => !open)}
						className="profile-button"
						aria-expanded={profileOpen}
						aria-label="Open profile menu"
					>
						<span>{getInitials(user)}</span>
					</button>

					{profileOpen && (
						<div className="profile-dropdown">
							<div className="profile-summary">
								<p>{user?.username ?? "Not signed in"}</p>
								<small>{user?.email ?? "Sign in to use protected endpoints"}</small>
							</div>
							<button type="button" onClick={handleSignOut}>
								Sign out
							</button>
						</div>
					)}
				</div>
			</div>
		</nav>
	);
}
