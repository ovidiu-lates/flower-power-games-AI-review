import { useEffect, useState } from "react";
import { BrowserRouter, Navigate, Outlet, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import DiscoverPage from "./pages/DiscoverPage";
import GameDetailPage from "./pages/GameDetailPage";
import Login from "./pages/Login";
import { getCurrentUser, logout } from "./services/authService";
import { getAccessToken } from "./services/apiClient";
import type { User } from "./types/api";

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [checkingAuth, setCheckingAuth] = useState(Boolean(getAccessToken()));

  useEffect(() => {
    if (!getAccessToken()) {
      setCheckingAuth(false);
      return;
    }

    getCurrentUser()
      .then(setUser)
      .catch(() => {
        logout();
        setUser(null);
      })
      .finally(() => setCheckingAuth(false));
  }, []);

  if (checkingAuth) {
    return (
      <div className="app-loading">
        <span className="loader" />
        <p>Opening the game shelf...</p>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/login"
          element={
            user
              ? <Navigate to="/discover" replace />
              : <Login />
          }
        />

        <Route
          element={
            user
              ? <AppLayout user={user} />
              : <Navigate to="/login" replace />
          }
        >
          <Route path="/discover" element={<DiscoverPage />} />
          <Route path="/games/:gameId" element={<GameDetailPage />} />
        </Route>

        <Route
          path="*"
          element={<Navigate to={user ? "/discover" : "/login"} replace />}
        />
      </Routes>
    </BrowserRouter>
  );
}

function AppLayout({ user }: { user: User }) {
  return (
    <>
      <Navbar user={user} />
      <Outlet />
    </>
  );
}

export default App;