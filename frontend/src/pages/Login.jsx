import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      // Envoi du JSON {email, password} au backend
      const response = await API.post("/auth/login", { email, password });

      // Récupération du token
      const { access_token } = response.data;
      localStorage.setItem("token", access_token);

      alert("Connexion réussie !");
      navigate("/"); // redirige vers la page d'accueil (liste des véhicules)
    } catch (error) {
      console.error(error);
      alert("Email ou mot de passe incorrect");
    }
  };

  return (
    <div className="container mt-5">
      <h2>Connexion</h2>
      <form onSubmit={handleLogin}>
        <div className="mb-3">
          <label>Email</label>
          <input
            type="email"
            className="form-control"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="mb-3">
          <label>Mot de passe</label>
          <input
            type="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button className="btn btn-primary">Se connecter</button>
      </form>
    </div>
  );
}

export default Login;