import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Vehicules from "./pages/Vehicules";
import PrivateRoute from "./components/PrivateRoute";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer"; 
import AdminRoute from "./components/AdminRoute";
import Dossiers from "./pages/Dossiers";
import AdminDashboard from "./pages/AdminDashboard";
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; 
import VehiculeDetail from "./pages/VehiculeDetail";

import "./App.css";

function App() {
  return (
    <Router>
      {/* Conteneur global en flex-column */}
      <div className="d-flex flex-column min-vh-100">
        {/* Navbar fixe en haut */}
        <Navbar />

        {/* Contenu principal qui pousse le footer vers le bas */}
        <div className="flex-grow-1">
          <Routes>
            <Route path="/" element={<Navigate to="/vehicules" />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/vehicules"
              element={
                <PrivateRoute>
                  <Vehicules />
                </PrivateRoute>
              }
            />
            <Route path="/vehicules/:id" element={<VehiculeDetail />} />
            <Route
              path="/dossiers"
              element={
                <PrivateRoute>
                  <Dossiers />
                </PrivateRoute>
              }
            />
            <Route
              path="/admin"
              element={
                <AdminRoute>
                  <AdminDashboard />
                </AdminRoute>
              }
            />
            <Route path="*" element={<Navigate to="/login" />} />
          </Routes>
        </div>

        {/* Footer collé en bas */}
        <Footer />
      </div>
    </Router>
  );
}

export default App;