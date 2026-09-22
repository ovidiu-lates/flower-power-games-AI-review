import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import Login from './pages/Login';
import Discover from "./pages/Discover";

function App() {
    return (
        <BrowserRouter>
        <Routes>
        <Route path= "/" element = {< Login />} />
            < Route path = "/login" element = {< Login />} />
                < Route path = "*" element = {< Navigate to = "/" replace />} />
                < Route path = "/discover" element = {< Discover />} />
                    </Routes>
                    </BrowserRouter>
  );
}

export default App;