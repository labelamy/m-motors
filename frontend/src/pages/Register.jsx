import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";

function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await API.post("/auth/register", {
        email,
        password,
      });

      alert("Inscription réussie ✅");
      navigate("/login");
    } catch (error) {
      console.error(error);
      alert("Erreur lors de l'inscription ❌");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container vh-100 d-flex justify-content-center align-items-center ">

      <div className="card shadow-lg border-0 register-card" style={{ width: "100%", maxWidth: "420px" }}>

        <div className="">

          <div className="card-body p-4">

            <h3 className="text-center mb-4 fw-bold">
              📝 Inscription
            </h3>

            <form onSubmit={handleRegister}>

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
                  placeholder="Créer un mot de passe"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>

              <button
                className="btn btn-success w-100"
                disabled={loading}
              >
                {loading ? "Inscription..." : "S'inscrire"}
              </button>

            </form>

            <p className="text-center mt-3">
              Déjà un compte ?{" "}
              <a href="/login">
                Se connecter
              </a>
            </p>

          </div>

        </div>

      </div>

    </div>
  );
}

export default Register;