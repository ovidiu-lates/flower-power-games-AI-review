import { BrowserRouter, Navigate, Outlet, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import DiscoverPage from "./pages/DiscoverPage";
import GameDetailPage from "./pages/GameDetailPage";
import Login from "./pages/Login";
import type { User } from "./types/api";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route element={<ProtectedLayout />}>
          <Route path="/discover" element={<DiscoverPage />} />
          <Route path="/games/:gameId" element={<GameDetailPage />} />
        </Route>

        <Route
          path="*"
          element={
            <Navigate
              to={hasSession() ? "/discover" : "/login"}
              replace
            />
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

function ProtectedLayout() {
  if (!hasSession()) {
    return <Navigate to="/login" replace />;
  }

  const user = getStoredUser();

  return (
    <>
      <Navbar user={user} />
      <Outlet />
    </>
  );
}

function hasSession() {
  return Boolean(localStorage.getItem("access_token"));
}

function getStoredUser(): User {
  const storedUser = localStorage.getItem("current_user");

  if (!storedUser) {
    return {} as User;
  }

  try {
    return JSON.parse(storedUser) as User;
  } catch {
    return {} as User;
  }
}

export default App;