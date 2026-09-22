import { BrowserRouter, Navigate, Outlet, Route, Routes, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import Navbar from "./components/ui/Navbar";
import { getCurrentUser, logout } from "./services/auth";
import Discover from "./pages/Discover";
import GameDetailPage from "./pages/GameDetailPage";
import Login from "./pages/Login";
import type { User } from "./types/game";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/discover" element={<Discover />} />
        <Route element={<AuthenticatedLayout />}>
          <Route path="/games/:gameId" element={<GameDetailPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/discover" replace />} />
      </Routes>
    </BrowserRouter>
  );
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