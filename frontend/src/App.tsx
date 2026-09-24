import { BrowserRouter, Navigate, Outlet, Route, Routes, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import Navbar from "./components/ui/Navbar";
import { getCurrentUser, logout } from "./services/auth";
import Discover from "./pages/Discover";
import GameDetailPage from "./pages/GameDetailPage";
import Login from "./pages/Login";
import MyReviews from "./pages/MyReviews";
import type { User } from "./types/game";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<RequireAuthentication />}>
          <Route path="/discover" element={<Discover />} />
        </Route>
        <Route element={<AuthenticatedLayout />}>
          <Route path="/games/:gameId" element={<GameDetailPage />} />
          <Route path="/my-reviews" element={<MyReviews />} />
        </Route>
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

function RequireAuthentication() {
  const navigate = useNavigate();
  const [checking, setChecking] = useState(true);
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    let active = true;

    void getCurrentUser()
      .then(() => {
        if (active) {
          setAuthenticated(true);
        }
      })
      .catch(() => {
        logout();
        if (active) {
          setAuthenticated(false);
          navigate("/login", { replace: true });
        }
      })
      .finally(() => {
        if (active) {
          setChecking(false);
        }
      });

    return () => {
      active = false;
    };
  }, [navigate]);

  if (checking) {
    return <main className="page-shell state-message"><span className="loader" /> Checking your session...</main>;
  }

  return authenticated ? <Outlet /> : null;
}

function AuthenticatedLayout() {
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null);
  const [search, setSearch] = useState("");

  useEffect(() => {
    void getCurrentUser()
      .then(setUser)
      .catch(() => {
        logout();
        navigate("/login", { replace: true });
      });
  }, [navigate]);

  function handleSearchChange(value: string) {
    setSearch(value);
    navigate(`/discover${value.trim() ? `?search=${encodeURIComponent(value.trim())}` : ""}`);
  }

  return (
    <>
      <Navbar
        user={user}
        search={search}
        onSearchChange={handleSearchChange}
      />
      <Outlet />
    </>
  );
}

export default App;