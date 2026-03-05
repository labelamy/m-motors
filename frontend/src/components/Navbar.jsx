import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark px-3">
      <Link className="navbar-brand" to="/">M-Motors</Link>

      <div className="ms-auto">
        {!token ? (
          <>
            <Link className="btn btn-outline-light me-2" to="/login">Login</Link>
            <Link className="btn btn-light" to="/register">Register</Link>
            <Link className="nav-link" to="/dossiers"> Mes Dossiers</Link>
          </>
        ) : (
          <button className="btn btn-danger" onClick={handleLogout}>
            Logout
          </button>
        )}
      </div>
    </nav>
  );
}

export default Navbar;