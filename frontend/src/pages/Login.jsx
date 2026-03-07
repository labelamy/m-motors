import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await API.post("/auth/login", { email, password });

      const { access_token } = response.data;
      localStorage.setItem("token", access_token);

      alert("Connexion réussie ✅");
      navigate("/");
    } catch (error) {
      console.error(error);
      alert("Email ou mot de passe incorrect ❌");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container vh-100 d-flex justify-content-center align-items-center">

      <div className="col-12 col-md-6 col-lg-4">

        <div className="card shadow-lg border-0 login-card">

          <div className="card-body p-4">

            <h3 className="text-center mb-4 fw-bold">
              🔐 Connexion
            </h3>

            <form onSubmit={handleLogin}>

              <div className="mb-3">
                <label className="form-label">
                  Email
                </label>

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
                <label className="form-label">
                  Mot de passe
                </label>

                <input
                  type="password"
                  className="form-control"
                  placeholder="Votre mot de passe"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>

              <button
                className="btn btn-primary w-100"
                disabled={loading}
              >
                {loading ? "Connexion..." : "Se connecter"}
              </button>
              <p className="text-center mt-3">
                Pas de compte ? <a href="/register">Créer un compte</a>
              </p>
            </form>

          </div>

        </div>

      </div>

    </div>
  );
}

export default Login;