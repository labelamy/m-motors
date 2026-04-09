import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../services/api";
import { jwtDecode } from "jwt-decode";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Appel à l'API pour se connecter
      const response = await API.post("/users/login", {
        email,
        password
      });

      const { access_token } = response.data;

      // Décodage du token
      const decoded = jwtDecode(access_token);

      const userEmail = decoded.sub;
      const userRole = decoded.role || "client";

      // Stockage
      localStorage.setItem("token", access_token);
      localStorage.setItem(
        "currentUser",
        JSON.stringify({ email: userEmail, role: userRole })
      );

      console.log("Utilisateur :", decoded);

      // Redirection en fonction du rôle
      if (userRole === "admin") {
        navigate("/admin");
      } else {
        navigate("/vehicules");
      }

    } catch (error) {
      console.error(error);
      alert("Email ou mot de passe incorrect ❌");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container-fluid vh-100 d-flex justify-content-center align-items-center bg-light">
      <div className="card shadow-lg border-0" style={{ width: "100%", maxWidth: "420px" }}>
        <div className="card-body p-4">
          <h3 className="text-center mb-4 fw-bold">🔐 Connexion</h3>

          <form onSubmit={handleLogin}>
            <div className="mb-3">
              <label className="form-label">Email</label>
              <input
                type="email"
                className="form-control"
                placeholder="exemple@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="mb-4">
              <label className="form-label">Mot de passe</label>
              <input
                type="password"
                className="form-control"
                placeholder="Votre mot de passe"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <button className="btn btn-primary w-100" disabled={loading}>
              {loading ? "Connexion..." : "Se connecter"}
            </button>

            <p className="text-center mt-3">
              Pas de compte ? <Link to="/register">Créer un compte</Link>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Login;