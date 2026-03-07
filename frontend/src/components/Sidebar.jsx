import { Link } from "react-router-dom";

function Sidebar() {
   const token = localStorage.getItem("token");

  if (!token) return null; // Masquer la sidebar si pas connecté
  
  return (
    <div className="bg-dark text-white p-3 vh-100 sidebar">

      <h4 className="mb-4">Admin</h4>

      <ul className="nav flex-column">

        <li className="nav-item">
          <Link className="nav-link text-white" to="/admin">
            Dashboard
          </Link>
        </li>

        <li className="nav-item">
          <Link className="nav-link text-white" to="/dossiers">
            Dossiers
          </Link>
        </li>

        <li className="nav-item">
          <Link className="nav-link text-white" to="/">
            Véhicules
          </Link>
        </li>

      </ul>

    </div>
  );
}

export default Sidebar;