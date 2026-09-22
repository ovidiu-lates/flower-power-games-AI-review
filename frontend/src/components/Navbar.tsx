import { Flower2, LogOut, Search, UserRound } from "lucide-react";
import { FormEvent, useState } from "react";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { logout } from "../services/auth";
import type { User } from "../types/api";

export default function Navbar({ user }: { user: User }) {
  const navigate = useNavigate();
  const [search, setSearch] = useState("");
  const [profileOpen, setProfileOpen] = useState(false);

  function submitSearch(event: FormEvent) {
    event.preventDefault();
    navigate(`/discover${search.trim() ? `?search=${encodeURIComponent(search.trim())}` : ""}`);
  }

  function signOut() {
    logout();
    navigate("/login", { replace: true });
  }

  return (
    <nav className="navbar">
      <div className="navbar__inner">
        <Link to="/discover" className="brand" aria-label="Flower Power Games home">
          <span className="brand__mark"><Flower2 size={19} /></span>
          <span className="brand__name">Flower Power <strong>Games · AI Review</strong></span>
        </Link>

        <div className="navbar__links">
          <NavLink to="/discover" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>Discover</NavLink>
        </div>

        <form className="nav-search" onSubmit={submitSearch}>
          <Search size={17} aria-hidden="true" />
          <input
            type="search"
            aria-label="Search board games"
            placeholder="Search board games..."
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />
        </form>

        <div className="profile-menu">
          <button className="profile-button" onClick={() => setProfileOpen((open) => !open)} aria-expanded={profileOpen}>
            <UserRound size={18} />
            <span>{user.username}</span>
          </button>
          {profileOpen && (
            <div className="profile-popover">
              <div className="profile-popover__identity">
                <strong>{user.username}</strong>
                <span>{user.email}</span>
              </div>
              <button onClick={signOut}><LogOut size={16} /> Sign out</button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}