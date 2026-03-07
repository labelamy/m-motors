import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Vehicules from "./pages/Vehicules";
import PrivateRoute from "./components/PrivateRoute";
import Navbar from "./components/Navbar";
import Dossiers from "./pages/Dossiers";
import AdminDashboard from "./pages/AdminDashboard";

import "./App.css";

function App() {
  return (
    <Router>
      <Navbar />

      <Routes>
        {/* Redirection automatique vers /vehicules */}
        <Route path="/" element={<Navigate to="/vehicules" />} />

        {/* Routes publiques */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Route protégée */}
        <Route
          path="/vehicules"
          element={
            <PrivateRoute>
              <Vehicules />
            </PrivateRoute>
          }
        />
        <Route
          path="/dossiers"
          element={
            <PrivateRoute>
              <Dossiers />
            </PrivateRoute>
          }
        />
        {/* Route fallback si URL inconnue */}
        <Route path="*" element={<Navigate to="/login" />} />
        <Route path="/admin"
                element={
                  <PrivateRoute>
                    <AdminDashboard />
                  </PrivateRoute>
                }
              />
      </Routes>
    </Router>
  );
}

export default App;